"""
agents/planner_agent.py
Study Planner Agent — creates a personalised daily study schedule
based on exam date, available hours, and topic list.
"""
import json
import re
from datetime import date
from core.watsonx_client import WatsonxClient

PLANNER_PROMPT = """\
You are an expert academic coach. Create a detailed, personalised study plan for a student.

Student Profile:
- Exam Date: {exam_date}
- Days Available: {days_available} days
- Study Hours Per Day: {hours_per_day} hours
- Topics to Cover: {topics}
- Weak Areas (needs more time): {weak_areas}

Guidelines:
- Distribute topics proportionally across available days.
- Allocate extra time (25% more) to weak areas.
- Include one revision/mock test day before the exam.
- Add short breaks every 2 hours.
- Keep the last 2 days for full revision only.

Output FORMAT (strict JSON):
{{
  "total_days": <int>,
  "daily_plan": [
    {{
      "day": 1,
      "date": "YYYY-MM-DD",
      "focus_topics": ["Topic A", "Topic B"],
      "hours_allocated": <float>,
      "tasks": ["Task description 1", "Task description 2"],
      "tip": "Motivational or strategic tip for this day."
    }},
    ...
  ],
  "milestones": [
    {{"day": <int>, "milestone": "Description"}},
    ...
  ],
  "overall_tips": ["Tip 1", "Tip 2", "Tip 3"]
}}

Return ONLY valid JSON.
"""


class StudyPlannerAgent:
    """Generates personalised study schedules."""

    def __init__(self):
        self._llm = WatsonxClient()

    def generate_plan(
        self,
        exam_date: date,
        hours_per_day: float,
        topics: list[str],
        weak_areas: list[str] | None = None,
    ) -> dict:
        """
        Build a day-by-day study plan.

        Args:
            exam_date: The exam date.
            hours_per_day: Study hours available per day.
            topics: List of topics to cover.
            weak_areas: Topics that need extra attention.

        Returns:
            Structured plan dict.
        """
        today = date.today()
        days_available = max((exam_date - today).days, 1)
        weak = weak_areas or []

        prompt = PLANNER_PROMPT.format(
            exam_date=exam_date.strftime("%d %B %Y"),
            days_available=days_available,
            hours_per_day=hours_per_day,
            topics=", ".join(topics) if topics else "General review",
            weak_areas=", ".join(weak) if weak else "None specified",
        )
        raw = self._llm.generate(prompt, max_tokens=1200)
        return self._parse_json(raw)

    @staticmethod
    def _parse_json(raw: str) -> dict:
        """Extract JSON object from LLM response."""
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        return {"error": "Could not parse plan.", "raw": raw[:500]}
