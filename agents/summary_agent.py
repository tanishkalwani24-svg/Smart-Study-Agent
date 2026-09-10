"""
agents/summary_agent.py
Summary Agent — generates chapter-level summaries in simple language.
Uses IBM Granite via watsonx.ai.
"""
from core.watsonx_client import WatsonxClient

SUMMARY_PROMPT = """\
You are an expert academic tutor. Your task is to summarise the following study material
in simple, easy-to-understand language suitable for a college student.

Guidelines:
- Write in clear, concise bullet points under logical headings.
- Highlight the 5 most important concepts.
- Use simple vocabulary — avoid jargon unless necessary (and explain it when used).
- Keep the total summary under 400 words.

--- STUDY MATERIAL START ---
{text}
--- STUDY MATERIAL END ---

Provide a well-structured summary below:
"""


class SummaryAgent:
    """Generates chapter summaries from raw document text."""

    def __init__(self):
        self._llm = WatsonxClient()

    def summarise(self, text: str) -> str:
        """
        Generate a structured summary of the provided text.

        Args:
            text: Raw extracted document text (max ~3000 chars for context).

        Returns:
            Summary string.
        """
        # Truncate to avoid context overflow
        truncated = text[:3000]
        prompt = SUMMARY_PROMPT.format(text=truncated)
        return self._llm.generate(prompt, max_tokens=600)
