import logging
import os
import sys
import time

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse

from queryImage import get_similar_images
from storage_util import storage_handler

# Load environment variables
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "[%(levelname)s] %(asctime)s - %(name)s - - %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

logger.info('API is starting up')

# BACKEND_BASE_URL = os.getenv("BASE_SERVER_URL", "http://localhost:8000")
STORAGE_TYPE = os.getenv("STORAGE", "local")
IMAGE_FOLDER = os.getenv("IMAGE_FOLDER", "all_images")


@app.get("/images/{filename}")
async def serve_image(filename):
    if STORAGE_TYPE == "local":
        logger.info(f"Trying to retrieve image: {IMAGE_FOLDER}/{filename}")
        file_path = f"{IMAGE_FOLDER}/{filename}"
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(path=file_path)

    raise HTTPException(status_code=404, detail="File not found")


@app.post("/upload-and-search")
async def upload_and_search(file: UploadFile = File(...)):
    start_time = time.time()
    # logger.info(file.filename)
    # logger.info(file.content_type)
    file_path = storage_handler.save_temporary_file(file)
    logger.info(f"Path to save: {file_path}")
    similar_images = get_similar_images(file_path)
    # logger.info(similar_images)
    elapsed_time = time.time() - start_time
    logger.debug(f"Request processed in {elapsed_time:.2f} seconds")
    return JSONResponse(content={"similar_images_uris": similar_images})
