import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables (Supabase URL and Key)
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Clinic Appointment Agent API",
    description="Backend API for slot validation and booking",
    version="1.0.0"
)

# Allow CORS for Flowise/Langflow webhooks
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include the booking router
from routes.booking import router as booking_router
app.include_router(booking_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Clinic Appointment API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
