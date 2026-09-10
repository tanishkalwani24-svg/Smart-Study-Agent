# 📊 PPT Content — Smart Study Generator Agent
## 12 Slides with Speaker Notes

---

## Slide 1 — Title Slide
**Title:** Smart Study Generator Agent
**Subtitle:** AI-Powered Personalized Study Assistant using IBM watsonx.ai + IBM Granite
**Footer:** Problem Statement #13 | IBM Langflow | Streamlit Dashboard

### Speaker Notes:
Good morning/afternoon everyone. Today we present our project — the Smart Study Generator Agent, an AI-powered study assistant built on IBM's enterprise-grade AI platform, watsonx.ai, using the IBM Granite language model and orchestrated through IBM Langflow. This project addresses a real problem faced by millions of college students — the lack of personalized, intelligent study support.

---

## Slide 2 — Problem Statement
**Title:** The Problem

**Content:**
- 📚 Students struggle to extract key insights from large PDFs and textbooks
- ❓ No instant access to quizzes or self-assessment tools
- 🗓️ Poor study planning leads to last-minute cramming
- 📉 No visibility into weak areas or progress
- 🤖 Existing tools are generic — not personalized

**Visual:** Split image — stressed student vs. confident student with AI assistant

### Speaker Notes:
Every student faces this challenge: you have a 500-page textbook, an exam in 2 weeks, and no idea where to begin. Traditional tools like static PDFs or YouTube videos don't adapt to your pace or identify your weak areas. Our solution changes this fundamentally using multi-agent AI.

---

## Slide 3 — Solution Overview
**Title:** Our Solution — Smart Study Generator Agent

**Content:**
- Upload any document: PDF, image, or notes
- AI automatically generates: Summaries, Flashcards, Quizzes, Study Plans
- Ask questions in natural language (RAG-powered)
- Personalized study schedule based on exam date
- Live progress dashboard

**Visual:** Circular flow diagram: Upload → Process → Generate → Learn → Track

### Speaker Notes:
Our solution is a complete AI study companion. Students simply upload their material, and four specialized AI agents — each powered by IBM Granite — handle summarization, quiz generation, flashcard creation, and study planning. A RAG pipeline lets students ask natural language questions answered directly from their own documents.

---

## Slide 4 — IBM Tech Stack
**Title:** Technology Stack

**Content (Table):**
| Component | Technology |
|---|---|
| AI Model | IBM Granite 13B Instruct |
| AI Platform | IBM watsonx.ai |
| Orchestration | IBM Langflow |
| Embeddings | IBM Slate 125M |
| Vector DB | ChromaDB |
| Frontend | Streamlit |
| PDF Parsing | PyMuPDF |
| OCR | Tesseract |

**Visual:** IBM watsonx logo + tech stack icons

### Speaker Notes:
The entire AI backbone runs on IBM's enterprise cloud. IBM Granite is a family of foundation models specifically designed for enterprise use — it's transparent, responsible, and optimized for instruction-following tasks like summarization and quiz generation. IBM Langflow handles the visual workflow orchestration, making the multi-agent pipeline easy to modify without rewriting code.

---

## Slide 5 — System Architecture
**Title:** System Architecture

**Content (Architecture diagram description):**
```
[User Browser / Streamlit UI]
         │
         ▼
[Document Upload Module]
    PDF / Image / Text
         │
         ▼
[Document Loader & Chunker]
    PyMuPDF + Tesseract OCR
         │
    ┌────┴────┐
    ▼         ▼
[ChromaDB    [IBM Granite LLM]
 Vector       via watsonx.ai
 Store]           │
    │         ┌───┼───────────────┐
    └──RAG───►│   │               │
              ▼   ▼               ▼
         [Summary] [Quiz]  [Flashcard]
          Agent    Agent    Agent
                               │
                        [Planner Agent]
                               │
                        [Streamlit Dashboard]
```

### Speaker Notes:
The architecture follows a clean pipeline. Documents enter through the upload module, get parsed and chunked, then are indexed into ChromaDB for RAG. Simultaneously, the text is passed to four specialized agents running on IBM Granite via watsonx.ai. All outputs surface in the Streamlit dashboard. The IBM Langflow JSON defines the entire orchestration graph.

---

## Slide 6 — Multi-Agent Design
**Title:** Four Specialized AI Agents

**Content:**
🔵 **Summary Agent**
- Input: Raw text → Output: Bullet-point chapter summary
- Prompt: Simple language, key concepts, under 400 words

🟣 **Quiz Generator Agent**
- Input: Text + question count → Output: JSON MCQs with answers
- Prompt: Varied difficulty (30% easy / 50% medium / 20% hard)

🟢 **Flashcard Agent**
- Input: Text + card count → Output: JSON term-definition pairs
- Prompt: 1-2 sentence definitions, student-friendly

🟠 **Study Planner Agent**
- Input: Exam date, hours/day, topics → Output: Day-by-day JSON schedule
- Prompt: Milestone-based, accounts for weak areas

### Speaker Notes:
Each agent has a single, focused responsibility. This separation of concerns is a core software engineering principle — it makes the system modular, testable, and easy to extend. All four agents share the same IBM Granite model but receive carefully engineered prompts that steer the model toward their specific output format.

---

## Slide 7 — RAG Pipeline
**Title:** RAG — Retrieval-Augmented Generation

**Content:**
**How RAG Works:**
1. Student uploads PDF → text extracted → split into 512-char chunks
2. Chunks embedded using IBM Slate model → stored in ChromaDB
3. Student asks a question → query embedded → top-4 similar chunks retrieved
4. Chunks + question sent to IBM Granite → accurate, grounded answer

