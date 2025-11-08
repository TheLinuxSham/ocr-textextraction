# start main manually with hot reload enabled:
# uvicorn main:app --reload --port 4321

import asyncio
import os
import time
import uuid

import psutil
from error_parsing import check_param
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from image_processing import process_image

print("CWD:", os.getcwd())
app = FastAPI()


@app.get("/", response_class=RedirectResponse)
async def redirect_to_docs():
    """Redirect to the API documentation."""
    return RedirectResponse(url="/docs")


@app.get("/health")
def run_health_check():
    """
    Performs a basic health check of the running FastAPI process and returns process-level metrics.

    - **status (string)**: "healthy" when the check succeeds.
    - **code (integer)**: HTTP-like status code, here 200.
    - **details (object)**:
        - **duration (number)**: Time taken to perform the health check in seconds, rounded to 4 decimal places.
        - **cpu_user_time (number)**: CPU time spent in user mode by the current process (seconds).
        - **cpu_system_time (number)**: CPU time spent in kernel/system mode by the current process (seconds).
        - **memory_process (number)**: Resident memory size (RSS) of the process in megabytes, rounded to 2 decimal places.
        - **memory_virtual (number)**: Virtual memory size (VMS) of the process in megabytes, rounded to 2 decimal places.

    Example request:
    GET /health

    Example successful response:
    {
        "status": "healthy",
        "code": 200,
        "details": {
            "duration": 0.0007,
            "cpu_user_time": 0.12,
            "cpu_system_time": 0.03,
            "memory_process": 45.23,
            "memory_virtual": 128.50
        }
    }
    """

    start = time.time()
    process = psutil.Process(os.getpid())

    response_data = {
        "status": "healthy",
        "code": 200,
        "details": {
            "duration": round((time.time() - start), 4),
            "cpu_user_time": process.cpu_times().user,
            "cpu_system_time": process.cpu_times().system,
            "memory_process": round(
                (process.memory_info().rss / 1024 / 1024), 2
            ),  # memory consumption of process
            "memory_virtual": round(
                (process.memory_info().vms / 1024 / 1024), 2
            ),  # virtual memory on disk of process
        },
    }

    return JSONResponse(content=response_data)


@app.post("/image-to-text")
async def image_to_text(
    file: UploadFile = File(...),
    engine_mode: int = Form(3),
    segmentation_mode: int = Form(11),
):
    """
    Extract text from an uploaded image file.

    - **file**: The image file to process. Supported formats include JPEG, PNG, etc.

    Returns a JSON response with the following fields:
    - **text**: The extracted text from the image as a string.
    - **version**: The Version of the JSON-File returned.
    - **details**: Contains metrics of the job execution, including:
        - **duration**: Time taken to process the image in seconds, rounded to four decimal places.
        - **job_id**: Unique identifier for the job, generated for tracking purposes.
        - **filename**: The name of the uploaded file.
        - **content_type**: The MIME type of the uploaded file.
    - **errors**: Contains information about any errors encountered during processing:
        - **count**: Number of errors encountered.
        - **error**: Specific error messages, if any.
    """
    try:
        start = time.time()
        job_id = uuid.uuid4().hex
        e, r, config = check_param(engine_mode, segmentation_mode)

        contents = await file.read()
        result = await asyncio.to_thread(process_image, contents, config)

        json_response = {
            "text": result,
            "version": 0.1,
            "details": {
                "duration": round((time.time() - start), 4),
                "job_id": job_id,
                "filename": file.filename,
                "job_id": job_id,
                "content_type": file.content_type,
            },
            "errors": {"count": e, "error": r},
        }

        return JSONResponse(content=json_response, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
