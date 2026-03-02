---
description: Execute a task directly on Haiku (fastest, cheapest)
argument-hint: <task description>
model: haiku
---

Execute this task efficiently and concisely:

$ARGUMENTS

After completing the task, log it:
```bash
mkdir -p .claude && echo "[$(date '+%Y-%m-%d %H:%M:%S')] HAIKU-DIRECT | $(echo 'task' | head -c 80)" >> .claude/model-router.log
```
