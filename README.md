# 🎓 Smart Study Generator Agent
### IBM watsonx.ai + IBM Granite + IBM Langflow

> Problem Statement No. 13 — AI-Powered Personalized Study Assistant

---

## 📌 Overview

Smart Study Generator Agent is a college-level AI project that allows students to upload PDFs, notes, or images and receive personalized study assistance powered by IBM Granite models running on IBM watsonx.ai, orchestrated through IBM Langflow, with a beautiful Streamlit dashboard.

---

## 🚀 Quick Start

```bash
# 1. Clone / navigate to project
cd smart_study_agent

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Fill in your IBM watsonx credentials in .env

# 5. Run the application
streamlit run app/main.py
```

---

## 📁 Project Structure

```
smart_study_agent/
├── app/
│   ├── main.py                  # Streamlit entry point
│   ├── pages/
│   │   ├── 01_upload.py         # Document upload page
│   │   ├── 02_summary.py        # Chapter summaries
│   │   ├── 03_flashcards.py     # Flashcard viewer
│   │   ├── 04_quiz.py           # MCQ quiz page
│   │   ├── 05_qa.py             # Q&A with RAG
│   │   ├── 06_planner.py        # Study planner
│   │   └── 07_dashboard.py      # Progress dashboard
│   └── components/
│       ├── sidebar.py           # Shared sidebar
│       └── styles.py            # CSS styles
├── agents/
│   ├── summary_agent.py         # Summary Agent
│   ├── quiz_agent.py            # Quiz Generator Agent
│   ├── flashcard_agent.py       # Flashcard Agent
│   └── planner_agent.py         # Study Planner Agent
├── core/
│   ├── watsonx_client.py        # IBM watsonx.ai client
│   ├── vector_store.py          # ChromaDB RAG setup
│   ├── document_loader.py       # PDF/Image loader
│   └── session_state.py         # Streamlit session helpers
├── langflow/
│   └── smart_study_flow.json    # Langflow export
├── prompts/
│   ├── summary_prompt.txt
│   ├── quiz_prompt.txt
│   ├── flashcard_prompt.txt
│   └── planner_prompt.txt
├── tests/
│   ├── test_agents.py
│   └── sample_data/
│       └── sample_chapter.txt
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `WATSONX_API_KEY` | IBM Cloud API key |
| `WATSONX_PROJECT_ID` | watsonx.ai project ID |
| `WATSONX_URL` | watsonx.ai service URL |
| `GRANITE_MODEL_ID` | e.g. `ibm/granite-13b-instruct-v2` |

---

## 🛠️ Tech Stack

- **AI Models**: IBM Granite (via watsonx.ai)
- **Orchestration**: IBM Langflow
- **RAG**: ChromaDB + ibm-watsonx-ai embeddings
- **Frontend**: Streamlit
- **PDF Parsing**: PyMuPDF (fitz)
- **Image OCR**: Tesseract / pytesseract
- **Vector DB**: ChromaDB (local)

---

## 📊 Agents

| Agent | Role |
|---|---|
| Summary Agent | Generates chapter summaries in simple language |
| Quiz Agent | Creates MCQ quizzes with answer keys |
| Flashcard Agent | Produces term-definition flashcard pairs |
| Study Planner Agent | Builds personalized study schedule |

---

## 📄 License
MIT License — Free for academic use.
