# Nurse's AI Assistant API

FastAPI backend for Nurse's AI Assistant, providing evidence-informed summaries, patient education drafts, and live biomedical data integration with LLMs.

## 🚀 Features

- **Patient Education Materials**: Generate draft educational content with multiple reading levels (elementary through professional)
- **Clinical Summaries**: Create clinical summaries from patient data with flexible word counts
- **Multiple Reading Levels**: Content adapted for different literacy levels
- **Safety Guardrails**: Built-in compliance checking and content filtering
- **Draft-Only Outputs**: All content requires clinician review before use
- **Evidence-Based**: Integration structure for biomedical literature sources
- **HIPAA Considerations**: Privacy protection and PII detection
- **Professional Standards**: Appropriate medical disclaimers and review requirements

## 📋 Requirements

- Python 3.8+
- FastAPI 0.104.1
- Pydantic 2.5.0
- Uvicorn 0.24.0

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/silversurfer562/nurse_api.git
cd nurse_api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔧 Usage

### API Documentation
Once running, access the interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### Generate Patient Education Material
```bash
curl -X POST "http://localhost:8000/api/v1/patient-education" \
     -H "Content-Type: application/json" \
     -d '{
       "topic": "diabetes management",
       "reading_level": "high-school",
       "word_count": 300,
       "include_sources": true
     }'
```

### Generate Clinical Summary
```bash
curl -X POST "http://localhost:8000/api/v1/clinical-summary" \
     -H "Content-Type: application/json" \
     -d '{
       "patient_data": "Patient presents with chest pain and shortness of breath. History of hypertension.",
       "summary_type": "admission",
       "word_count": 400,
       "include_recommendations": true
     }'
```

## 📊 Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

Run with coverage:
```bash
python -m pytest tests/ --cov=app
```

## 🏗️ Architecture

```
nurse_api/
├── main.py                 # FastAPI application entry point
├── app/
│   ├── config.py          # Configuration settings
│   ├── models/            # Pydantic request/response models
│   │   ├── requests.py
│   │   └── responses.py
│   ├── routers/           # API route handlers
│   │   ├── health.py
│   │   ├── patient_education.py
│   │   └── clinical_summaries.py
│   └── services/          # Business logic services
│       ├── content_generator.py
│       └── compliance_checker.py
├── tests/                 # Test files
└── requirements.txt       # Python dependencies
```

## 🔒 Safety & Compliance

### Content Safety
- Inappropriate medical claims detection
- Definitive medical advice prevention
- Content filtering for sensitive topics

### Privacy Protection
- PII pattern detection
- HIPAA compliance considerations
- Patient identifier screening

### Professional Standards
- Mandatory clinician review flags
- Appropriate medical disclaimers
- Clinical hedging language validation

## ⚙️ Configuration

Environment variables (optional .env file):

```bash
# LLM Configuration
LLM_API_KEY=your_llm_api_key_here
LLM_MODEL=gpt-3.5-turbo

# Content Settings
MAX_CONTENT_LENGTH=2000
ENABLE_CONTENT_FILTERING=true
REQUIRE_CLINICIAN_REVIEW=true

# Data Sources
PUBMED_API_KEY=your_pubmed_api_key_here
ENABLE_LIVE_DATA=false
```

## 🚨 Important Disclaimers

⚠️ **CRITICAL**: This API generates DRAFT content only. All outputs must be reviewed and approved by qualified healthcare professionals before patient use.

⚠️ **NO MEDICAL ADVICE**: This system does not provide medical advice, diagnosis, or treatment recommendations.

⚠️ **COMPLIANCE REQUIRED**: Users must ensure compliance with HIPAA, medical regulations, and institutional policies.

⚠️ **PROFESSIONAL OVERSIGHT**: Clinical decisions should always involve qualified healthcare professionals and direct patient assessment.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📖 API Documentation

For detailed API documentation, see [API_DOCS.md](API_DOCS.md).

## 📄 License

This project is intended for educational and development purposes. Ensure compliance with all applicable healthcare regulations before production use.

## 🔮 Future Enhancements

- Live biomedical database integration (PubMed, Cochrane, etc.)
- Advanced LLM model support
- Multi-language content generation
- EHR system integration
- Enhanced clinical decision support
- Advanced analytics and reporting
- Real-time content collaboration features

## 📞 Support

For questions, issues, or contributions, please open an issue in the GitHub repository.

---

**Built with ❤️ for healthcare professionals and the patients they serve.**