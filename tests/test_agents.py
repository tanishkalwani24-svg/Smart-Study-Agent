"""
tests/test_agents.py
Unit tests for all four agents.
Run: pytest tests/ -v
"""
import pytest
from unittest.mock import MagicMock, patch


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
SAMPLE_TEXT = """
Operating Systems manage hardware and software resources on a computer.
A process is a program in execution. Threads are lightweight processes.
Deadlock occurs when processes wait for each other indefinitely.
Virtual memory allows processes to use more memory than physically available.
Paging divides memory into fixed-size pages; segmentation uses variable-size segments.
"""


# ─────────────────────────────────────────────────────────────────────────────
# Summary Agent Tests
# ─────────────────────────────────────────────────────────────────────────────
class TestSummaryAgent:
    @patch("agents.summary_agent.WatsonxClient")
    def test_summarise_returns_string(self, MockClient):
        mock_instance = MockClient.return_value
        mock_instance.generate.return_value = "## Summary\n- Processes manage CPU\n- Deadlock avoidance"

        from agents.summary_agent import SummaryAgent
        agent = SummaryAgent()
        result = agent.summarise(SAMPLE_TEXT)

        assert isinstance(result, str)
        assert len(result) > 0
        mock_instance.generate.assert_called_once()

    @patch("agents.summary_agent.WatsonxClient")
    def test_summarise_truncates_long_text(self, MockClient):
        mock_instance = MockClient.return_value
        mock_instance.generate.return_value = "Summary"

        from agents.summary_agent import SummaryAgent
        agent = SummaryAgent()
        long_text = "word " * 10000  # ~50,000 chars
        agent.summarise(long_text)

        call_args = mock_instance.generate.call_args[0][0]
        # Prompt should not exceed ~3200 chars of source text
        assert len(call_args) < 4500


# ─────────────────────────────────────────────────────────────────────────────
# Quiz Agent Tests
# ─────────────────────────────────────────────────────────────────────────────
class TestQuizAgent:
    VALID_JSON = """
    [
      {
        "question": "What is a process?",
        "options": {"A": "A file", "B": "A program in execution", "C": "A thread", "D": "A CPU"},
        "answer": "B",
        "explanation": "A process is a program currently being executed."
      }
    ]
    """

    @patch("agents.quiz_agent.WatsonxClient")
    def test_generate_returns_list(self, MockClient):
        mock_instance = MockClient.return_value
        mock_instance.generate.return_value = self.VALID_JSON

        from agents.quiz_agent import QuizAgent
        agent = QuizAgent()
        result = agent.generate_quiz(SAMPLE_TEXT, num_questions=1)

        assert isinstance(result, list)
        assert len(result) == 1
        assert "question" in result[0]
        assert "options" in result[0]

    @patch("agents.quiz_agent.WatsonxClient")
    def test_handles_invalid_json(self, MockClient):
        mock_instance = MockClient.return_value
        mock_instance.generate.return_value = "NOT JSON AT ALL"

        from agents.quiz_agent import QuizAgent
        agent = QuizAgent()
        result = agent.generate_quiz(SAMPLE_TEXT, num_questions=1)

        assert isinstance(result, list)
        assert len(result) == 1
        assert "⚠️" in result[0]["question"]


# ─────────────────────────────────────────────────────────────────────────────
# Flashcard Agent Tests
# ─────────────────────────────────────────────────────────────────────────────
class TestFlashcardAgent:
    VALID_JSON = '[{"term": "Deadlock", "definition": "A state where processes wait indefinitely."}]'

    @patch("agents.flashcard_agent.WatsonxClient")
    def test_generate_returns_list(self, MockClient):
        mock_instance = MockClient.return_value
        mock_instance.generate.return_value = self.VALID_JSON

        from agents.flashcard_agent import FlashcardAgent
        agent = FlashcardAgent()
        result = agent.generate_flashcards(SAMPLE_TEXT, num_cards=1)

        assert isinstance(result, list)
        assert result[0]["term"] == "Deadlock"

    @patch("agents.flashcard_agent.WatsonxClient")
    def test_handles_garbage_response(self, MockClient):
        mock_instance = MockClient.return_value
        mock_instance.generate.return_value = "garbage response"

        from agents.flashcard_agent import FlashcardAgent
        agent = FlashcardAgent()
        result = agent.generate_flashcards(SAMPLE_TEXT)

        assert isinstance(result, list)
        assert len(result) == 1


# ─────────────────────────────────────────────────────────────────────────────
# Study Planner Agent Tests
# ─────────────────────────────────────────────────────────────────────────────
class TestStudyPlannerAgent:
    from datetime import date, timedelta

    VALID_PLAN = """{
        "total_days": 7,
        "daily_plan": [
            {
                "day": 1, "date": "2024-12-01",
                "focus_topics": ["Operating Systems"],
                "hours_allocated": 3,
                "tasks": ["Read chapter 1", "Make notes"],
                "tip": "Start fresh!"
            }
        ],
        "milestones": [{"day": 7, "milestone": "Full revision complete"}],
        "overall_tips": ["Take breaks", "Stay hydrated"]
    }"""

    @patch("agents.planner_agent.WatsonxClient")
    def test_generate_plan_returns_dict(self, MockClient):
        from datetime import date, timedelta
        mock_instance = MockClient.return_value
        mock_instance.generate.return_value = self.VALID_PLAN

        from agents.planner_agent import StudyPlannerAgent
        agent = StudyPlannerAgent()
        result = agent.generate_plan(
            exam_date=date.today() + timedelta(days=7),
            hours_per_day=3,
            topics=["Operating Systems", "DBMS"],
        )

        assert isinstance(result, dict)
        assert "daily_plan" in result
        assert result["total_days"] == 7

    @patch("agents.planner_agent.WatsonxClient")
    def test_handles_empty_topics(self, MockClient):
        from datetime import date, timedelta
        mock_instance = MockClient.return_value
        mock_instance.generate.return_value = self.VALID_PLAN

        from agents.planner_agent import StudyPlannerAgent
        agent = StudyPlannerAgent()
        result = agent.generate_plan(
            exam_date=date.today() + timedelta(days=7),
            hours_per_day=2,
            topics=[],  # empty topics
        )
        assert isinstance(result, dict)


# ─────────────────────────────────────────────────────────────────────────────
# Document Loader Tests
# ─────────────────────────────────────────────────────────────────────────────
class TestDocumentLoader:
    def test_load_text(self):
        from core.document_loader import load_text
        result = load_text(b"Hello World")
        assert result == "Hello World"

    def test_chunk_text_basic(self):
        from core.document_loader import chunk_text
        text = "A" * 1000
        chunks = chunk_text(text, chunk_size=200, overlap=50)
        assert len(chunks) > 1
        assert all(len(c) <= 200 for c in chunks)

    def test_chunk_overlap(self):
        from core.document_loader import chunk_text
        text = "abcdefghij" * 100
        chunks = chunk_text(text, chunk_size=100, overlap=20)
        # Verify consecutive chunks share some content
        if len(chunks) >= 2:
            end_first = chunks[0][-20:]
            start_second = chunks[1][:20]
            assert end_first == start_second

    def test_unsupported_format_raises(self):
        from core.document_loader import load_document
        with pytest.raises(ValueError):
            load_document("file.docx", b"binary data")
