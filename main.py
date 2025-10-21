import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from google.router import router as google_router
from zoho.router import router as zoho_router

app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key="your-super-secret-key")

app.include_router(google_router, prefix="/provider/google", tags=["google"])
app.include_router(zoho_router, prefix="/provider/zoho", tags=["zoho"])

@app.get("/")
def read_root():
    return {"message": "Welcome to your custom SSO system. Navigate to /provider/google/authorize to login with Google."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)