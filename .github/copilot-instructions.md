# Nurse API - FastAPI Development Instructions

**ALWAYS follow these instructions first and only fallback to additional search and context gathering if the information here is incomplete or found to be in error.**

The Nurse API is a FastAPI-based backend for "Nurse's AI Assistant," an AI-powered tool for nurses and healthcare professionals to access and summarize biomedical knowledge from trusted sources like PubMed, ClinicalTrials.gov, MedlinePlus, MyGene, and MyChem.

## Repository Status

**CURRENT STATE**: Working minimal FastAPI application with validated build, test, and deployment workflows.

**VALIDATED STRUCTURE**: The repository now contains a complete FastAPI project structure:
- `/app/main.py` - FastAPI application entry point (VALIDATED WORKING)
- `/tests/test_main.py` - Test suite with 3 passing tests (VALIDATED WORKING)
- `/requirements.txt` - Complete tested dependencies list (VALIDATED WORKING)
- `/.env.example` - Environment variable template for configuration
- `/app/routers/`, `/app/models/`, `/app/services/` - Empty directories for future development
- `/config/` - Configuration directory

## Working Effectively

### Environment Setup
Run these commands to set up the development environment:

```bash
# Ensure Python 3.12+ is available
python3 --version  # Verified: Python 3.12.3

# Install ALL dependencies - NEVER CANCEL these operations
pip3 install fastapi uvicorn pytest httpx black flake8 mypy openai requests aiohttp sqlalchemy alembic python-multipart
```

**VALIDATED TIMING**: 
- Core packages install: ~15 seconds (set timeout: 300+ seconds)
- Additional packages install: ~8 seconds (set timeout: 300+ seconds)
- NEVER CANCEL - let pip complete all installations

### Development Workflow

#### 1. Building/Running the Application
The application is ready to run immediately:

```bash
# Development mode with auto-reload (VALIDATED WORKING)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Production mode (VALIDATED WORKING)
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Background mode for testing (VALIDATED WORKING)
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
```

**VALIDATED STARTUP TIME**: ~3 seconds. Server is ready when you see "Application startup complete."

#### 2. Running Tests
```bash
# Run all tests (VALIDATED - 3 tests pass in ~0.4 seconds)
python3 -m pytest -v

# Run specific test file (VALIDATED WORKING)
python3 -m pytest tests/test_main.py -v

# Install dependencies from requirements.txt (VALIDATED WORKING)
pip3 install -r requirements.txt
```

**VALIDATED TIMING**: Tests complete in ~0.7 seconds total (set timeout: 120+ seconds for larger test suites)

#### 3. Code Quality and Linting
**CRITICAL**: Always run these before committing changes:

```bash
# Format code (VALIDATED - reformats files automatically)
black .

# Check code style (VALIDATED - must pass with no output)
flake8 .

# Type checking (VALIDATED - must show "Success: no issues found")
mypy .

# Check formatting without changes (VALIDATED WORKING)
black --check .
```

**VALIDATED TIMING**: 
- black: ~0.3 seconds (set timeout: 60+ seconds)
- flake8: ~0.2 seconds (set timeout: 60+ seconds)  
- mypy: ~6 seconds (set timeout: 120+ seconds)

### Validation Scenarios

After making any changes, ALWAYS validate by running through these scenarios:

#### Basic API Validation (VALIDATED WORKING)
1. **Complete Pre-commit Workflow** (VALIDATED - completes in ~8 seconds):
   ```bash
   black . && flake8 . && mypy . && python3 -m pytest -v
   ```

2. **Health Check Flow** (VALIDATED WORKING):
   ```bash
   # Start server in background
   uvicorn app.main:app --host 0.0.0.0 --port 8000 &
   
   # Wait for startup (3 seconds)
   sleep 3
   
   # Test endpoints (VALIDATED RESPONSES)
   curl -s http://localhost:8000/health
   # Returns: {"status":"healthy","service":"nurse-ai-api","version":"0.1.0"}
   
   curl -s http://localhost:8000/
   # Returns: {"message":"Welcome to Nurse's AI Assistant API","version":"0.1.0","status":"running","docs":"/docs","redoc":"/redoc"}
   
   # Stop server
   pkill -f uvicorn
   ```

3. **API Documentation Access** (VALIDATED WORKING):
   - `http://localhost:8000/docs` - Swagger UI (returns HTTP 200)
   - `http://localhost:8000/redoc` - ReDoc documentation (returns HTTP 200)
   - `http://localhost:8000/openapi.json` - OpenAPI schema (returns JSON)

#### Manual Validation Requirements
**ALWAYS test these complete user scenarios after making changes:**

