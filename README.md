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

There are two ways to use model-router: as a **full plugin** or as a **standalone command**.

### Option A: Full Plugin (recommended)

Gives you all features — slash commands, worker agents, advisory hook, and auto-triggered skill.

```bash
git clone https://github.com/oharveyoh-web/model-router.git
claude --plugin-dir /path/to/model-router
```

### Option B: Standalone Command (lightweight alternative)

If you just want the core routing functionality without installing the full plugin, copy a single file:

```bash
# Copy the standalone command to your global Claude Code commands
cp standalone/model-routing.md ~/.claude/commands/model-routing.md
```

Then use it in any Claude Code session with:

```
/model-routing <task description>
```

This classifies the task, recommends a model tier, and delegates to a subagent at the right tier. No plugin loading required.

**Differences from the full plugin:**
- No `/route-haiku`, `/route-sonnet`, `/route-opus` shortcuts
- No advisory hook (passive mismatch detection)
- No `/route-stats` logging
- No auto-triggered skill
- Works globally without `--plugin-dir`

---

## Usage (Full Plugin)

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