**Why RAG?**
- Answers are grounded in the actual uploaded document
- No hallucinations from general training data
- Works with ANY subject, ANY textbook

**Visual:** RAG pipeline flowchart

### Speaker Notes:
RAG is what makes the Q&A feature genuinely useful. Without RAG, the LLM would answer from its training data, which may not match the student's specific textbook. With RAG, every answer is traced back to the exact uploaded material. This is enterprise-grade, responsible AI in action.

---

## Slide 8 — Streamlit Dashboard
**Title:** Live Demo — Streamlit Frontend

**Content (screenshots/description):**
- 📤 **Upload Page** — Drag-and-drop multi-file upload with processing status
- 📝 **Summary Page** — One-click summary generation with regenerate option
- 🃏 **Flashcard Page** — Interactive flip-card navigator with all-cards table
- ❓ **Quiz Page** — MCQ quiz with real-time scoring and answer explanations
- 💬 **Q&A Page** — Chat interface with source passage citations
- 📅 **Planner Page** — Day-by-day expandable schedule with milestones
- 📊 **Dashboard** — Donut chart (topic completion) + activity bar chart

### Speaker Notes:
The Streamlit frontend provides a clean, professional interface with zero setup for the student. Each feature lives on its own page, accessible through a persistent sidebar. The dashboard gives a bird's-eye view of progress, showing completed topics, weak areas flagged by low quiz scores, and study milestones from the AI-generated plan.

---

## Slide 9 — Key Features Demo
**Title:** Feature Highlights

**Content:**
✅ **Smart Chunking** — 512-char chunks with 64-char overlap for perfect context preservation

✅ **JSON-Structured Outputs** — All agents return structured JSON, enabling rich UI rendering

✅ **Automatic Weak-Area Detection** — Quiz scores below 50% auto-flag topics as weak

✅ **Session State Caching** — Generated content cached in Streamlit session to avoid redundant API calls

✅ **Graceful Error Handling** — Regex fallback JSON parsing for noisy LLM responses

✅ **Multi-Format Support** — PDF, PNG, JPG, TXT, Markdown all supported out of the box

### Speaker Notes:
These engineering decisions make the project production-ready, not just a demo. The caching system prevents unnecessary watsonx API calls, reducing cost. The automatic weak-area detection creates a feedback loop between quiz performance and study planning — this is what makes it truly personalized.

---

## Slide 10 — Testing & Validation
**Title:** Testing Strategy

**Content:**
**Unit Tests (pytest):**
- SummaryAgent: tests output type, text truncation
- QuizAgent: tests JSON parsing, invalid-response fallback
- FlashcardAgent: tests card structure, garbage-response handling
- StudyPlannerAgent: tests plan structure, empty topic handling
- DocumentLoader: tests chunking logic, unsupported format rejection

**Testing Commands:**
```bash
pytest tests/ -v
# Expected: 12 passed in <2s (with mocked watsonx calls)
```

**Sample Test Input:** Operating Systems Chapter — Process Management (65 lines)

### Speaker Notes:
All tests mock the watsonx.ai calls so they run offline without credentials. This is industry best practice — unit tests should be fast and deterministic. The mocks verify that the agent logic (prompt construction, JSON parsing, error handling) works correctly independent of the LLM backend.

---

## Slide 11 — IBM watsonx Setup
**Title:** Setting Up IBM watsonx.ai

**Step-by-Step:**
1. Create IBM Cloud account → ibm.com/cloud
2. Provision watsonx.ai service instance
3. Create a Project in watsonx.ai Studio
4. Generate API key from IBM Cloud IAM
5. Copy Project ID from watsonx.ai project settings
6. Select model: `ibm/granite-13b-instruct-v2`
7. Add credentials to `.env` file
8. Install: `pip install ibm-watsonx-ai`

**Granite Model Options:**
| Model | Use Case |
|---|---|
| granite-13b-instruct-v2 | Default — best balance |
| granite-8b-code-instruct | Code-heavy content |
| granite-3-8b-instruct | Faster, lighter tasks |

### Speaker Notes:
Setting up IBM watsonx.ai takes about 10 minutes. The IBM Cloud free tier provides sufficient quota for academic projects. The Granite model we chose — granite-13b-instruct-v2 — is IBM's flagship instruction-following model, optimized for tasks like summarization, question generation, and structured output, which are exactly what our agents need.

---

## Slide 12 — Conclusion & Future Scope
**Title:** Conclusion & Future Scope

**What We Built:**
- ✅ Complete multi-agent AI study assistant
- ✅ 4 specialized IBM Granite-powered agents
- ✅ RAG-based Q&A grounded in uploaded documents
- ✅ Personalized study planner with milestone tracking
- ✅ Professional Streamlit dashboard with progress analytics

**Future Enhancements:**
- 🌐 Multi-language support (Hindi, regional languages)
- 🎙️ Voice-based Q&A using IBM Watson Speech-to-Text
- 📱 Mobile app using React Native
- 🤝 Collaborative study groups with shared flashcard decks
- 📊 Learning analytics with IBM OpenPages integration
- 🏆 Gamification — streaks, badges, leaderboards

**Closing:** "IBM Granite doesn't just answer questions — it helps students ask better ones."

### Speaker Notes:
This project demonstrates how IBM's enterprise AI stack can solve real, everyday problems for students. The modular architecture means each feature can be independently extended or replaced. Our future roadmap includes voice input, mobile deployment, and deeper analytics — all feasible given the IBM ecosystem. Thank you for your time and attention. We welcome your questions.
