# AI FHIR Integration Copilot

An AI-powered FHIR assistant built with **LangGraph multi-agent architecture**, featuring RAG knowledge retrieval and InterSystems IRIS integration.

## Features

- **FHIR Q&A** - RAG-enhanced answers based on FHIR specification documents
- **Data Mapping** - Convert natural language/JSON to FHIR resources
- **FHIR Query** - Convert natural language to FHIR Search API and execute against IRIS
- **Bundle Generation** - Generate FHIR Bundles from scenario descriptions
- **Resource Validation** - Validate FHIR resources with AI improvement suggestions
- **IRIS Integration** - Full CRUD operations with InterSystems IRIS FHIR server
- **Settings Page** - Configure LLM, IRIS, and vector store via web UI
- **Vector Store** - Support both FAISS (local) and IRIS Vector Search (database)

## Architecture

```
User Input
  ↓
Router Agent (LangGraph task classification)
  ↓
RAG Retrieval (FAISS / IRIS Vector Search)
  ↓
┌─────────────────────────────────────────────────────────────┐
│  Expert │ Query │ Mapping │ Bundle │ Validation │ IRIS      │
└─────────────────────────────────────────────────────────────┘
  ↓
Return Result
```

### Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI + LangGraph |
| LLM | OpenAI-compatible API (OpenAI, DeepSeek, etc.) |
| Vector Database | FAISS (local) or IRIS Vector Search |
| Embedding | sentence-transformers/all-MiniLM-L6-v2 (384 dims) |
| Frontend | Vanilla HTML/CSS/JS |
| Package Manager | uv |

## Quick Start

### Option 1: Docker Compose (Recommended)

**Prerequisites:**
- Docker and Docker Compose installed

**Steps:**

1. Create `.env` file:
```bash
cp .env.example .env
```

2. Configure API Key in `.env` file:
```bash
# Edit .env file
OPENAI_API_KEY=sk-your-api-key-here
```

2. Start all services:
```bash
docker compose up -d
```

3. Wait for services to be ready:

   > **Note:** After starting Docker, please wait a moment. The vector database needs to be initialized on first startup. Port 8000 will become accessible once initialization is complete. You can monitor the progress with `docker compose logs -f`.

4. Access the application:

| URL | Description |
|-----|-------------|
| http://localhost:8000 | Chat Interface |
| http://localhost:8000/docs | Swagger API Docs |
| http://localhost:52773/csp/sys/UtilHome.csp | IRIS Management Portal |

**Features:**
- Both FAISS and IRIS vector stores are built automatically on startup
- If API key is not configured, a prompt will appear in the chat
- Settings can be changed via the web UI and take effect immediately

**Useful commands:**
```bash
# View logs
docker compose logs -f

# Stop all services
docker compose down

# Rebuild and restart
docker compose up -d --build
```

### Option 2: Local Development

