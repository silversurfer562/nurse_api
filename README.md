# nurses\_api

`nurses_api` is the FastAPI-based backend for **Nurse’s AI Assistant**, an AI-powered tool that helps nurses and allied health professionals quickly access, summarize, and adapt biomedical knowledge. By integrating large language models with trusted biomedical sources like PubMed, ClinicalTrials.gov, MedlinePlus, MyGene, and MyChem, the service generates evidence-informed drafts for patient education and professional use.

### Key Features

* **Draft Summaries & Education Materials** — Generates concise, adjustable content for patients, students, or clinicians.
* **Reading Level Control** — Customizes output for different audiences.
* **Flexible Word Counts** — Provides summaries that are clear, concise, and informative.
* **Live Data Retrieval** — Pulls the latest information from biomedical databases.
* **Safety Guardrails** — Enforces draft-only usage, requires clinician review, and avoids PHI storage.

### Tech Stack

* **FastAPI** for asynchronous Python APIs.
* **OpenAI SDK v2** for language generation and summarization.
* **Biomedical Integrations** with PubMed, ClinicalTrials.gov, MedlinePlus, MyGene, and MyChem.
* **Caching, Logging, and Provenance Layers** to improve speed, reliability, and transparency.

### Status

This project is an early-stage prototype, actively under development. Its goal is to support nurses and allied health professionals with responsibly designed AI tools, while ensuring compliance with HIPAA and other regulatory standards.
