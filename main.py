import uvicorn
from fastapi import FastAPI

from api.routers import books
from api.routers import users

app = FastAPI()

app.include_router(users.router)
app.include_router(books.router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
