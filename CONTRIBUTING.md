# Contributing to traderStack

## Quick start

```bash
git clone https://github.com/apexphere/traderStack.git
cd traderStack
pip install -r requirements.txt
python -m pytest test/ -v            # 55 tests, should all pass
./setup                              # symlink skills for local testing
```

## Project layout

```
traderStack/
├── {skill-name}/SKILL.md    # Skill templates (read by Claude Code)
├── backtest/templates/       # Python strategy archetypes
├── lib/                      # Shared Python libraries
└── test/                     # pytest test suite
```

## Making changes

### Skill templates (SKILL.md)
These are Markdown files read by Claude Code as prompts. Edit them directly.
Test by running the skill in a Claude Code session.

### Python libraries (lib/)
Write tests first. Run `python -m pytest test/ -v` before committing.

### Strategy templates (backtest/templates/)
Each template is a constrained bt strategy archetype. If adding a new archetype:
1. Create `trader/backtest/templates/{name}.py`
2. Include `download_data()`, `build_strategy()`, `build_benchmark()`, `run_and_report()`
3. The `run_and_report()` function must return both strategy and B&H benchmark results
4. Update the archetype list in `trader/backtest/SKILL.md`

## Testing

```bash
python -m pytest test/ -v         # all tests
python -m pytest trader/test/ -k "bias"  # just bias check tests
python -m pytest trader/test/ -k "quiz"  # just quiz tests
```

## Commit style

```
<type>: <description>

Types: feat, fix, refactor, docs, test, chore
```
