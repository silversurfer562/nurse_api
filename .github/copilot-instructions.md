# Nurse API - FastAPI Development Instructions

**ALWAYS follow these instructions first and only fallback to additional search and context gathering if the information here is incomplete or found to be in error.**

The Nurse API is a FastAPI-based backend for "Nurse's AI Assistant," an AI-powered tool for nurses and healthcare professionals to access and summarize biomedical knowledge from trusted sources like PubMed, ClinicalTrials.gov, MedlinePlus, MyGene, and MyChem.

## Repository Status

**CURRENT STATE**: This repository is in early development with minimal code. Currently contains only README.md describing the intended functionality.

**EXPECTED STRUCTURE**: When fully developed, this will be a standard Python FastAPI project with the following anticipated structure:
- `/app/` - Main application code
- `/tests/` - Test suite
- `/requirements.txt` or `pyproject.toml` - Dependencies
- `/alembic/` - Database migrations (if using databases)
- `/config/` - Configuration files

## Working Effectively

### Environment Setup
Run these commands to set up the development environment:

```bash
# Ensure Python 3.12+ is available
python3 --version  # Verified: Python 3.12.3

# Install core dependencies for FastAPI development
pip3 install fastapi uvicorn pytest httpx black flake8 mypy openai

# For biomedical integrations (when implemented)
pip3 install requests aiohttp sqlalchemy alembic python-multipart
```

**Installation time**: ~2-3 minutes. NEVER CANCEL - let pip complete all installations.

### Development Workflow

#### 1. Building/Running the Application
Since the codebase is minimal, create a basic FastAPI structure first:

```bash
# When main application exists, run with:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# For production:
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Expected behavior**: FastAPI starts in ~5-10 seconds with automatic reload in development mode.

#### 2. Running Tests
```bash
# Run all tests
python3 -m pytest -v

# Run tests with coverage (when coverage is set up)
python3 -m pytest --cov=app tests/

# Run specific test file
python3 -m pytest tests/test_main.py -v
```

**Test execution time**: ~5-30 seconds depending on test suite size. NEVER CANCEL - always wait for completion.

#### 3. Code Quality and Linting
**CRITICAL**: Always run these before committing changes:

```bash
# Format code (auto-fixes formatting issues)
black .

# Check code style (must pass)
flake8 .

# Type checking (must pass)
mypy .

# Check formatting without changes
black --check .
```

**Linting time**: ~10-30 seconds total. NEVER CANCEL - these are fast operations.

### Validation Scenarios

After making any changes, ALWAYS validate by running through these scenarios:

#### Basic API Validation
1. **Health Check Flow**:
   ```bash
   # Start the server
   uvicorn app.main:app --host 0.0.0.0 --port 8000 &
   
   # Test endpoints
   curl -s http://localhost:8000/health
   curl -s http://localhost:8000/
   
   # Stop server
   pkill -f uvicorn
   ```

2. **API Documentation Access**:
   - Navigate to `http://localhost:8000/docs` for Swagger UI
   - Navigate to `http://localhost:8000/redoc` for ReDoc
   - Verify all endpoints are documented and testable

#### Application-Specific Validation (when implemented)
3. **Biomedical Data Integration**:
   - Test PubMed search functionality
   - Verify ClinicalTrials.gov integration
   - Validate MedlinePlus content retrieval
   - Test AI summarization with sample medical queries

4. **Safety and Compliance**:
   - Verify no PHI (Protected Health Information) is stored
   - Confirm "draft-only" disclaimers are present
   - Test rate limiting and error handling

### Common Development Tasks

#### Adding New Endpoints
1. Create route in appropriate module under `/app/routers/`
2. Add corresponding tests in `/tests/`
3. Update API documentation
4. Run full validation workflow

#### Database Operations (when implemented)
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Downgrade migration
alembic downgrade -1
```

#### Dependency Management
```bash
# Add new dependency
pip3 install package_name

# Update requirements
pip3 freeze > requirements.txt

# Or if using pyproject.toml, update dependencies there
```

### Build and Deployment

#### Local Development
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run in development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Production Considerations
- Use environment variables for API keys (OpenAI, database connections)
- Configure proper logging levels
- Set up monitoring and health checks
- Ensure HIPAA compliance measures are in place

### Timing Expectations and Timeouts

**NEVER CANCEL these operations - always use these timeout values:**

- **pip install**: 2-5 minutes (set timeout: 300+ seconds)
- **pytest execution**: 5-60 seconds depending on test count (set timeout: 120+ seconds)
- **uvicorn startup**: 5-15 seconds (set timeout: 60+ seconds)
- **linting (black/flake8/mypy)**: 10-30 seconds each (set timeout: 60+ seconds)
- **API response tests**: 1-10 seconds per request (set timeout: 30+ seconds)

### Key Files and Locations

When the codebase is developed, expect these key files:
- `/app/main.py` - FastAPI application entry point
- `/app/routers/` - API route definitions
- `/app/models/` - Pydantic models and database schemas  
- `/app/services/` - Business logic and external API integrations
- `/tests/` - Test suite
- `/requirements.txt` or `pyproject.toml` - Dependencies
- `/alembic.ini` and `/alembic/` - Database migration configuration
- `/.env.example` - Environment variable template

### Troubleshooting

#### Common Issues
1. **Import errors**: Ensure PYTHONPATH includes the project root
2. **Database connection issues**: Check environment variables and database status
3. **API key errors**: Verify OpenAI API key is set in environment
4. **Port conflicts**: Use different port if 8000 is occupied

#### Debug Mode
```bash
# Run with debug logging
uvicorn app.main:app --log-level debug --reload

# Python debugger integration
python3 -m pdb -m uvicorn app.main:app --reload
```

### Security and Compliance Notes

- **NEVER commit API keys or secrets** - use environment variables
- **ALWAYS include PHI protection measures** when handling health data
- **REQUIRE clinician review disclaimers** for all AI-generated content
- **IMPLEMENT rate limiting** to prevent API abuse
- **USE HTTPS** in production environments

### Pre-commit Checklist

Before committing any changes, ALWAYS run:
1. `black .` - Format code
2. `flake8 .` - Check style
3. `mypy .` - Type checking  
4. `python3 -m pytest` - Run tests
5. Test at least one complete user scenario manually
6. Verify no secrets are committed

**Total pre-commit validation time**: 2-5 minutes. NEVER SKIP these steps.

## Reference Information

### Tested Package Versions (as of validation)
These package versions have been validated to work together:

```
aiohttp==3.12.15
alembic==1.16.5
black==25.1.0
fastapi==0.116.1
flake8==7.3.0
httpx==0.28.1
mypy==1.18.1
openai==1.107.2
pytest==8.4.2
requests==2.31.0
sqlalchemy==2.0.43
uvicorn==0.35.0
```

### System Requirements
- **Python**: 3.12+ (tested with Python 3.12.3)
- **pip**: 24.0+ for reliable package installation
- **Operating System**: Linux (Ubuntu/Debian tested), macOS, Windows

### Performance Benchmarks
Based on validation testing:
- Package imports: ~0.8 seconds
- Code formatting (black): ~0.1 seconds  
- Linting (flake8): ~0.1 seconds
- Type checking (mypy): ~1.0 seconds
- Test execution: ~0.7 seconds for basic FastAPI tests
- FastAPI startup: ~0.3 seconds

Use these benchmarks to set appropriate expectations and timeouts.