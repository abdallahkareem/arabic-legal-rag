# Arabic Legal RAG

An early-stage retrieval-augmented generation (RAG) project for Egyptian civil law. The repository currently contains a FastAPI service scaffold and an ingestion utility that extracts Arabic and English article text from a bilingual PDF into structured JSON.

> **Project status:** Retrieval, vector indexing, and answer generation are not implemented yet. The current API does not answer legal questions.

## Current capabilities

- FastAPI application with a welcome route and a health-check route.
- PDF parsing with PyMuPDF, including Arabic and English article extraction and article-number matching.
- Structured JSON output containing page, section, topic, article number, and Arabic and English text fields.
- Project dependencies and environment settings managed with `uv` and Pydantic Settings.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)
- The Egyptian Civil Law PDF for running the ingestion utility

The PDF is tracked through DVC. The repository contains its DVC pointer, not the PDF itself, and no DVC remote is configured in this checkout. Obtain the PDF through the project maintainers or configure the appropriate DVC remote before running ingestion.

## Getting started

Clone the repository, enter its directory, and install the locked dependencies:

```powershell
uv sync
```

Create a local environment file from the example:

```powershell
Copy-Item .env.example .env
```

Set the input PDF and output JSON paths in `.env`. Paths can be relative to the repository root:

```dotenv
APP_NAME="Arabic Legal RAG"
APP_VERSION="0.1.0"
PDF_PATH="data/docs/EgyptionCivilLaw.pdf"
JSON_PATH="data/processed/law_structured.json"
```

Ensure the PDF exists at `PDF_PATH` before running ingestion. Keep `.env` local; do not commit machine-specific paths or secrets.

## Run the API

Start the development server from the repository root:

```powershell
uv run uvicorn src.main:app --reload
```

The service is available at `http://127.0.0.1:8000`.

| Endpoint | Description |
| --- | --- |
| `GET /api/v1/` | Returns a welcome message. |
| `GET /api/v1/health` | Returns `{"status":"ok"}` when the service is running. |
| `GET /docs` | Interactive OpenAPI documentation. |

## Run PDF ingestion

With `.env` configured and the source PDF available, run:

```powershell
uv run python -m src.rag.ingestion.parser
```

The parser writes the extracted articles to `JSON_PATH`. Arabic article numerals are converted to Western numerals, and English text is matched to Arabic articles by article number. Records include page and section metadata; the `topic` field is currently unset. The parser relies on the document's two-column layout and article-heading formats, so review the output for documents with a different layout or formatting.

## Project layout

```text
data/
	docs/          DVC pointer for the source civil-law PDF
	processed/     Processed data and generated JSON output
src/
	main.py        FastAPI application
	helpers/       Application settings
	routes/        API route definitions
	rag/
		ingestion/   PDF parsing and text-processing utilities
		generation/  Reserved for future generation components
		retrival/    Reserved for future retrieval components
```

## Development

Run the configured formatter and linter hooks with `uv`:

```powershell
uvx pre-commit run --all-files
```

## Limitations

- No retrieval pipeline, vector store, or LLM-backed answer generation is currently available.
- The API currently exposes only welcome and health-check endpoints.
- `docker-compose.yml` and `Dockerfile` are empty; container-based setup is not available yet.
- The source PDF is not included directly in the repository checkout.

