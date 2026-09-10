"""
core/watsonx_client.py
AI client wrapper — supports Groq, Grok (xAI), and IBM watsonx.ai.
Priority: Groq → Grok → IBM watsonx.ai → error message.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class WatsonxClient:
    """
    Unified AI client singleton.
    Tries Groq first, then Grok (xAI), then IBM watsonx.ai.
    Never crashes — returns a readable error string if none is configured.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._ready   = False
            cls._instance._backend = None   # "groq" | "grok" | "watsonx"
            cls._instance._error   = None
            cls._instance._init()
        return cls._instance

    # ── Initialisation ────────────────────────────────────────────────────────

    def _init(self):
        if self._try_groq():
            return
        if self._try_grok():
            return
        self._try_watsonx()

    def _try_groq(self) -> bool:
        """Attempt to set up the Groq fast-inference client."""
        api_key = os.getenv("GROQ_API_KEY", "").strip()
        if not api_key:
            return False
        try:
            from groq import Groq
            self._client  = Groq(api_key=api_key)
            self._model   = os.getenv("GROQ_MODEL", "compound-beta")
            self._ready   = True
            self._backend = "groq"
            return True
        except Exception as e:
            self._error = f"⚠️ Groq init failed: {e}"
            return False

    def _try_grok(self) -> bool:
        """Attempt to set up the Grok (xAI) OpenAI-compatible client."""
        api_key = os.getenv("GROK_API_KEY", "").strip()
        if not api_key:
            return False
        try:
            from openai import OpenAI
            self._client  = OpenAI(
                api_key  = api_key,
                base_url = os.getenv("GROK_BASE_URL", "https://api.x.ai/v1"),
            )
            self._model   = os.getenv("GROK_MODEL", "grok-3-mini")
            self._ready   = True
            self._backend = "grok"
            return True
        except Exception as e:
            self._error = f"⚠️ Grok init failed: {e}"
            return False

    def _try_watsonx(self) -> bool:
        """Attempt to set up the IBM watsonx.ai client."""
        api_key    = os.getenv("WATSONX_API_KEY", "").strip()
        project_id = os.getenv("WATSONX_PROJECT_ID", "").strip()
        if not api_key or not project_id:
            self._error = (
                "⚠️ No AI backend configured.\n"
                "Set GROK_API_KEY (recommended) **or** "
                "WATSONX_API_KEY + WATSONX_PROJECT_ID in your .env file."
            )
            return False
        try:
            from ibm_watsonx_ai import Credentials
            from ibm_watsonx_ai.foundation_models import ModelInference
            from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

            url      = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
            model_id = os.getenv("GRANITE_MODEL_ID", "ibm/granite-3-8b-instruct")

            creds = Credentials(url=url, api_key=api_key)
            self._wx_model = ModelInference(
                model_id   = model_id,
                credentials= creds,
                project_id = project_id,
                params={
                    GenParams.DECODING_METHOD:    "greedy",
                    GenParams.MAX_NEW_TOKENS:     1024,
                    GenParams.MIN_NEW_TOKENS:     10,
                    GenParams.TEMPERATURE:        0.7,
                    GenParams.REPETITION_PENALTY: 1.1,
                    GenParams.STOP_SEQUENCES:     ["<|endoftext|>"],
                },
            )
            self._ready   = True
            self._backend = "watsonx"
            return True
        except Exception as e:
            self._error = f"⚠️ Failed to connect to IBM watsonx.ai: {e}"
            return False

    # ── Public API ────────────────────────────────────────────────────────────

    @property
    def is_ready(self) -> bool:
        return self._ready

    @property
    def backend(self) -> str | None:
        """Returns 'grok', 'watsonx', or None."""
        return self._backend

    @property
    def error_message(self) -> str | None:
        return self._error

    def generate(self, prompt: str, max_tokens: int = 1024) -> str:
        """Generate text. Returns an error string if not ready."""
        if not self._ready:
            return self._error or "⚠️ AI client is not initialised."

        if self._backend in ("groq", "grok"):
            return self._generate_chat(prompt, max_tokens)
        return self._generate_watsonx(prompt, max_tokens)

    def _generate_chat(self, prompt: str, max_tokens: int) -> str:
        """Shared chat-completion path for both Groq and Grok."""
        try:
            response = self._client.chat.completions.create(
                model      = self._model,
                messages   = [{"role": "user", "content": prompt}],
                max_tokens = max_tokens,
                temperature= 0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"⚠️ {self._backend.capitalize()} generation error: {e}"

    def _generate_watsonx(self, prompt: str, max_tokens: int) -> str:
        try:
            from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
            response = self._wx_model.generate_text(
                prompt = prompt,
                params = {GenParams.MAX_NEW_TOKENS: max_tokens},
            )
            return response.strip() if response else "⚠️ Empty response from model."
        except Exception as e:
            return f"⚠️ watsonx generation error: {e}"

    @classmethod
    def reset(cls):
        """Force re-initialisation (call after updating .env at runtime)."""
        cls._instance = None
