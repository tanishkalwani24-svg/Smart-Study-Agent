"""
agents/quiz_agent.py
Quiz Generator Agent — creates MCQ quizzes with answer keys.
"""
import json
import re
from core.watsonx_client import WatsonxClient

QUIZ_PROMPT = """\
You are an expert exam question setter. Based on the study material below,
generate exactly {num_questions} multiple-choice questions (MCQs).

Rules:
- Each question must have 4 options labelled A, B, C, D.
- Clearly mark the correct answer.
- Questions should test understanding, not just memory.
- Vary difficulty: 30% easy, 50% medium, 20% hard.

Output FORMAT (strict JSON array):
[
  {{
    "question": "Question text here?",
    "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
    "answer": "A",
    "explanation": "Brief explanation of the correct answer."
  }},
  ...
]

--- STUDY MATERIAL ---
{text}
--- END MATERIAL ---

Return ONLY valid JSON. No extra commentary.
"""


class QuizAgent:
    """Generates MCQ quizzes from document text."""

    def __init__(self):
        self._llm = WatsonxClient()

    def generate_quiz(self, text: str, num_questions: int = 5) -> list[dict]:
        """
        Generate MCQ questions from text.

        Args:
            text: Source material text.
            num_questions: Number of MCQs to generate (default 5).

        Returns:
            List of question dicts with keys: question, options, answer, explanation.
        """
        truncated = text[:3000]
        prompt = QUIZ_PROMPT.format(text=truncated, num_questions=num_questions)
        raw = self._llm.generate(prompt, max_tokens=1024)

        # Extract JSON array from response
        return self._parse_json(raw)

    @staticmethod
    def _parse_json(raw: str) -> list[dict]:
        """Attempt to extract a JSON array from a potentially noisy LLM response."""
        # Try direct parse first
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

        # Try to find a JSON block
        match = re.search(r"\[.*\]", raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        # Return an empty list with an error marker so the UI can handle it
        return [
            {
                "question": "⚠️ Could not parse quiz. Please retry.",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "answer": "A",
                "explanation": raw[:300],
            }
        ]
