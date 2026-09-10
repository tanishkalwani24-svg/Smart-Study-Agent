"""
agents/flashcard_agent.py
Flashcard Agent — creates term-definition pairs from document text.
"""
import json
import re
from core.watsonx_client import WatsonxClient

FLASHCARD_PROMPT = """\
You are a study assistant. Extract key terms and their definitions from the material below
to create {num_cards} study flashcards.

Rules:
- Each flashcard: one key term on the front, clear definition on the back.
- Terms should cover the most important concepts.
- Definitions must be concise (1-2 sentences).
- Use simple, student-friendly language.

Output FORMAT (strict JSON array):
[
  {{
    "term": "Term or concept",
    "definition": "Clear, simple definition in 1-2 sentences."
  }},
  ...
]

--- STUDY MATERIAL ---
{text}
--- END MATERIAL ---

Return ONLY valid JSON. No extra text.
"""


class FlashcardAgent:
    """Generates flashcard pairs from document text."""

    def __init__(self):
        self._llm = WatsonxClient()

    def generate_flashcards(self, text: str, num_cards: int = 10) -> list[dict]:
        """
        Generate flashcard term-definition pairs.

        Args:
            text: Source material text.
            num_cards: Number of flashcards to generate (default 10).

        Returns:
            List of dicts with keys: term, definition.
        """
        truncated = text[:3000]
        prompt = FLASHCARD_PROMPT.format(text=truncated, num_cards=num_cards)
        raw = self._llm.generate(prompt, max_tokens=800)
        return self._parse_json(raw)

    @staticmethod
    def _parse_json(raw: str) -> list[dict]:
        """Extract JSON array from LLM response."""
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

        match = re.search(r"\[.*\]", raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        return [{"term": "⚠️ Parse error", "definition": raw[:200]}]
