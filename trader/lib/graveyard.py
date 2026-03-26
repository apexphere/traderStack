"""Strategy Graveyard — post-mortems for rejected strategies.

When /strategy-review gates REJECT, a post-mortem is auto-generated at
~/.traderstack/graveyard/{name}.md. Over time, this becomes the most
valuable asset: a catalog of mistakes you'll never make again.
"""

import re
from datetime import datetime, timezone
from pathlib import Path


GRAVEYARD_DIR = Path.home() / ".traderstack" / "graveyard"


def ensure_graveyard() -> Path:
    """Create the graveyard directory if it doesn't exist."""
    GRAVEYARD_DIR.mkdir(parents=True, exist_ok=True)
    return GRAVEYARD_DIR


def write_postmortem(
    strategy_name: str,
    thesis: str,
    rejection_reason: str,
    bias_found: str,
    lesson: str,
    backtest_summary: str = "",
) -> Path:
    """Write a post-mortem for a rejected strategy.

    Returns the path to the written file.
    """
    graveyard = ensure_graveyard()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    slug = re.sub(r"[^a-z0-9]+", "-", strategy_name.lower()).strip("-")
    file_path = graveyard / f"{slug}-{timestamp}.md"

    content = (
        f"# Post-Mortem: {strategy_name}\n\n"
        f"**Date:** {timestamp}\n"
        f"**Verdict:** REJECTED\n\n"
        f"## Thesis\n\n{thesis}\n\n"
        f"## Why It Failed\n\n{rejection_reason}\n\n"
        f"## Bias / Issue Found\n\n{bias_found}\n\n"
    )

    if backtest_summary:
        content += f"## Backtest Summary\n\n{backtest_summary}\n\n"

    content += f"## Lesson Learned\n\n{lesson}\n"

    file_path.write_text(content)
    return file_path
