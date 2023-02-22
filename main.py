from fastapi import FastAPI
from routers import auth, article

app=FastAPI()
app.include_router(auth.router)
app.include_router(article.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}