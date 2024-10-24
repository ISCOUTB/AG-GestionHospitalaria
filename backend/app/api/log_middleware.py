from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

import time
from datetime import datetime

from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]
collection = db["api_logs"]  # Colección para los registros de la API


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        
        process_time = time.perf_counter() - start_time
        process_time_ms = round(process_time * 1000, 2)
        
        body = await request.body()

        log_data = {
            "timestamp": datetime.now(),
            "method": request.method,
            "url": request.url.path,
            "headers": dict(request.headers),
            "body": body.decode("utf-8") if body else None,
            "process_time_ms": process_time_ms,
            "status_code": response.status_code
        }

        collection.insert_one(log_data)

        return response
