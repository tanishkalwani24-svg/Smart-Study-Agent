# IBM Cloud Deployment Guide — Smart Study Generator Agent

## Overview
This document covers all IBM Cloud service integrations used in this project.

---

## 1. IBM watsonx.ai — Granite LLM

**Service:** IBM watsonx.ai Foundation Models  
**Model Used:** `ibm/granite-3-8b-instruct`  
**Purpose:** Powers Summary Agent, Quiz Agent, Flashcard Agent, Study Planner Agent

### Setup Steps
1. Log in to [IBM Cloud](https://cloud.ibm.com)
2. Create a **watsonx.ai** service instance
3. Go to **IAM → API Keys** → Create API Key
4. Go to **watsonx.ai Projects** → Copy Project ID
5. Add to `.env`:
```
WATSONX_API_KEY=your_ibm_cloud_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://eu-de.ml.cloud.ibm.com
GRANITE_MODEL_ID=ibm/granite-3-8b-instruct
```

---

## 2. IBM watsonx.ai — Slate Embeddings (RAG)

**Model:** `ibm/slate-125m-english-rtrvr`  
**Purpose:** Converts document chunks into vectors for semantic search (Q&A page)

### Setup
```
EMBEDDING_MODEL_ID=ibm/slate-125m-english-rtrvr
```

---

## 3. IBM Langflow — Agent Orchestration

**File:** `langflow/smart_study_flow.json`  
**Purpose:** Visual pipeline orchestrating the 4 agents

### Import Steps
1. Open IBM Langflow at your IBM Cloud instance
2. Click **Import** → Upload `langflow/smart_study_flow.json`
3. Configure watsonx.ai credentials in the flow nodes
4. Deploy and test each agent pipeline

---

## 4. Agent Files Reference

| Agent | File | IBM Service Used |
|---|---|---|
| Summary Agent | `agents/summary_agent.py` | IBM Granite via watsonx.ai |
| Quiz Agent | `agents/quiz_agent.py` | IBM Granite via watsonx.ai |
| Flashcard Agent | `agents/flashcard_agent.py` | IBM Granite via watsonx.ai |
| Study Planner Agent | `agents/planner_agent.py` | IBM Granite via watsonx.ai |
| RAG Q&A | `app/pages/05_qa.py` | IBM Slate Embeddings + ChromaDB |
| AI Client | `core/watsonx_client.py` | IBM watsonx.ai SDK |
| Vector Store | `core/vector_store.py` | IBM Slate + ChromaDB |

---

## 5. IBM Cloud SDK Dependencies

```
ibm-watsonx-ai       # Core watsonx.ai SDK
langchain-ibm        # LangChain integration for IBM embeddings
```

Install:
```bash
pip install ibm-watsonx-ai langchain-ibm
```

---

## 6. Supported IBM Granite Models

| Model ID | Use Case |
|---|---|
| `ibm/granite-3-8b-instruct` | Default — fast, accurate |
| `ibm/granite-13b-instruct-v2` | Higher quality responses |
| `ibm/granite-3-2b-instruct` | Lightweight, faster |

---

## 7. IBM Cloud Region URLs

| Region | URL |
|---|---|
| US South | `https://us-south.ml.cloud.ibm.com` |
| EU Frankfurt | `https://eu-de.ml.cloud.ibm.com` |
| Tokyo | `https://jp-tok.ml.cloud.ibm.com` |
| London | `https://eu-gb.ml.cloud.ibm.com` |

---

## 8. Architecture Diagram

```
User (Browser)
    │
    ▼
Streamlit App (app/main.py)
    │
    ├── Upload Page ──► ChromaDB (local) ◄── IBM Slate Embeddings
    ├── Summary Page ──► Summary Agent ──► IBM Granite (watsonx.ai)
    ├── Flashcard Page ──► Flashcard Agent ──► IBM Granite (watsonx.ai)
    ├── Quiz Page ──► Quiz Agent ──► IBM Granite (watsonx.ai)
    ├── Q&A Page ──► RAG Pipeline ──► IBM Slate + IBM Granite
    ├── Planner Page ──► Planner Agent ──► IBM Granite (watsonx.ai)
    └── Dashboard Page ──► Session State (local)
```

---

*Problem Statement #13 — AI-Powered Personalized Study Assistant*  
*IBM SkillsBuild / Edunet Foundation Internship Project*
