---
description: Execute a task directly on Opus (most capable)
argument-hint: <task description>
model: opus
---

Execute this task with maximum depth and thoroughness:

$ARGUMENTS

After completing the task, log it:
```bash
mkdir -p .claude && echo "[$(date '+%Y-%m-%d %H:%M:%S')] OPUS-DIRECT | $(echo 'task' | head -c 80)" >> .claude/model-router.log
```
