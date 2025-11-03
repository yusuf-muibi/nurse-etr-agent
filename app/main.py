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
    """Root endpoint"""
    return {
        "message": "Welcome to Nurse ETR Assistant API",
        "status": "operational",
        "docs": "/docs"
    }


#@app.post("/webhook/telex")
#async def telex_webhook(request: Request):
    """
    Webhook endpoint for Telex.im
    Receives messages from Telex and processes them
    """
    try:
        body = await request.json()
        
        # Extract message data from Telex webhook
        event_type = body.get('event', '')
        
        if event_type == 'message.created':
            message_data = body.get('data', {})
            message_text = message_data.get('text', '').strip()
            user_id = message_data.get('user_id', '')
            channel_id = message_data.get('channel_id', '')
            
            # Process message through agent
            response = await agent.process_message(
                Request(scope={
                    'type': 'http',
                    'method': 'POST',
                    'headers': [],
                    'query_string': b'',
                }),
                message=message_text,
                user_id=user_id
            )
            
            # Send response back to Telex
            # TODO: Implement Telex response
            
            return {"status": "processed"}
        
        return {"status": "ignored"}
    
    except Exception as e:
        print(f"Webhook error: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)