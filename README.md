# Nurse AI Assistant API

`nurse_api` is the FastAPI-based backend for **Nurse's AI Assistant**, an AI-powered tool that helps nurses and allied health professionals quickly access, summarize, and adapt biomedical knowledge. By integrating large language models with trusted biomedical sources like PubMed, ClinicalTrials.gov, MedlinePlus, MyGene, and MyChem, the service generates evidence-informed drafts for patient education and professional use.

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip or poetry for package management
- (Optional) Redis for caching
- (Optional) OpenAI API key for AI content generation

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd nurse_api
   ```

2. **Quick start with the development script**
   ```bash
   ./start_dev.sh
   ```
   
   Or manual setup:

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Run tests**
   ```bash
   pytest tests/ -v
   ```

6. **Start the development server**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

The API will be available at:
- **API Server**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

### Docker Setup

1. **Using docker-compose (recommended)**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   docker-compose up --build
   ```

2. **Using Docker directly**
   ```bash
   docker build -t nurse-ai-api .
   docker run -p 8000:8000 nurse-ai-api
   ```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Redis Configuration (for caching)
REDIS_URL=redis://localhost:6379

# Application Configuration
APP_NAME=Nurse AI Assistant API
DEBUG=false
LOG_LEVEL=INFO

# NCBI API Configuration (for PubMed access)
NCBI_API_KEY=your_ncbi_api_key_here
NCBI_EMAIL=your_email@example.com
```

### API Keys Setup

1. **OpenAI API Key** (Optional - will use mock data if not provided)
   - Get from: https://platform.openai.com/api-keys
   - Required for AI content generation

2. **NCBI API Key** (Optional - improves rate limits)
   - Get from: https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/
   - Required for high-volume PubMed access

## 📚 API Usage

### Generate Medical Summary

```bash
curl -X POST "http://localhost:8000/api/v1/summaries" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "diabetes management",
    "content_type": "patient_education",
    "reading_level": "high_school",
    "word_count": 300,
    "include_sources": true
  }'
```

### Get Available Sources

```bash
curl "http://localhost:8000/api/v1/summaries/sources/diabetes"
```

### Health Check

```bash
curl "http://localhost:8000/health/"
```

## 🏗️ Architecture

### Key Features

* **Draft Summaries & Education Materials** — Generates concise, adjustable content for patients, students, or clinicians.
* **Reading Level Control** — Customizes output for different audiences (elementary to professional).
* **Flexible Word Counts** — Provides summaries that are clear, concise, and informative.
* **Live Data Retrieval** — Pulls the latest information from biomedical databases.
* **Safety Guardrails** — Enforces draft-only usage, requires clinician review, and avoids PHI storage.
* **Caching Layer** — Redis-based caching for improved performance.
* **Source Attribution** — Proper citations for all generated content.

### Tech Stack

* **FastAPI** for asynchronous Python APIs
* **OpenAI SDK v2** for language generation and summarization
* **Redis** for caching and session management
* **Biomedical Integrations**:
  - PubMed (via NCBI E-utilities)
  - ClinicalTrials.gov
  - MedlinePlus
  - MyGene.info
  - MyChem.info
* **Pydantic** for data validation and serialization
* **Uvicorn** ASGI server for production deployment

### Project Structure

```
nurse_api/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   ├── routers/
│   │   ├── health.py        # Health check endpoints
│   │   └── summaries.py     # Summary generation endpoints
│   ├── services/
│   │   ├── openai_service.py     # OpenAI integration
│   │   ├── biomedical_service.py # Biomedical APIs
│   │   └── cache_service.py      # Redis caching
│   └── utils/
├── tests/                   # Test suite
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Multi-service setup
└── .env.example           # Environment template
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test
pytest tests/test_main.py::test_health_check -v
```

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Set all required API keys and configuration
2. **Redis**: Use a persistent Redis instance for caching
3. **Monitoring**: Set up logging and health checks
4. **Security**: Configure CORS, rate limiting, and authentication
5. **Scaling**: Use multiple worker processes with Gunicorn

### Example Production Command

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## ⚠️ Important Safety Notice

**This application generates draft medical content for educational purposes only.**

- All generated content requires review by qualified healthcare professionals
- Not intended for direct patient care decisions
- Does not replace clinical judgment or professional medical advice
- Complies with HIPAA by not storing patient health information
- Users should always consult healthcare providers for personalized medical advice

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and add tests
4. Run tests: `pytest tests/ -v`
5. Commit changes: `git commit -am 'Add your feature'`
6. Push to branch: `git push origin feature/your-feature`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API](https://platform.openai.com/docs)
- [PubMed E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [ClinicalTrials.gov API](https://clinicaltrials.gov/api/gui)

## 📞 Support

For questions and support, please open an issue in the repository or contact the development team.

---

**Status**: This project is an early-stage prototype, actively under development. Its goal is to support nurses and allied health professionals with responsibly designed AI tools, while ensuring compliance with HIPAA and other regulatory standards.