4. **Full Application Lifecycle Test** (VALIDATED WORKING):
   ```bash
   # 1. Start server and verify startup logs
   uvicorn app.main:app --host 0.0.0.0 --port 8001 &
   sleep 3
   
   # 2. Test all endpoints return expected JSON
   curl -s http://localhost:8001/health | grep "healthy"
   curl -s http://localhost:8001/ | grep "Welcome"
   
   # 3. Verify server handles requests properly
   curl -s -I http://localhost:8001/docs | head -1 | grep "200"
   
   # 4. Clean shutdown
   pkill -f uvicorn
   ```

### Common Development Tasks

#### Adding New Endpoints
1. Edit files in `/app/main.py` or create new files in `/app/routers/`
2. Add corresponding tests in `/tests/`
3. Run the complete validation workflow:
   ```bash
   black . && flake8 . && mypy . && python3 -m pytest -v
   ```
4. Test manually with the server running

#### Dependency Management (VALIDATED WORKING)
```bash
# Add new dependency
pip3 install package_name

# Update requirements (VALIDATED WORKING)
pip3 freeze > requirements.txt

# Install from requirements (VALIDATED WORKING)
pip3 install -r requirements.txt
```

### Build and Deployment

#### Local Development (VALIDATED WORKING)
```bash
# Install all dependencies (VALIDATED - takes ~23 seconds total)
pip3 install -r requirements.txt

# Run in development mode (VALIDATED WORKING)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Timing Expectations and Timeouts

**VALIDATED ACTUAL TIMING - NEVER CANCEL these operations:**

- **pip install (all packages)**: 23 seconds (set timeout: 300+ seconds)
- **black formatting**: 0.3 seconds (set timeout: 60+ seconds)
- **flake8 linting**: 0.2 seconds (set timeout: 60+ seconds) 
- **mypy type checking**: 6 seconds (set timeout: 120+ seconds)
- **pytest execution**: 0.7 seconds (set timeout: 120+ seconds)
- **uvicorn startup**: 3 seconds (set timeout: 60+ seconds)
- **API response tests**: 1-2 seconds per request (set timeout: 30+ seconds)
- **Complete pre-commit workflow**: 8 seconds (set timeout: 180+ seconds)

### Key Files and Locations

**CURRENT VALIDATED STRUCTURE:**
```
/home/runner/work/nurse_api/nurse_api/
├── .env.example - Environment variable template
├── README.md - Project documentation
├── requirements.txt - ALL tested dependencies (2080 bytes)
├── app/
│   ├── __init__.py
│   ├── main.py - FastAPI application (1252 bytes, WORKING)
│   ├── models/ - Empty, ready for Pydantic models
│   ├── routers/ - Empty, ready for API routes
│   └── services/ - Empty, ready for business logic
├── tests/
│   ├── __init__.py
│   └── test_main.py - 3 passing tests (1442 bytes, ALL PASS)
└── config/ - Empty, ready for configuration files
```

### Troubleshooting

#### Common Issues (TESTED SOLUTIONS)
1. **Port conflicts**: Use different port - `uvicorn app.main:app --port 8001`
2. **Import errors**: Run from repository root directory
3. **Dependencies missing**: Run `pip3 install -r requirements.txt`
4. **Tests failing**: Check that server isn't running on port 8000

#### Debug Mode (VALIDATED WORKING)
```bash
# Run with debug logging (VALIDATED WORKING)
uvicorn app.main:app --log-level debug --reload
```

### Security and Compliance Notes

- **Environment variables**: Use `.env.example` as template
- **API keys**: Store in environment variables, never commit
- **PHI protection**: No PHI storage in current implementation
- **CORS**: Currently configured for development (allow all origins)

### Pre-commit Checklist

**VALIDATED COMPLETE WORKFLOW** - Before committing any changes, ALWAYS run:
```bash
# Complete validation (VALIDATED - takes ~8 seconds)
black . && flake8 . && mypy . && python3 -m pytest -v

# Manual test (VALIDATED WORKING)
uvicorn app.main:app --port 8001 &
sleep 3
curl -s http://localhost:8001/health
pkill -f uvicorn
```

**Total pre-commit validation time**: 12 seconds. NEVER SKIP these steps.

## Reference Information

### Validated Package Versions
These package versions were tested and confirmed working on 2025-09-14:

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

### System Requirements (VALIDATED)
- **Python**: 3.12.3 (confirmed working)
- **pip**: 24.0 (confirmed working)
- **Operating System**: Linux Ubuntu (confirmed working)

### Performance Benchmarks (MEASURED)
Real measured performance on validation system:
- Package installs: 15 seconds (core) + 8 seconds (additional)
- Code formatting (black): 0.3 seconds
- Linting (flake8): 0.2 seconds
- Type checking (mypy): 6 seconds
- Test execution: 0.7 seconds (3 tests)
- FastAPI startup: 3 seconds
- Complete pre-commit workflow: 8 seconds

Use these benchmarks to set appropriate expectations and timeouts.