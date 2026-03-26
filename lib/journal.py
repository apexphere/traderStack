"""Strategy Journal — auto-log every thesis→backtest→review cycle.

Appends structured entries to ~/.traderstack/journal.md.
The journal is the user's learning log — searchable, reviewable, and
the trading diary equivalent that pro quants keep.
"""

from datetime import datetime, timezone
from pathlib import Path


JOURNAL_PATH = Path.home() / ".traderstack" / "journal.md"


def ensure_journal() -> Path:
    """Create the journal file with a header if it doesn't exist."""
    JOURNAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not JOURNAL_PATH.exists():
        JOURNAL_PATH.write_text(
            "# traderStack Strategy Journal\n\n"
            "Auto-generated learning log. Each entry records a "
            "thesis→backtest→review cycle.\n\n---\n\n"
        )
    return JOURNAL_PATH


def append_entry(
    strategy_name: str,
    skill_name: str,
    outcome: str,
    what_happened: str,
    what_learned: str,
    ai_caught: str = "",
) -> None:
    """Append a structured journal entry."""
    journal = ensure_journal()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    entry = (
        f"## {timestamp} — {strategy_name} ({skill_name})\n\n"
        f"**Outcome:** {outcome}\n\n"
        f"**What happened:** {what_happened}\n\n"
        f"**What I learned:** {what_learned}\n\n"
    )

    if ai_caught:
        entry += f"**What the AI caught that I missed:** {ai_caught}\n\n"

    entry += "---\n\n"

    with open(journal, "a") as f:
        f.write(entry)
