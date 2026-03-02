#!/usr/bin/env python3
"""UserPromptSubmit hook for model-router plugin.

Classifies user prompts using keyword heuristics and injects an advisory
system message suggesting the optimal model tier. Uses NO LLM calls —
pure regex/keyword matching for zero additional token cost.
"""

import sys
import json
import re
import os
from datetime import datetime

# Check opus indicators first (complex tasks), then haiku (simple), default sonnet
OPUS_PATTERNS = [
    r'\b(refactor|redesign|architect|migration|migrate)\b.*\b(system|entire|whole|all|across)\b',
    r'\bmulti.?file\b',
    r'\b(security|vulnerability|audit)\s+(analysis|review|scan)\b',
    r'\b(performance|memory)\s+(optimization|leak|profil)',
    r'\b(design|architect)\s+(system|service|api|database|schema)\b',
    r'\bcomplex\s+(debug|bug|issue|problem)\b',
    r'\b(rewrite|overhaul)\b',
    r'\bcross.?cutting\b',
]

HAIKU_PATTERNS = [
    r'^(what|show|list|display|print|read|cat|get)\s',
    r'\b(format|lint|prettify|indent)\b',
    r'\bgit\s+(status|log|diff|show|branch)\b',
    r'\bexplain\s+(this|that|the)\s+(function|method|line|error)\b',
    r'\b(commit\s+message|changelog\s+entry)\b',
    r'\b(search|grep|find)\s+(for|in)\b',
    r'\bsimple\s+(question|fix|change|update)\b',
]


def classify_prompt(prompt_text):
    """Classify prompt into haiku/sonnet/opus tier using heuristics."""
    lower = prompt_text.lower().strip()
    word_count = len(lower.split())

    # Very short prompts are likely simple queries
    if word_count <= 5:
        for pattern in HAIKU_PATTERNS:
            if re.search(pattern, lower, re.IGNORECASE):
                return "haiku", "Short, simple query"

    # Check for opus indicators (complex tasks)
    for pattern in OPUS_PATTERNS:
        if re.search(pattern, lower, re.IGNORECASE):
            return "opus", "Complex task detected"

    # Check for haiku indicators (simple tasks)
    for pattern in HAIKU_PATTERNS:
        if re.search(pattern, lower, re.IGNORECASE):
            return "haiku", "Simple task detected"

    # Long prompts with many requirements tend to be complex
    if word_count > 100:
        return "opus", "Long, detailed task description"

    # Default to sonnet
    return "sonnet", "Standard task"


def main():
    try:
        input_data = json.load(sys.stdin)
        prompt = input_data.get("user_prompt", "") or input_data.get("prompt", "")

        if not prompt:
            print(json.dumps({}))
            sys.exit(0)

        tier, reason = classify_prompt(prompt)

        # Only inject advisory when there's a clear mismatch
        current_model = os.environ.get("CLAUDE_MODEL", "unknown").lower()

        message = ""
        if tier == "haiku" and "opus" in current_model:
            message = (
                f"[Model Router] This looks like a simple task ({reason}). "
                f"Consider using /route-haiku or delegating to haiku-worker "
                f"for cost efficiency."
            )
        elif tier == "opus" and "haiku" in current_model:
            message = (
                f"[Model Router] This looks like a complex task ({reason}). "
                f"Consider using /route-opus or delegating to opus-worker "
                f"for better results."
            )

        if message:
            # Log the advisory
            try:
                log_file = os.path.join(".claude", "model-router.log")
                os.makedirs(".claude", exist_ok=True)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                summary = prompt[:80].replace("\n", " ")
                with open(log_file, "a") as f:
                    f.write(f"[{timestamp}] ADVISORY {tier.upper()} | {summary}\n")
            except Exception:
                pass

            print(json.dumps({"systemMessage": message}))
        else:
            print(json.dumps({}))

    except Exception as e:
        # Fail silently — don't break the user's session
        print(json.dumps({}))

    sys.exit(0)


if __name__ == "__main__":
    main()
