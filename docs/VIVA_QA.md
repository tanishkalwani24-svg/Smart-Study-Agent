# Viva Questions & Answers — Smart Study Generator Agent

---

## Section 1: Project Basics

**Q1. What is the Smart Study Generator Agent?**
A: It is an AI-powered study assistant that allows students to upload PDFs, notes, or images and receive personalized study help — including summaries, flashcards, MCQ quizzes, Q&A via RAG, and a study plan — all powered by IBM Granite on IBM watsonx.ai, orchestrated through IBM Langflow, with a Streamlit dashboard.

---

**Q2. What problem does this project solve?**
A: Students waste time manually creating summaries, flashcards, and quiz questions from large textbooks. They also lack personalized study schedules and have no visibility into their weak areas. Our agent automates all of this using IBM Granite, making studying more efficient and data-driven.

---

**Q3. Why did you choose IBM Granite over GPT or other models?**
A: IBM Granite is an enterprise-grade, responsible AI model built for transparency and trust. It is specifically designed for instruction-following tasks, has a clear training data lineage (unlike closed-source models), and integrates natively with IBM watsonx.ai — which provides production-level reliability, monitoring, and governance that GPT-based models through OpenAI don't offer in an enterprise context.

---

## Section 2: Architecture & Technology

**Q4. Explain the system architecture.**
A: The system follows a pipeline:
1. User uploads a file via Streamlit → DocumentLoader extracts text (PyMuPDF for PDFs, Tesseract OCR for images).
2. Text is chunked into 512-character overlapping segments.
3. Chunks are embedded using IBM Slate and stored in ChromaDB (vector store).
4. Four IBM Langflow-orchestrated agents (Summary, Quiz, Flashcard, Planner) process the text via IBM Granite.
5. For Q&A, a RAG pipeline retrieves relevant chunks from ChromaDB and passes them to Granite.
6. All results render in the Streamlit multi-page dashboard.

---

**Q5. What is RAG? Why did you use it?**
A: RAG stands for Retrieval-Augmented Generation. Instead of relying solely on the LLM's training data, RAG retrieves relevant passages from the student's actual uploaded document and provides them as context to the model. This ensures answers are grounded in the specific textbook being studied, eliminating hallucinations and making responses accurate to the student's course material.

---

**Q6. What is ChromaDB and why did you choose it?**
A: ChromaDB is an open-source, in-process vector database. We chose it because it requires zero server setup, integrates natively with Python, supports persistent and in-memory modes, and has excellent LangChain integration. For a college project with a local deployment, it's the optimal choice — production deployments could swap it for IBM Cloud Object Storage or Milvus.

---

**Q7. What is IBM Langflow?**
A: IBM Langflow is a visual, low-code orchestration platform for building AI pipelines using a node-and-edge graph interface. We use it to define the multi-agent workflow — each agent is a node, and the data flows between nodes as edges. The workflow is exported as a JSON file that can be re-imported and modified visually.

---

**Q8. Explain the document chunking strategy.**
A: We split documents into 512-character chunks with 64-character overlaps. The overlap ensures that concepts spanning a chunk boundary aren't split across two isolated chunks, preserving context for the embedding model. This is critical for RAG quality — without overlap, a sentence split at a chunk boundary would lose half its context.

---

## Section 3: AI Agents

**Q9. How many agents are in your system? Explain each.**
A:
1. **Summary Agent**: Takes raw text, sends it to Granite with a structured prompt requesting bullet-point summaries in simple language. Output is displayed directly in the Streamlit UI.
2. **Quiz Generator Agent**: Takes text and desired question count, prompts Granite to generate MCQs in JSON format with options, correct answers, and explanations.
3. **Flashcard Agent**: Takes text and card count, prompts Granite to extract key term-definition pairs in JSON format.
4. **Study Planner Agent**: Takes exam date, daily hours, topics, and weak areas, then generates a full day-by-day JSON study schedule with milestones and tips.

---

**Q10. How do you handle cases where the model returns malformed JSON?**
A: All agents implement a two-layer fallback parser:
1. First, we try `json.loads()` directly on the response.
2. If that fails, we use `re.search(r'\[.*\]', raw, re.DOTALL)` to find a JSON block within noisy output.
3. If both fail, we return a graceful error dict/list so the UI can display a helpful message instead of crashing.

---

**Q11. What is prompt engineering? Give an example from your project.**
A: Prompt engineering is the practice of crafting precise instructions that guide an LLM to produce the desired output format and content. In our Quiz Agent, the prompt specifies: the exact output format (JSON array with `question`, `options`, `answer`, `explanation` keys), the difficulty distribution (30% easy, 50% medium, 20% hard), and ends with "Return ONLY valid JSON. No extra commentary." — this last instruction significantly reduces parsing failures.

---

## Section 4: Frontend & UX

**Q12. Why Streamlit for the frontend?**
A: Streamlit allows rapid, Python-native web app development with zero HTML/CSS/JavaScript knowledge required. It supports multi-page apps, session state management, file uploaders, chat interfaces, and Plotly charts — everything our project needs. For a college project timeline, it's the fastest path from code to a professional-looking dashboard.

---

