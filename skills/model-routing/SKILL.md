---
name: model-routing
description: This skill should be used when the user asks to "route this task", "pick the right model", "which model should I use", "optimize cost", "use the cheapest model", or when the user submits a task that is clearly simple (file reads, formatting, git status) while running on Opus, or clearly complex (multi-file refactoring, architecture) while running on Haiku. Provides model selection guidance to minimize token costs.
version: 1.0.0
---

# Model Routing Skill

This skill classifies tasks by complexity and recommends the optimal Claude model tier to minimize cost while maintaining quality.

## When This Skill Applies

This skill activates when:
- A task's complexity clearly mismatches the current model tier
- The user explicitly asks about model selection or cost optimization
- A simple task is being handled by an expensive model (Opus)
- A complex task is being handled by a cheap model (Haiku)

## Model Tiers

### Haiku (fastest, cheapest)

Route to Haiku via `/route-haiku <task>` or the **haiku-worker** agent.

Task indicators:
- Simple questions with factual answers
- File reading, listing, status checks
- Code formatting, linting, indentation
- Git status, diff, log, branch viewing
- Simple text generation (commit messages, comments, changelogs)
- Search/grep operations
- Explaining a single function or error
- Simple regex or string operations

### Sonnet (balanced)

Route to Sonnet via `/route-sonnet <task>` or the **sonnet-worker** agent.

Task indicators:
- Single-file code changes or bug fixes
- Writing tests for existing code
- Code review of small changes
- Documentation writing
- API endpoint implementation
- Configuration changes
- Moderate refactoring within one file
- Standard feature implementation

### Opus (most capable, most expensive)

Route to Opus via `/route-opus <task>` or the **opus-worker** agent.

Task indicators:
- Multi-file refactoring or migration
- Architecture design or redesign
- Complex debugging across system boundaries
- Security analysis or vulnerability review
- Performance optimization or memory leak investigation
- System design decisions
- Complex algorithm implementation
- Cross-cutting concerns affecting many modules

## Classification Heuristics

To classify a task, check these patterns in order:

**Opus signals** (check first):
- Words like "refactor", "redesign", "architect", "migrate" combined with "system", "entire", "whole", "across"
- "multi-file" anywhere in the task
- "security/vulnerability/audit" + "analysis/review/scan"
- "performance/memory" + "optimization/leak"
- "rewrite" or "overhaul"
- "cross-cutting"
- Very long prompts (100+ words) with detailed requirements

**Haiku signals** (check second):
- Starts with "what", "show", "list", "display", "print", "read", "get"
- Contains "format", "lint", "prettify", "indent"
- Git read operations: "git status", "git log", "git diff", "git show"
- "explain this/that/the function/method/line/error"
- "commit message" or "changelog entry"
- "search/grep/find for/in"
- "simple question/fix/change/update"

**Sonnet (default):** Everything else falls here — standard development work.

## How to Apply

When this skill triggers:

1. Identify the current model from environment context
2. Classify the task using the heuristics above
3. If there is a mismatch (simple task on Opus, or complex task on Haiku), suggest the appropriate routing command:
   - `/route-haiku <task>` for simple tasks
   - `/route-sonnet <task>` for standard tasks
   - `/route-opus <task>` for complex tasks
4. If no mismatch, proceed normally without interruption

To auto-classify and delegate in one step, use `/route <task>` — this runs the classifier on Haiku and delegates to the appropriate worker agent.

## Cost Reference

| Model  | Relative Cost | Best For                        |
|--------|---------------|---------------------------------|
| Haiku  | 1x            | Reads, queries, formatting      |
| Sonnet | ~10x          | Standard dev work               |
| Opus   | ~30x          | Architecture, deep debugging    |

Diverting a simple task from Opus to Haiku saves ~$0.05-0.50 per task. With 70-80% of tasks being simple enough for cheaper tiers, savings compound quickly.

## Routing Commands Reference

- `/route <task>` — Auto-classify and delegate (runs classifier on Haiku)
- `/route-haiku <task>` — Force Haiku execution
- `/route-sonnet <task>` — Force Sonnet execution
- `/route-opus <task>` — Force Opus execution
- `/route-stats` — View routing log and estimated savings
