# 💼 Smart Email Classifier & Rewriter (Gen-AI Powered)

A FastAPI-based Gen-AI microservice that intelligently **classifies emails** and **rewrites them in a user-specified tone**, using **LLM-powered prompt engineering** via Groq and LangChain.

This project demonstrates foundational skills in:

-  Prompt engineering
-  FastAPI development
-  LLM integration using LangChain + Groq

---

##  Features

-  Classifies incoming email into: `Work`, `Personal`, `Finance`, or `Spam`
-  Rewrites email tone to match: `professional`, `friendly`, or any custom tone
-  Prompts designed explicitly and stored externally
-  Environment-based configuration using `.env`
-  Tested via Swagger and Thunder Client

---

## 📁 Project Structure
smart-email-service/
├── main.py # FastAPI app with 2 POST routes
├── prompts/
│ ├── classify_prompt.txt # Prompt for classification
│ └── rewrite_prompt.txt # Prompt for tone rewriting
├──logger_config.log # Storing the Logs, as maintaining the record of the requests time to time.
├── .env # Sample environment file
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── Dockerfile # (Optional) Containerization setup

## 🔧 Technologies Used

- **FastAPI** – lightweight web framework for APIs
- **LangChain** – LLM abstraction & prompt integration
- **Groq API** – LLM backend with ultra-fast inference
- **DeepSeek LLM** – `deepseek-coder-7b-instruct`
- **Python 3.11+**