**Q13. How does the progress dashboard work?**
A: The dashboard reads from Streamlit's `session_state` which stores:
- `completed`: list of topics/docs that have been summarized
- `weak_areas`: docs where the student scored below 50% on quizzes (auto-flagged)
- `milestones`: milestones extracted from the AI-generated study plan
These are visualized using Plotly — a donut chart for topic completion percentage and a bar chart for activity counts.

---

**Q14. How do you persist data between page reloads in Streamlit?**
A: We use Streamlit's `session_state` dictionary, initialized in `core/session_state.py`'s `init_session()` function. Every page calls this function on load. Session state persists for the duration of the browser session. For persistent storage across sessions, we could add SQLite or IBM Cloudant — noted as a future enhancement.

---

## Section 5: IBM watsonx.ai

**Q15. How do you authenticate with IBM watsonx.ai?**
A: We use IBM Cloud IAM authentication. The `WatsonxClient` class in `core/watsonx_client.py` reads `WATSONX_API_KEY`, `WATSONX_PROJECT_ID`, and `WATSONX_URL` from the `.env` file. These are passed to the `ibm_watsonx_ai.Credentials` object, which handles token exchange automatically.

---

**Q16. What parameters did you use for Granite inference and why?**
A:
- `DECODING_METHOD: greedy` — deterministic output, important for structured JSON generation
- `MAX_NEW_TOKENS: 1024` — sufficient for summaries and quizzes without excessive cost
- `TEMPERATURE: 0.7` — slight creativity for tips and study plans while remaining coherent
- `REPETITION_PENALTY: 1.1` — prevents the model from repeating phrases in summaries

---

**Q17. What is the IBM Slate model used for?**
A: IBM Slate (`ibm/slate-125m-english-rtrvr`) is IBM's retrieval-optimized embedding model. We use it to convert text chunks and user queries into dense vector representations. Slate is specifically trained for retrieval tasks, meaning it places semantically similar texts close together in vector space — this improves RAG accuracy compared to general-purpose embeddings.

---

## Section 6: Advanced Topics

**Q18. What is the difference between in-context learning and fine-tuning? Which does your project use?**
A: Fine-tuning updates the model weights using task-specific training data — expensive and complex. In-context learning (prompt engineering + RAG) provides the model with task instructions and relevant context at inference time, without touching the model weights. Our project uses in-context learning exclusively — the agent behavior is defined entirely through prompt templates, which is faster to iterate on and requires no GPU training infrastructure.

---

**Q19. What is a vector embedding?**
A: A vector embedding is a numerical representation of text as a high-dimensional vector (e.g., 768 dimensions) where semantically similar texts have vectors that are geometrically close (measured by cosine similarity). The IBM Slate model converts each 512-character chunk into such a vector. When a student asks a question, the query is also embedded, and ChromaDB finds the chunks with the highest cosine similarity — these are the most relevant passages to include as context.

---

**Q20. How would you scale this project for 10,000 concurrent students?**
A:
1. Replace ChromaDB (in-memory) with a distributed vector database like Milvus or IBM Db2 AI.
2. Deploy Streamlit on IBM Code Engine (container-based, auto-scaling).
3. Use IBM watsonx.ai's batch inference API for non-real-time requests (e.g., generating study plans overnight).
4. Add Redis for session caching instead of Streamlit session_state.
5. Implement a job queue (Celery + RabbitMQ) for long-running agent tasks.
6. Use IBM Cloud Object Storage for document persistence.

---

**Q21. What are the ethical considerations of this AI system?**
A: 
- **Accuracy**: Quiz answers generated by AI may occasionally be wrong — we mitigate this with explanations that students can verify.
- **Privacy**: Student documents (potentially containing personal notes) are processed through IBM watsonx.ai — IBM's data governance policies protect this data.
- **Dependency**: Over-reliance on AI-generated summaries could reduce deep reading skills — the system is designed as a complement, not a replacement, for genuine study.
- **Fairness**: IBM Granite's transparent training data lineage reduces bias compared to models with undisclosed training data.

---

**Q22. Can this system handle non-English documents?**
A: Partially. PyMuPDF and Tesseract support multilingual text extraction. However, IBM Granite 13B Instruct is primarily English-optimized. For multilingual support, we would use IBM's multilingual Granite models or add a translation layer (IBM Watson Language Translator) before sending text to the agent prompts. This is listed in our future scope.

---

**Q23. What design patterns did you use?**
A:
- **Singleton Pattern**: `WatsonxClient` uses `__new__` to ensure only one model instance is created, avoiding redundant credential initialization.
- **Facade Pattern**: Each agent class exposes a simple interface (`summarise()`, `generate_quiz()`, etc.) hiding the complexity of prompt construction and LLM calls.
- **Strategy Pattern**: `DocumentLoader` dispatches to different loading functions based on file extension — adding a new format requires only adding one `elif` branch.

---

**Q24. What is the time complexity of your chunking algorithm?**
A: O(n) where n is the length of the input text. Each character is visited a constant number of times as we slide the window. The overlap doesn't change the asymptotic complexity since the overlap fraction (64/512 ≈ 12.5%) is a constant factor.

---

**Q25. If watsonx.ai is down, how does your app behave?**
A: The `WatsonxClient.generate()` method will raise an exception from the IBM SDK. In the Streamlit pages, this exception propagates to the `with st.spinner()` block. Currently, it surfaces as an error message via `st.error()`. A production improvement would be a circuit-breaker pattern that retries with exponential backoff and a fallback message advising the user to try again later.
