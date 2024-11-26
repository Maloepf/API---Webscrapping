import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.app import get_application

app = get_application()

#redirect root API to automatic swagger documentation
@app.get("/")
async def redirect_root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8080)
