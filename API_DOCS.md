# Nurse's AI Assistant API Documentation

## Overview

The Nurse's AI Assistant API is a FastAPI-powered backend service that combines live biomedical data sources with large language models to generate draft patient education materials and clinical summaries. The API is designed with compliance and guardrails in mind, providing evidence-informed information for nurses and allied health professionals.

## Key Features

- **Multiple Reading Levels**: Content can be generated for elementary through professional reading levels
- **Flexible Word Counts**: Supports customizable word counts (50-2000 words) based on use case
- **Safety Guardrails**: Built-in compliance checking and content filtering
- **Draft-Only Output**: All content requires clinician review before patient use
- **Evidence-Based Sources**: Integration with biomedical literature (mock implementation)
- **Comprehensive Validation**: Input validation and safety checks at multiple levels

## API Endpoints

### Health Check

**GET** `/api/v1/health`

Returns the current health status of the API and its dependencies.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-13T17:22:55.722620",
  "version": "1.0.0",
  "services": {
    "database": "healthy",
    "llm_service": "not_configured",
    "biomedical_api": "disabled"
  }
}
```

### Patient Education Generation

**POST** `/api/v1/patient-education`

Generates patient education materials with specified reading level and word count.

**Request Body:**
```json
{
  "topic": "diabetes management",
  "reading_level": "high-school",
  "word_count": 300,
  "include_sources": true,
  "patient_age_group": "adult",
  "language": "english"
}
```

**Response:**
```json
{
  "content": "Generated patient education content...",
  "title": "Understanding Diabetes Management: A Patient Guide",
  "key_points": [
    "Understanding diabetes management is important for your health",
    "Early recognition of diabetes management symptoms can improve outcomes",
    "Follow your healthcare provider's recommendations about diabetes management",
    "Ask questions about diabetes management during medical appointments"
  ],
  "sources": [
    {
      "title": "Clinical Guidelines for Diabetes Management",
      "authors": ["Smith, J.", "Johnson, M."],
      "journal": "Medical Journal",
      "year": 2023,
      "doi": "10.1000/example",
      "relevance_score": 0.95
    }
  ],
  "metadata": {
    "generated_at": "2025-09-13T17:23:02.291878",
    "word_count": 265,
    "reading_level": "high-school",
    "model_used": "gpt-3.5-turbo",
    "safety_flags": [],
    "requires_review": true
  },
  "disclaimer": "This content is AI-generated and intended as a draft. It must be reviewed and approved by a qualified healthcare professional before use."
}
```

### Clinical Summary Generation

**POST** `/api/v1/clinical-summary`

Generates clinical summaries from patient data with flexible word counts.

**Request Body:**
```json
{
  "patient_data": "Patient presents with chest pain, shortness of breath, and fatigue. Vital signs stable. History of hypertension.",
  "summary_type": "admission",
  "word_count": 400,
  "include_recommendations": true,
  "focus_areas": ["cardiovascular", "respiratory"]
}
```

**Response:**
```json
{
  "summary": "Clinical admission summary based on provided patient data...",
  "key_findings": [
    "Patient presents with documented clinical history",
    "Current symptoms align with clinical presentation",
    "Vital signs within documented ranges"
  ],
  "recommendations": [
    "Continue current treatment plan as prescribed",
    "Monitor symptoms and report changes to healthcare provider",
    "Follow-up appointment recommended within specified timeframe"
  ],
  "risk_factors": [
    "Standard risk factors identified in clinical history",
    "Consider patient-specific risk assessment"
  ],
  "follow_up_needed": [
    "Schedule routine follow-up as per clinical guidelines",
    "Patient education on symptom monitoring"
  ],
  "metadata": {
    "generated_at": "2025-09-13T17:23:09.372900",
    "word_count": 313,
    "reading_level": "professional",
    "model_used": "gpt-3.5-turbo",
    "safety_flags": ["Clinical summary lacks appropriate hedging language"],
    "requires_review": true
  },
  "disclaimer": "This summary is AI-generated and intended to assist healthcare professionals. Clinical decisions should always be based on professional judgment and patient assessment."
}
```

## Reading Levels

The API supports five different reading levels:

1. **Elementary**: Simple language, short sentences
2. **Middle School**: Basic medical terms with explanations
3. **High School**: Standard patient education level
4. **College**: More complex terminology and concepts
5. **Professional**: Clinical language for healthcare providers

## Safety and Compliance Features

### Content Filtering
- Inappropriate medical claims detection
- Definitive medical advice prevention
- Sensitivity checking for high-risk topics

### Privacy Protection
- PII detection in clinical data
- HIPAA compliance considerations
- Patient identifier screening

### Professional Standards
- Mandatory clinician review flags
- Appropriate clinical hedging language
- Professional disclaimers on all content

### Input Validation
- Word count limits (50-2000 words)
- Topic length validation
- Patient data sensitivity checking

## Error Handling

The API returns standard HTTP status codes:

- **200**: Success
- **400**: Bad Request (compliance violations)
- **422**: Validation Error (invalid input)
- **500**: Internal Server Error

Example error response:
```json
{
  "error": "ValidationError",
  "message": "Request failed compliance check: Inappropriate term detected",
  "timestamp": "2025-09-13T17:23:09.372900",
  "request_id": "abc123"
}
```

## Configuration

Key configuration settings (via environment variables):

- `LLM_API_KEY`: API key for language model service
- `ENABLE_LIVE_DATA`: Enable/disable live biomedical data integration
- `MAX_CONTENT_LENGTH`: Maximum word count for generated content
- `ENABLE_CONTENT_FILTERING`: Enable/disable content safety filters

## Development and Testing

### Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Access API documentation
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_patient_education.py -v

# Run with coverage
python -m pytest tests/ --cov=app
```

## Integration Notes

### For Frontend Applications
- Use CORS-enabled endpoints
- Handle async operations appropriately
- Always display compliance disclaimers
- Implement proper error handling

### For Healthcare Systems
- Ensure proper authentication/authorization
- Implement audit logging
- Follow data governance policies
- Maintain clinician review workflows

## Limitations and Considerations

1. **Draft Content Only**: All generated content requires professional review
2. **Mock Implementation**: Current version uses mock data sources
3. **No Diagnosis**: API does not provide medical diagnoses
4. **Compliance Required**: Users must ensure HIPAA and other regulatory compliance
5. **Professional Oversight**: Clinical decisions must involve qualified healthcare professionals

## Future Enhancements

- Live biomedical data integration
- Advanced LLM model support
- Multi-language support
- Enhanced clinical decision support
- Integration with EHR systems
- Advanced analytics and reporting