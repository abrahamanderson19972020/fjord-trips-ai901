# ⛰️ Fjord Trips · AI travel assistant (AI-901 course project)

The project for the **AI-901 Full Course: Azure AI Fundamentals with a Real Project** on the [AI, Actually](https://www.youtube.com/@AIActuallyLab) YouTube channel.

You build **Fjord Trips**, an AI travel assistant for a fictional Norwegian travel agency, in **Microsoft Foundry**. Each module adds one feature, and together they cover every skill on the AI-901 exam:

| Feature | Azure AI skill | Module |
|---|---|---|
| Trip planner chat | Deploy a model, prompts, Foundry SDK | 5–6 |
| Trip agent with tools | Agents, file search, web search | 7–8 |
| Review insights | Text analysis (Azure Language) | 9 |
| Voice assistant (English and Hindi) | Speech recognition and synthesis | 10 |
| "Where is this?" and postcards | Vision and image generation | 11 |
| Staff document reader | Information extraction (Content Understanding) | 12 |
| Brochure-grounded answers | Retrieval (RAG) with Foundry IQ | 13 |
| Tests, safety, cost, deployment | Evaluation, guardrails, tracing, Container Apps | 14–17 |

> **All data is fictional.** Fjord Trips, its trips, prices, travellers, bookings and receipts are made up for this course.

## What you need

- An Azure subscription ([Azure for Students](https://azure.microsoft.com/free/students) or the [Azure free account](https://azure.microsoft.com/free))
- Python 3.12, [VS Code](https://code.visualstudio.com) with the Python extension, the [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) and Git

## Get started (Module 1)

```powershell
git clone https://github.com/abrahamanderson19972020/fjord-trips-ai901
cd fjord-trips-ai901

# Start from the beginning of the course, on your own branch
git switch -c my-build course-start

python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

copy .env.example .env          # macOS/Linux: cp .env.example .env
az login
```

Open `.env` and paste your Foundry **project endpoint**. You fill in the other values module by module.

Sign-in uses `DefaultAzureCredential`, which uses your `az login`. Most of the app has **no keys in the code**. The two services that use keys (Language and Speech) read them from `.env`, which is never committed.

## Follow the course module by module

The `main` branch is the **finished app**. Every module also has two Git tags:

- `mNN-start`: the code at the start of module NN
- `mNN-end`: the finished code of module NN

```powershell
git switch -c my-build course-start   # build everything yourself, from the start
git diff m08-start m08-end            # see exactly what Module 8 changes
git switch --detach m12-end           # jump to the finished code of Module 12
git switch my-build                   # back to your own work
```

On GitHub, use the **branch/tag** menu to view any module's files.

| Module | What you build | Files | Run it |
|---|---|---|---|
| 1 | Azure, Foundry project, local setup | `.env` | `az login` |
| 2 | (concepts: AI workloads) | | |
| 3 | Tokens and embeddings | `concepts/tokens.py`, `concepts/embeddings_demo.py` | `python concepts/tokens.py "Plan a trip to Bergen"` |
| 4 | Responsible AI checklist | `docs/RESPONSIBLE_AI.md` | |
| 5 | System prompt in the playground | `prompts/trip_planner.txt` | (Foundry portal) |
| 6 | Your first AI app | `app/chat.py` | `python app/chat.py` |
| 7 | `trip-agent` in the portal | `prompts/agent_instructions.txt` | (Foundry portal) |
| 8 | An app for your agent | `app/agent_client.py`, `app/app.py` | `streamlit run app/app.py` |
| 9 | Review insights | `app/language.py`, `app/pages/2_Review_insights.py` | `python app/language.py` |
| 10 | Speech | `app/audio_prompt.py`, `app/speech.py`, `app/pages/3_Voice.py` | `python app/speech.py` |
| 11 | Vision and postcards | `app/vision.py`, `app/pages/4_Photo.py`, `app/pages/5_Postcard.py` | `python app/vision.py` |
| 12 | Information extraction | `app/extract.py`, `app/pages/6_Staff_documents.py` | `python app/extract.py` |
| 13 | Knowledge base (RAG) | `docs/knowledge-base.md` | (Foundry portal) |
| 14 | Evaluation | `tests/run_eval.py` | `python tests/run_eval.py` |
| 15 | Safety and guardrails | `tests/attack_prompts.txt`, `docs/safety-log.md` | `python tests/run_eval.py` |
| 16 | Tracing and cost | `tests/cost_report.py` | `python tests/cost_report.py` |
| 17 | Deploy to Azure | `Dockerfile`, `infra/deploy.ps1` | see `infra/deploy.ps1` |

Run every command from the project folder (the folder with this README).

## Project structure

```
fjord-trips-ai901/
├── app/                 # the Fjord Trips app (Python + Streamlit)
│   ├── app.py           # home page: streamlit run app/app.py
│   └── pages/           # one page per feature
├── concepts/            # small scripts that explain AI concepts (Module 3)
├── data/                # fictional Fjord Trips data
│   ├── trip-catalog.docx / .json   # 12 trips with prices and dates
│   ├── brochure.pdf / .txt         # the official brochure 2027 (trips + policies)
│   ├── reviews.csv                 # 50 traveller reviews
│   ├── eval-set.csv                # 40 test questions with expected facts
│   ├── bookings/                   # 5 booking confirmations (PDF)
│   ├── receipts/                   # 5 receipt photos
│   └── media/                      # audio, a 60-second tour video, your own photos
├── docs/                # responsible AI checklist, safety log, knowledge base settings
├── prompts/             # system prompt and agent instructions
├── tests/               # evaluation, attack prompts, cost report
├── infra/               # deployment commands (Module 17)
├── Dockerfile
├── requirements.txt
└── .env.example         # copy to .env (never commit .env)
```

**Your own photos:** for Module 11, copy 2–3 photos from Norway into `data/media/` (for example `geiranger.jpg`). The tour video in `data/media/tour-60s.mp4` is an illustrated sample; you can replace it with your own clip.

## Clean up

Everything lives in one resource group. When you finish, delete `rg-fjordtrips` in the Azure portal (Module 19), so nothing keeps costing money. The search service from Module 13 is billed per hour, so delete it first if you keep the rest.

## Exam

AI-901 is Microsoft's Azure AI Fundamentals exam: about 40–45% AI concepts and 55–60% building AI solutions with Microsoft Foundry. Use the [official study guide](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-901) as your reference.
