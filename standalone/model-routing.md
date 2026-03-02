---
description: Classify a task and recommend the optimal model tier (Haiku/Sonnet/Opus) to minimize token costs
argument-hint: <task description>
---

Classify the following task by complexity and recommend the cheapest Claude model that can handle it well.

**Task:** $ARGUMENTS

## Classification Rules

Check these patterns in order:

### Opus signals (check first)
- Words like "refactor", "redesign", "architect", "migrate" combined with "system", "entire", "whole", "across"
- "multi-file" anywhere in the task
- "security/vulnerability/audit" + "analysis/review/scan"
- "performance/memory" + "optimization/leak"
- "rewrite" or "overhaul"
- "cross-cutting"
- Very long prompts (100+ words) with detailed requirements

### Haiku signals (check second)
- Starts with "what", "show", "list", "display", "print", "read", "get"
- Contains "format", "lint", "prettify", "indent"
- Git read operations: "git status", "git log", "git diff", "git show"
- "explain this/that/the function/method/line/error"
- "commit message" or "changelog entry"
- "search/grep/find for/in"
- "simple question/fix/change/update"

### Sonnet (default)
Everything else — standard development work.

## Cost Reference

| Model  | Relative Cost | Best For                        |
|--------|---------------|---------------------------------|
| Haiku  | 1x            | Reads, queries, formatting      |
| Sonnet | ~10x          | Standard dev work               |
| Opus   | ~30x          | Architecture, deep debugging    |

## Output

1. State the recommended model tier and why (one line)
2. Suggest the user switch via `/model` or delegate to a subagent with the appropriate `model:` parameter using the Agent tool
3. Then execute the task using the Agent tool with the recommended model
