# RAG Queue Server

This is an asynchronous Retrieval-Augmented Generation (RAG) system built with FastAPI, Redis Queue (RQ) and Qdrant. It answers questions based on a specific knowledge base (a Node.js book, by default) using Google's Generative AI models.

## Features

*   **FastAPI Backend**: Exposes REST endpoints to submit chat queries and poll for results.
*   **Asynchronous Processing**: Uses Redis Queue (RQ) to handle time-consuming LLM and retrieval tasks in the background without blocking the API.
*   **LangChain & Qdrant**: Implements RAG by retrieving relevant documents from a Qdrant vector database and synthesizing an answer using Gemini.
*   **Google Generative AI**: Uses `models/text-embedding-004` for embeddings and `gemini-1.5-flash` for generation.

## Prerequisites

*   Python 3.10+
*   Redis server (for RQ)
*   Qdrant server (for vector storage)
*   Google API Key (for Gemini and Google Embeddings)

## Environment Variables

Create a `.env` file in the root of the project with the following keys:

```env
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=nodejs_book
GOOGLE_API_KEY=your_google_api_key_here
```

## Setup & Running

1. **Start infrastructure (Redis, Qdrant)**:
   You can use the provided `docker-compose.yml` to start the required services.
   ```bash
   docker-compose up -d
   ```

2. **Start the Worker**:
   Start the RQ worker to process background jobs.
   ```bash
   rq worker
   ```

3. **Start the API Server**:
   ```bash
   python main.py
   ```
   The API will be available at `http://0.0.0.0:8001`.

## API Endpoints

*   `GET /`: Health check to verify the server is running.
*   `POST /chat?query={your_question}`: Submit a query to the queue. Returns a `job_id`.
*   `GET /chat/{job_id}`: Poll the status of a job. If finished, it returns the final generated answer.
