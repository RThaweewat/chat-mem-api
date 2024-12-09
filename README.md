# Chat App API

This project provides a production-grade conversational API similar to ChatGPT, but with openstack-based features such as:

- 📄 Document ingestion and retrieval with [textract](https://textract.readthedocs.io/en/stable/) + [ChromaDB](https://docs.trychroma.com/getting-started)
- 🧠 Memory functionality to maintain conversational state across messages with [LangGraph](https://python.langchain.com/docs/versions/migrating_memory/)
- 🔗 Integration with [Opik](https://www.comet.com/opik) for tracing, custom prompt templates and evaluating LLM calls.
- 🚀 Deployment-ready with Docker, FastAPI, and logging (Loguru).
- 🧪 Example tests (both unit and integration) and Postman collections for easy verification.

**Key Features:**

- **Upload and Process Documents**: Upload `.pdf` or `.docx` files, extract text, and store them in a vector database (Chroma) for semantic retrieval.
- **Conversational Memory**: Maintains conversation context (memory) using LangGraph and state persistence.
- **LLM Integration**: Uses `langchain` and `OpenAI` models to generate answers, leveraging vectorstore retrieval as context.
- **Tracing**: Seamless integration with Opik for logging, tracing, and evaluation of LLM responses, cost and stat.
- **Extensible Architecture**: Code is structured professionally with `src/api`, `src/services`, `src/config`, `src/prompts`, and `tests` directories to keep components modular and maintainable.

---
## Project Structure

```
my_chat_app/
    ├─ src/
    │   ├─ api/
    │   │   ├─ __init__.py
    │   │   ├─ app.py
    │   │   └─ routes/
    │   │       ├─ __init__.py
    │   │       └─ chat.py
    │   ├─ config.py
    │   ├─ services/
    │   │   ├─ __init__.py
    │   │   ├─ document_loader.py
    │   │   ├─ llm.py
    │   │   ├─ observatory.py
    │   │   ├─ vectorstore.py
    │   │   └─ prompt_loader.py
    │   ├─ prompts/
    │   │   └─ prompts.yaml
    │   ├─ utils.py
    │   └─ main.py
    ├─ tests/
    │   ├─ unit/
    │   ├─ api/
    │   └─ ...
    ├─ data/
    │   ├─ uploaded_docs/
    │   └─ chroma/
    ├─ logs/
    │   └─ logs.log
    ├─ requirements.txt
    ├─ Dockerfile
    └─ README.md
```

---
## Requirements

- Python 3.11
- A valid `OPENAI_API_KEY` set in environment.
- Opik Account with `OPIK_API_KEY`, `OPIK_WORKSPACE`, `OPIK_PROJECT_NAME` set in environment.
- Installed dependencies from `requirements.txt`.

---

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/my_chat_app.git
   cd my_chat_app
   ```

2. **Set Environment Variables**:
   Create a `.env` file at the project root and add:
   ```env
   OPENAI_API_KEY=sk-...
   UNSTRUCTURED_API_KEY=...   # optional if using Unstructured API
   OPIK_WORKSPACE=your-workspace
   OPIK_PROJECT_NAME=your-project
   ```

3. **Install Dependencies**:
   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```

4. **Run Locally**:
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```
   The API will be available at `http://localhost:8000`.

5. **Run With Docker**:
   ```bash
   docker build -t my-chat-app:latest .
   docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... my-chat-app:latest
   ```

---

## Usage

### Upload Documents

- **Endpoint**: `POST /upload-docs`
- **Description**: Upload `.pdf` or `.docx` files. The system extracts the text, chunks it, and stores it in the vector database.

**Example cURL:**
```bash
curl -X POST http://localhost:8000/upload-docs \
  -F "files=@/path/to/document.pdf"
```

### Chat with Memory

- **Endpoint**: `POST /chat`
- **Description**: Send a user query. The system retrieves relevant context from vectorstore, uses memory to maintain conversation, and returns a response.
- **Request Body**:
  ```json
  {
    "query": "What is this document about?",
    "thread_id": "optional_thread_id"
  }
  ```
  If `thread_id` is not provided, it defaults to `"default_thread"`.

**Example cURL:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello, who am I?"}'
```

### Reset Conversation

- **Endpoint**: `POST /reset?thread_id=default_thread`
- **Description**: Clears memory for the given thread, resetting the conversation history.

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/reset?thread_id=default_thread"
```

### Reset Vectorstore

- **Endpoint**: `POST /reset-db`
- **Description**: Clears all documents from the vector database. After this, you must re-upload documents for retrieval.

**Example cURL:**
```bash
curl -X POST http://localhost:8000/reset-db
```

### Healthcheck

- **Endpoint**: `GET /healthcheck`
- **Description**: Returns a health status of the server.

**Example cURL:**
```bash
curl http://localhost:8000/healthcheck
```

---

## API Endpoints

- **POST `/upload-docs`**: Upload one or more documents.
  **Response**: `{"status": "ok", "processed_docs": [...]}`

- **POST `/chat`**: Query the chat with memory and vectorstore retrieval.
  **Request JSON**: `{"query": "Your question", "thread_id": "optional_thread_id"}`
  **Response**: `{"answer": "Response from LLM", "metadata": {...}}`

- **POST `/reset`**: Reset conversation memory for a given thread.
  **Query Param**: `thread_id` (default: `default_thread`)
  **Response**: `{"status": "conversation reset"}`

- **POST `/reset-db`**: Clears the entire vectorstore database.
  **Response**: `{"status": "vectorstore reset successfully"}`

- **GET `/healthcheck`**: Returns `{"status": "healthy"}` if the server is running.

---

## Testing

### Unit Tests
Unit tests are located in `tests/unit/`. They mock dependencies to test functions in isolation.

**Run unit tests:**
```bash
pytest tests/unit
```

### Integration (API) Tests
Integration tests are located in `tests/api/` and use `TestClient` to call the FastAPI endpoints.

**Run API tests:**
```bash
pytest tests/api
```

You can also use Postman to test endpoints. A sample Postman collection is provided as `postman_collection.json`. Import it into Postman, set `{{base_url}} = http://localhost:8000`, and run the requests.

---

## Logging & Tracing

- **Loguru** is used for logging. Logs are stored in `logs/logs.log`.
- **Opik** is used to trace LLM calls. Configure `OPIK_WORKSPACE` and `OPIK_PROJECT_NAME` in `.env`. Once configured, logs and traces can be viewed in the Opik dashboard.

---

## Deployment

- The service can be deployed with Docker. Ensure all environment variables are set.
- For production, consider using `gunicorn` or scaling with multiple workers.

---

## License
This project is licensed under the [MIT License](https://opensource.org/license/mit). Check the `LICENSE` file for more details.

---