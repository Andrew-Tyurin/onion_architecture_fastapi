import time

import uvicorn
from fastapi import FastAPI, Request

from api.routers import books, users
from api.routers.auth import auth

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(books.router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
