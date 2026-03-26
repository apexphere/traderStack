"""Quant Concept Quiz Gate.

Gates ALL traderStack skills on first use. The user must demonstrate basic
understanding of quant concepts before any skill will run.

Marker file: ~/.traderstack/.quiz-done
"""

from dataclasses import dataclass
from pathlib import Path


QUIZ_MARKER = Path.home() / ".traderstack" / ".quiz-done"

# Each question: (question_text, correct_answer_keyword, explanation, verification_hint)
QUIZ_QUESTIONS: tuple[tuple[str, str, str, str], ...] = (
    (
        "What is lookahead bias in backtesting?",
        "future",
        "Lookahead bias occurs when a strategy uses information that would not "
        "have been available at the time of the trade — like using tomorrow's "
        "closing price to make today's decision.",
        "Verify: Search 'lookahead bias backtesting' on QuantPedia or read "
        "Advances in Financial Machine Learning, Chapter 7.",
    ),
    (
        "A strategy has a Sharpe ratio of 0.5. Is that good, bad, or "
        "depends on context? Why?",
        "context",
        "It depends on context. A Sharpe of 0.5 means the strategy earns "
        "0.5 units of return per unit of risk. For a low-frequency strategy "
        "this is mediocre; for a high-frequency strategy it might be "
        "acceptable. Sample size matters — 0.5 on 20 trades is meaningless.",
        "Verify: Search 'interpreting Sharpe ratio backtesting' or read "
        "QuantStart's guide to the Sharpe Ratio.",
    ),
    (
        "Why is survivorship bias dangerous when backtesting a stock "
        "selection strategy?",
        "delisted",
        "Survivorship bias means your backtest only includes stocks that "
        "survived to the present — excluding companies that went bankrupt "
        "or were delisted. This inflates historical returns because you're "
        "only looking at winners.",
        "Verify: Search 'survivorship bias stock backtesting' or see "
        "Advances in Financial Machine Learning, Chapter 6.",
    ),
    (
        "You backtest a strategy and it returns 40% annually. What's the "
        "first thing you should check before getting excited?",
        "overfit",
        "Check for overfitting. A 40% annual return is suspiciously high. "
        "Compare in-sample vs out-of-sample performance. If the strategy "
        "was optimized on the same data it's being tested on, the results "
        "are meaningless.",
        "Verify: Search 'overfitting backtesting detection' or read "
        "'The Deflated Sharpe Ratio' by Bailey & Lopez de Prado.",
    ),
    (
        "What is the difference between a strategy's maximum drawdown "
        "and its average drawdown? Which matters more for risk management?",
        "maximum",
        "Maximum drawdown is the largest peak-to-trough decline. Average "
        "drawdown is the mean of all drawdowns. Maximum drawdown matters "
        "more for risk management because it represents the worst-case "
        "scenario — the point where most people panic and quit.",
        "Verify: Search 'maximum drawdown risk management' or see "
        "Investopedia's drawdown guide.",
    ),
)

PASSING_SCORE = 3  # out of 5 — calibrate through dogfooding


@dataclass(frozen=True)
class QuizResult:
    passed: bool
    score: int
    total: int
    feedback: tuple[str, ...]


def is_quiz_done() -> bool:
    """Check if the user has already passed the quiz."""
    return QUIZ_MARKER.exists()


def mark_quiz_done() -> None:
    """Mark the quiz as passed."""
    QUIZ_MARKER.parent.mkdir(parents=True, exist_ok=True)
    QUIZ_MARKER.touch()


def reset_quiz() -> None:
    """Reset the quiz (for testing or re-learning)."""
    QUIZ_MARKER.unlink(missing_ok=True)


def get_questions() -> tuple[tuple[str, str, str, str], ...]:
    """Return the quiz questions."""
    return QUIZ_QUESTIONS


def evaluate_answer(question_index: int, answer: str) -> tuple[bool, str, str]:
    """Evaluate a single answer.

    Returns (is_correct, explanation, verification_hint).

    Uses keyword matching as a heuristic — the LLM skill template does the
    real evaluation. This function provides the ground truth for the skill
    to reference.
    """
    if question_index < 0 or question_index >= len(QUIZ_QUESTIONS):
        return (False, "Invalid question index.", "")

    _, keyword, explanation, hint = QUIZ_QUESTIONS[question_index]
    # Simple keyword presence check — the skill template does nuanced evaluation
    is_correct = keyword.lower() in answer.lower()
    return (is_correct, explanation, hint)


def evaluate_quiz(answers: tuple[str, ...]) -> QuizResult:
    """Evaluate all quiz answers and return the result."""
    if len(answers) != len(QUIZ_QUESTIONS):
        return QuizResult(
            passed=False,
            score=0,
            total=len(QUIZ_QUESTIONS),
            feedback=("Wrong number of answers provided.",),
        )

    score = 0
    feedback_items = []

    for i, answer in enumerate(answers):
        correct, explanation, hint = evaluate_answer(i, answer)
        if correct:
            score += 1
            feedback_items.append(f"Q{i + 1}: Correct. {hint}")
        else:
            feedback_items.append(
                f"Q{i + 1}: Not quite. {explanation} {hint}"
            )

    passed = score >= PASSING_SCORE
    return QuizResult(
        passed=passed,
        score=score,
        total=len(QUIZ_QUESTIONS),
        feedback=tuple(feedback_items),
    )
