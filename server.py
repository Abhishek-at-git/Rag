from fastapi import FastAPI, HTTPException, Query

from .client.rq_client import enqueue_query, queue

app = FastAPI()


@app.get("/")
def root():
    return {"status": "server is up and running"}

@app.post("/chat")
def chat(
    query: str = Query(..., description="The chat query from the user"),
):
    job = enqueue_query(query)
    return {"status": "queued", "job_id": job.id}


@app.get("/chat/{job_id}")
def get_result(
    job_id: str,
):
    job = queue.fetch_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    if not job.is_finished:
        return {"status": job.get_status()}

    return {"status": "finished", "result": job.return_value()}