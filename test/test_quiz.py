"""Tests for the Quant Concept Quiz Gate."""

import pytest

from lib.quiz import (
    PASSING_SCORE,
    QUIZ_QUESTIONS,
    evaluate_answer,
    evaluate_quiz,
    is_quiz_done,
    mark_quiz_done,
    reset_quiz,
)


class TestQuizQuestions:
    def test_five_questions_exist(self):
        assert len(QUIZ_QUESTIONS) == 5

    def test_all_questions_have_four_fields(self):
        for q in QUIZ_QUESTIONS:
            assert len(q) == 4, f"Question missing fields: {q[0][:30]}..."

    def test_all_questions_have_verification_hints(self):
        for q in QUIZ_QUESTIONS:
            assert q[3].startswith("Verify:"), (
                f"Missing verification hint: {q[0][:30]}..."
            )


class TestEvaluateAnswer:
    def test_correct_answer_lookahead(self):
        correct, explanation, hint = evaluate_answer(
            0, "It means using future data that wouldn't be available"
        )
        assert correct is True

    def test_wrong_answer_lookahead(self):
        correct, explanation, hint = evaluate_answer(
            0, "It means looking at past data"
        )
        assert correct is False
        assert len(explanation) > 0

    def test_correct_answer_sharpe(self):
        correct, _, _ = evaluate_answer(
            1, "It depends on context and sample size"
        )
        assert correct is True

    def test_correct_answer_survivorship(self):
        correct, _, _ = evaluate_answer(
            2, "Because delisted and bankrupt companies are excluded"
        )
        assert correct is True

    def test_correct_answer_high_returns(self):
        correct, _, _ = evaluate_answer(
            3, "Check if the strategy is overfit to the training data"
        )
        assert correct is True

    def test_correct_answer_drawdown(self):
        correct, _, _ = evaluate_answer(
            4, "Maximum drawdown is the worst case scenario"
        )
        assert correct is True

    def test_invalid_question_index(self):
        correct, explanation, _ = evaluate_answer(99, "anything")
        assert correct is False
        assert "Invalid" in explanation

    def test_negative_question_index(self):
        correct, _, _ = evaluate_answer(-1, "anything")
        assert correct is False


class TestEvaluateQuiz:
    def test_all_correct(self):
        answers = (
            "Using future data that wouldn't be available",
            "It depends on context",
            "Delisted stocks are excluded",
            "Check if it's overfit",
            "Maximum drawdown is the worst case",
        )
        result = evaluate_quiz(answers)
        assert result.passed is True
        assert result.score == 5
        assert result.total == 5

    def test_all_wrong(self):
        answers = ("wrong",) * 5
        result = evaluate_quiz(answers)
        assert result.passed is False
        assert result.score == 0

    def test_passing_score(self):
        # 3 correct, 2 wrong
        answers = (
            "Using future data",
            "wrong answer",
            "Delisted stocks are excluded",
            "wrong answer",
            "Maximum drawdown matters most",
        )
        result = evaluate_quiz(answers)
        assert result.score >= PASSING_SCORE
        assert result.passed is True

    def test_wrong_number_of_answers(self):
        result = evaluate_quiz(("only one",))
        assert result.passed is False
        assert result.score == 0

    def test_feedback_for_each_question(self):
        answers = ("future",) * 5
        result = evaluate_quiz(answers)
        assert len(result.feedback) == 5


class TestQuizMarker:
    def test_quiz_marker_lifecycle(self, tmp_path, monkeypatch):
        marker = tmp_path / ".quiz-done"
        monkeypatch.setattr("lib.quiz.QUIZ_MARKER", marker)

        assert is_quiz_done() is False
        mark_quiz_done()
        assert is_quiz_done() is True
        reset_quiz()
        assert is_quiz_done() is False
