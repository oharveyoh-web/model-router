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

---

# model-router (FR)

Un plugin Claude Code qui selectionne automatiquement le modele Claude le moins cher capable de traiter chaque tache, en reduisant les couts de tokens en routant les taches simples vers Haiku et en reservant Opus pour les taches complexes.

## Fonctionnement

| Modele | Cout relatif | Ideal pour                            |
|--------|--------------|---------------------------------------|
| Haiku  | 1x           | Lectures, requetes, formatage         |
| Sonnet | ~10x         | Travail de dev standard               |
| Opus   | ~30x         | Architecture, debugging approfondi    |

70-80% des taches de dev sont assez simples pour des modeles moins chers. Ce plugin classe les taches par complexite et les redirige vers le modele optimal.

## Installation

Il y a deux facons d'utiliser model-router : en tant que **plugin complet** ou en tant que **commande autonome**.

### Option A : Plugin complet (recommande)

Donne acces a toutes les fonctionnalites — commandes slash, agents, hook d'avertissement et skill auto-declenchee.

```bash
git clone https://github.com/oharveyoh-web/model-router.git
claude --plugin-dir /chemin/vers/model-router
```

### Option B : Commande autonome (alternative legere)

Si vous voulez uniquement la fonctionnalite de routage sans installer le plugin complet, copiez un seul fichier :

```bash
# Copier la commande autonome dans vos commandes globales Claude Code
cp standalone/model-routing.md ~/.claude/commands/model-routing.md
```

Puis utilisez-la dans n'importe quelle session Claude Code avec :

```
/model-routing <description de la tache>
```

Cela classe la tache, recommande un tier de modele et delegue a un sous-agent au bon tier. Aucun chargement de plugin requis.

**Differences par rapport au plugin complet :**
- Pas de raccourcis `/route-haiku`, `/route-sonnet`, `/route-opus`
- Pas de hook d'avertissement (detection passive de desequilibre)
- Pas de journalisation `/route-stats`
- Pas de skill auto-declenchee
- Fonctionne globalement sans `--plugin-dir`

---

## Utilisation (Plugin complet)

### Classification automatique et delegation

```
/route <description de la tache>
```

Lance un classificateur sur Haiku (le moins cher), puis delegue a l'agent adapte (haiku-worker, sonnet-worker ou opus-worker).

### Raccourcis de routage direct

```
/route-haiku <tache>    # Forcer Haiku (taches simples)
/route-sonnet <tache>   # Forcer Sonnet (taches standard)
/route-opus <tache>     # Forcer Opus (taches complexes)
```

### Voir les statistiques de routage

```
/route-stats
```

Affiche l'historique de routage et les economies estimees.

## Regles de classification

**Haiku** (taches simples) :
- Lecture de fichiers, listes, verifications d'etat
- Git status, diff, log, affichage de branches
- Formatage de code, linting
- Questions simples, recherches grep
- Messages de commit, entrees de changelog

**Sonnet** (taches standard) :
- Modifications ou corrections dans un seul fichier
- Ecriture de tests, revue de code
- Documentation, endpoints API
- Implementation de fonctionnalites standard

**Opus** (taches complexes) :
- Refactoring ou migration multi-fichiers
- Conception ou reconception d'architecture
- Analyse de securite, revue de vulnerabilites
- Optimisation de performances, fuites memoire
- Debugging complexe entre composants systeme

## Composants

- **Commandes** (`/route`, `/route-haiku`, `/route-sonnet`, `/route-opus`, `/route-stats`)
- **Agents** (haiku-worker, sonnet-worker, opus-worker) — sous-agents verrouilles sur un modele
- **Hook** — classificateur heuristique sans cout qui avertit lors d'un desequilibre tache/modele
- **Skill** — guide de routage auto-declenche
- **Script** (`smartroute.sh`) — wrapper CLI optionnel pour utilisation non-interactive

## Licence

MIT