**Prerequisites:**
- Python >= 3.11
- [uv](https://docs.astral.sh/uv/) package manager
- InterSystems IRIS (optional, for data operations)

**Installation:**

```bash
cd ai-fhir-copilot
uv sync
```

**Configuration:**

Edit `.env` file or configure via Settings page:

```env
# LLM Configuration
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4o

# Vector Store (faiss or iris)
VECTOR_STORE_TYPE=faiss

# IRIS Configuration
IRIS_HOST=http://localhost:52773
IRIS_NAMESPACE=USER
IRIS_FHIR_PATH=/fhir/r4
IRIS_USERNAME=_SYSTEM
IRIS_PASSWORD=SYS
IRIS_SQL_PORT=1972
```

**Start:**

```bash
uv run main.py
```

**Access:**

| URL | Description |
|-----|-------------|
| http://localhost:8000 | Chat Interface |
| http://localhost:8000/docs | Swagger API Docs |

## Settings

Click the gear icon (⚙) in the header to open Settings.

**Note:** All settings take effect immediately after saving. No restart required.

### LLM Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| API Key | OpenAI-compatible API key | - |
| Base URL | API endpoint | https://api.openai.com/v1 |
| Model Name | Model to use | gpt-4o |

**Supported LLM providers:**
- OpenAI: `https://api.openai.com/v1`
- DeepSeek: `https://api.deepseek.com`
- OpenRouter: `https://openrouter.ai/api/v1`

### Vector Store

| Setting | Description | Default |
|---------|-------------|---------|
| Vector Store Type | FAISS (local) or IRIS (database) | faiss |

- **FAISS**: Stores vectors in local files, fast and simple
- **IRIS**: Stores vectors in IRIS database using native VECTOR type

### IRIS Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| Host | IRIS web server URL | http://localhost:52773 |
| FHIR Path | FHIR REST API path | /fhir/r4 |
| SQL Port | IRIS superserver port | 1972 |
| Username | IRIS username | _SYSTEM |
| Password | IRIS password | SYS |

## Project Structure

```
ai-fhir-copilot/
├── app.py                      # FastAPI application entry point
├── main.py                     # Startup script with auto vector index build
├── config.py                   # Pydantic settings management
├── pyproject.toml              # Project dependencies
│
├── Dockerfile                  # IRIS FHIR server image
├── Dockerfile.app              # AI Copilot application image
├── docker-compose.yml          # Docker Compose orchestration
├── .env.example                # Environment variables template
│
├── graph/
│   └── fhir_graph.py           # LangGraph state machine (router → rag → agent → END)
│
├── agents/
│   ├── state.py                # Shared TypedDict state definition
│   ├── router_agent.py         # Task classification
│   ├── rag_agent.py            # RAG context retrieval
│   ├── expert_agent.py         # FHIR specification Q&A
│   ├── query_agent.py          # Natural language → FHIR Search
│   ├── mapping_agent.py        # JSON → FHIR resource conversion
│   ├── bundle_agent.py         # FHIR Bundle generation
│   ├── validation_agent.py     # FHIR resource validation
│   └── iris_agent.py           # IRIS CRUD operations
│
├── services/
│   ├── llm_service.py          # LLM wrapper (dynamic settings)
│   ├── rag_service.py          # FAISS / IRIS vector store
│   └── iris_service.py         # IRIS REST API client
│
├── api/
│   ├── copilot.py              # POST /api/copilot endpoint
│   └── settings.py             # Settings API endpoints
│
├── knowledge/
│   └── fhir_docs/              # FHIR specification documents (7 files)
│
├── static/
│   └── index.html              # Frontend with settings modal
└── scripts/
    └── build_vectorstore.py    # Rebuild vector index script
```

## API Endpoints

### Chat

```bash
POST /api/copilot
Content-Type: application/json

{"question": "Your question here"}
```

Response:
```json
{
  "task_type": "expert|query|mapping|bundle|validation|iris",
  "result": "Response text with optional JSON data"
}
```

**Note:** If API key is not configured, returns a prompt to configure it in Settings.

### Settings

```bash
# Get current settings
GET /api/settings

# Update settings (applied immediately)
POST /api/settings
Content-Type: application/json

{
  "openai_api_key": "sk-...",
  "openai_base_url": "https://api.openai.com/v1",
  "model_name": "gpt-4o",
  "vector_store_type": "faiss",
  "iris_host": "http://localhost:52773",
  "iris_sql_port": 1972,
  "iris_username": "_SYSTEM",
  "iris_password": "SYS"
}
```

### Vector Store

```bash
# Rebuild vector store
POST /api/vectorstore/rebuild
```

## Examples

**FHIR Q&A:**
```bash
curl -X POST http://localhost:8000/api/copilot \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the FHIR Observation resource?"}'
```

**FHIR Query:**
```bash
curl -X POST http://localhost:8000/api/copilot \
  -H "Content-Type: application/json" \
  -d '{"question": "Find diabetic patients in the last 30 days"}'
```

**Data Mapping:**
```bash
curl -X POST http://localhost:8000/api/copilot \
  -H "Content-Type: application/json" \
  -d '{"question": "{\"name\":\"John\",\"gender\":\"male\"}"}'
```

**Bundle Generation:**
```bash
curl -X POST http://localhost:8000/api/copilot \
  -H "Content-Type: application/json" \
  -d '{"question": "Create a diabetic patient admission record"}'
```

## IRIS Integration

Full integration with InterSystems IRIS FHIR server.

### Supported Operations

| Operation | Description | Example |
|-----------|-------------|---------|
| `search_resource` | Search with FHIR parameters | `Patient?name=Smith` |
| `get_resource` | Read by resource ID | `Patient/123` |
| `create_resource` | Create new resource | POST Patient JSON |
| `update_resource` | Update existing resource | PUT Patient/123 |
| `delete_resource` | Delete resource | DELETE Patient/123 |
| `execute_bundle` | Transaction bundle | POST Bundle JSON |



## License

MIT
