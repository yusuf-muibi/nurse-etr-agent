from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import agent
from app.services.reminder_service import ReminderService
from contextlib import asynccontextmanager
import os

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize reminder service
reminder_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global reminder_service
    
    # Startup
    print("🚀 Starting Nurse ETR Assistant...")
    reminder_service = ReminderService()
    reminder_service.start()
    print("✅ Application started successfully!")
    
    yield
    
    # Shutdown
    print("👋 Shutting down...")
    if reminder_service and reminder_service.scheduler:
        reminder_service.scheduler.shutdown()

# Create FastAPI app
app = FastAPI(
    title="Nurse ETR Assistant",
    description="AI-powered healthcare assistant for nurses",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agent.router)

@app.get("/")
async def root():
    """Root endpoint - GET"""
    return {
        "message": "Welcome to Nurse ETR Assistant API",
        "status": "operational",
        "docs": "/docs",
        "endpoints": {
            "message": "/agent/message",
            "health": "/agent/health"
        }
    }

@app.post("/")
async def root_post(request: Request):
    """
    Root endpoint - POST
    Handles Telex messages sent to root URL
    """
    try:
        body = await request.json()
        print(f"📨 Received POST to root: {body}")
        
        # Extract message from various possible field names
        message_text = (
            body.get('message') or 
            body.get('text') or 
            body.get('content') or 
            body.get('data', {}).get('message', '') or
            body.get('data', {}).get('text', '')
        ).strip()
        
        user_id = (
            body.get('user_id') or 
            body.get('userId') or 
            body.get('sender_id') or 
            body.get('from') or
            'telex_user'
        )
        
        if not message_text:
            print(f"⚠️ No message found in body: {body}")
            return {
                "error": "No message found",
                "received": body,
                "response": "Please provide a message to process."
            }
        
        print(f"📝 Processing: '{message_text}' from {user_id}")
        
        # Import required modules
        from app.routers.agent import MessageRequest, process_message
        from app.database import get_db
        
        # Create message request
        message_request = MessageRequest(message=message_text, user_id=user_id)
        
        # Get database session
        db = next(get_db())
        
        # Process the message
        response = await process_message(message_request, db)
        
        print(f"✅ Responding with: {response}")
        
        return response
    
    except Exception as e:
        print(f"❌ Error in root POST handler: {e}")
        import traceback
        traceback.print_exc()
        
        error_msg = "Sorry, I encountered an error processing your request."
        return {
            "response": error_msg,
            "text": error_msg,
            "message": error_msg,
            "content": error_msg,
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)