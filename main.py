from fastapi import FastAPI

from routers import marketing


app = FastAPI()

app.include_router(marketing.router)
