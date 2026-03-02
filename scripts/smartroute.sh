#!/usr/bin/env bash
# smartroute - Pre-routing wrapper for claude CLI
# Usage: smartroute "your task description here"
#
# Classifies the task and routes to the optimal model.

set -euo pipefail

TASK="${1:-}"
if [ -z "$TASK" ]; then
    echo "Usage: smartroute \"your task description\""
    echo ""
    echo "Automatically selects the cheapest model that can handle your task."
    echo ""
    echo "  Haiku  - file reads, formatting, status checks, simple questions"
    echo "  Sonnet - bug fixes, tests, single-file features, docs"
    echo "  Opus   - multi-file refactoring, architecture, deep debugging"
    exit 1
fi

LOWER_TASK=$(echo "$TASK" | tr '[:upper:]' '[:lower:]')

# Heuristic classification (mirrors classify_prompt.py)
MODEL="sonnet"
REASON="standard task"

# Check opus indicators
if echo "$LOWER_TASK" | grep -qiE '(refactor|redesign|architect|migration).*(system|entire|whole|all|across)'; then
    MODEL="opus"; REASON="complex multi-scope task"
elif echo "$LOWER_TASK" | grep -qiE 'multi.?file'; then
    MODEL="opus"; REASON="multi-file operation"
elif echo "$LOWER_TASK" | grep -qiE '(security|vulnerability|audit)\s+(analysis|review)'; then
    MODEL="opus"; REASON="security analysis"
elif echo "$LOWER_TASK" | grep -qiE '(performance|memory)\s+(optimization|leak)'; then
    MODEL="opus"; REASON="performance work"
elif echo "$LOWER_TASK" | grep -qiE '(rewrite|overhaul)'; then
    MODEL="opus"; REASON="major rewrite"

# Check haiku indicators
elif echo "$LOWER_TASK" | grep -qiE '^(what|show|list|display|print|read|cat|get)\s'; then
    MODEL="haiku"; REASON="simple query"
elif echo "$LOWER_TASK" | grep -qiE '\b(format|lint|prettify)\b'; then
    MODEL="haiku"; REASON="formatting task"
elif echo "$LOWER_TASK" | grep -qiE 'git\s+(status|log|diff|show)'; then
    MODEL="haiku"; REASON="git status check"
elif echo "$LOWER_TASK" | grep -qiE '(search|grep|find)\s+(for|in)'; then
    MODEL="haiku"; REASON="search operation"
fi

# Log the decision
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
SUMMARY=$(echo "$TASK" | head -c 80 | tr '\n' ' ')
mkdir -p .claude
echo "[$TIMESTAMP] SCRIPT ${MODEL^^} | $SUMMARY" >> .claude/model-router.log

echo "[Model Router] Selected: $MODEL ($REASON)"
echo "---"

# Execute with selected model
claude -p --model "$MODEL" "$TASK"
