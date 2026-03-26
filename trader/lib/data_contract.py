"""Strategy Design Doc data contract.

The Strategy Design Doc is the shared artifact that flows through all traderStack skills:
  /strategy-thesis writes it → /backtest appends results → /strategy-review reads + gates.

All docs are Markdown files at ~/.traderstack/strategies/{name}-{date}.md
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


STRATEGIES_DIR = Path.home() / ".traderstack" / "strategies"

REQUIRED_SECTIONS = (
    "Thesis",
    "Evidence",
    "Premises",
    "Entry Rules",
    "Exit Rules",
    "Universe",
    "Position Sizing",
    "Risk Limits",
    "Expected Metrics",
    "Known Weaknesses",
    "Status",
)

VALID_STATUSES = frozenset({
    "DRAFT",
    "BACKTESTED",
    "REVIEWED",
    "PAPER_TRADING",
    "REJECTED",
})

BACKTEST_REQUIRED_SUBSECTIONS = (
    "Regime Performance",
    "Bias Checks",
    "Generated On",
    "Code Path",
)


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    missing_sections: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class BiasCheckResult:
    check_name: str
    result: str  # "PASS", "WARN", or "FAIL"
    notes: str = ""


@dataclass(frozen=True)
class RegimeResult:
    regime: str
    period: str
    total_return: float
    sharpe: float
    max_drawdown: float
    trades: int


@dataclass(frozen=True)
class BacktestResults:
    regime_results: tuple[RegimeResult, ...]
    bias_checks: tuple[BiasCheckResult, ...]
    generated_on: str
    code_path: str


@dataclass(frozen=True)
class StrategyDoc:
    name: str
    thesis: str
    evidence: str
    premises: str
    entry_rules: str
    exit_rules: str
    universe: str
    position_sizing: str
    risk_limits: str
    expected_metrics: str
    known_weaknesses: str
    status: str
    backtest_results: Optional[BacktestResults] = None
    file_path: Optional[Path] = None


def ensure_strategies_dir() -> Path:
    """Create the strategies directory if it doesn't exist."""
    STRATEGIES_DIR.mkdir(parents=True, exist_ok=True)
    return STRATEGIES_DIR


def validate_doc(content: str) -> ValidationResult:
    """Validate that a Strategy Design Doc has all required sections."""
    missing = []
    warnings = []

    for section in REQUIRED_SECTIONS:
        pattern = rf"^##\s+{re.escape(section)}"
        if not re.search(pattern, content, re.MULTILINE):
            missing.append(section)

    # Check status value if present
    status_match = re.search(r"^##\s+Status:\s*(.+)$", content, re.MULTILINE)
    if status_match:
        status_value = status_match.group(1).strip()
        if status_value not in VALID_STATUSES:
            warnings.append(
                f"Invalid status '{status_value}'. "
                f"Valid: {', '.join(sorted(VALID_STATUSES))}"
            )

    return ValidationResult(
        valid=len(missing) == 0,
        missing_sections=tuple(missing),
        warnings=tuple(warnings),
    )


def has_backtest_results(content: str) -> bool:
    """Check if a Strategy Design Doc has backtest results appended."""
    return bool(re.search(r"^##\s+Backtest Results", content, re.MULTILINE))


def parse_section(content: str, section_name: str) -> str:
    """Extract the content of a named section from the doc."""
    pattern = rf"^##\s+{re.escape(section_name)}.*?\n(.*?)(?=^##\s|\Z)"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


def strategy_file_path(name: str, date_str: str) -> Path:
    """Build the file path for a strategy doc."""
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return ensure_strategies_dir() / f"{slug}-{date_str}.md"
