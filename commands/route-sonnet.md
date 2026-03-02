---
description: Execute a task directly on Sonnet (balanced cost/quality)
argument-hint: <task description>
model: sonnet
---

Execute this task thoroughly:

$ARGUMENTS

After completing the task, log it:
```bash
mkdir -p .claude && echo "[$(date '+%Y-%m-%d %H:%M:%S')] SONNET-DIRECT | $(echo 'task' | head -c 80)" >> .claude/model-router.log
```
