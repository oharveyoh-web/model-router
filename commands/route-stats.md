---
description: View model routing statistics and estimated cost savings
allowed-tools: [Bash, Read]
---

# Model Router Statistics

Read the file `.claude/model-router.log` and provide a summary:

1. Read the log file `.claude/model-router.log`
2. Count entries by model tier (HAIKU, SONNET, OPUS, and their -DIRECT variants)
3. Show the last 20 routing decisions
4. Estimate approximate cost savings:
   - Each HAIKU task that would have run on Opus: ~$0.05 saved
   - Each SONNET task that would have run on Opus: ~$0.03 saved
   - ADVISORY entries: show how many suggestions were made
5. Show total count and percentage breakdown by tier

If the log file doesn't exist, report that no routing has been logged yet
and suggest using `/route <task>` to get started.

Format the output as a clean, readable report.
