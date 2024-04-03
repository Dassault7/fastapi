import uvicorn
from fastapi import FastAPI

from app import models
from app.db import engine
from app.routes import router


app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(router, tags=["books"])


if __name__ == "__main__":
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    
    except KeyboardInterrupt:
        print("Exiting...")
