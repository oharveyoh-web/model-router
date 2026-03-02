# model-router

A Claude Code plugin that automatically selects the cheapest Claude model capable of handling each task, saving token costs by routing simple tasks to Haiku and reserving Opus for complex work.

## How It Works

| Model  | Relative Cost | Best For                        |
|--------|---------------|---------------------------------|
| Haiku  | 1x            | Reads, queries, formatting      |
| Sonnet | ~10x          | Standard dev work               |
| Opus   | ~30x          | Architecture, deep debugging    |

70-80% of coding tasks are simple enough for cheaper tiers. This plugin classifies tasks by complexity and routes them to the optimal model.

## Installation

```bash
claude --plugin-dir /path/to/model-router
```

## Usage

### Auto-classify and delegate

```
/route <task description>
```

Runs a Haiku-powered classifier, then delegates to the appropriate worker agent (haiku-worker, sonnet-worker, or opus-worker).

### Direct routing shortcuts

```
/route-haiku <task>    # Force Haiku (simple tasks)
/route-sonnet <task>   # Force Sonnet (standard tasks)
/route-opus <task>     # Force Opus (complex tasks)
```

### View routing stats

```
/route-stats
```

Shows routing history and estimated cost savings.

## Classification Rules

**Haiku** (simple tasks):
- File reads, listing, status checks
- Git status, diff, log, branch viewing
- Code formatting, linting
- Simple questions, search/grep operations
- Commit messages, changelog entries

**Sonnet** (standard tasks):
- Single-file code changes or bug fixes
- Writing tests, code review
- Documentation, API endpoints
- Standard feature implementation

**Opus** (complex tasks):
- Multi-file refactoring or migration
- Architecture design or redesign
- Security analysis, vulnerability review
- Performance optimization, memory leaks
- Complex debugging across system boundaries

## Components

- **Commands** (`/route`, `/route-haiku`, `/route-sonnet`, `/route-opus`, `/route-stats`)
- **Agents** (haiku-worker, sonnet-worker, opus-worker) — model-locked subagents
- **Hook** — zero-cost heuristic classifier that advises when a task/model mismatch is detected
- **Skill** — auto-triggered model routing guidance
- **Script** (`smartroute.sh`) — optional CLI wrapper for non-interactive use

## License

MIT
