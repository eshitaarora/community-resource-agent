"""
Chat API endpoints for the AI agent
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.agents.resource_agent import get_agent
from datetime import datetime

router = APIRouter()


class Message(BaseModel):
    """Schema for a chat message"""
    content: str = Field(..., min_length=1, max_length=2000)
    
    class Config:
        example = {
            "content": "I need help finding shelter in downtown"
        }


class UserContext(BaseModel):
    """Schema for user context/profile"""
    location: Optional[str] = None
    needs: Optional[List[str]] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    eligibility_info: Optional[Dict[str, Any]] = None
    accessibility_needs: Optional[List[str]] = None


class ChatRequest(BaseModel):
    """Schema for chat request"""
    user_id: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1, max_length=2000)
    user_context: Optional[UserContext] = None
    include_history: bool = False


class ChatResponse(BaseModel):
    """Schema for chat response"""
    success: bool
    message: str
    user_id: str
    tools_used: List[str] = []
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConversationMessage(BaseModel):
    """Schema for conversation history"""
    id: int
    user_message: str
    agent_response: str
    tools_used: List[str]
    timestamp: str


@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    Send a message to the AI agent and get a response.
    
    The agent will understand the user's needs and search for relevant resources.
    Supports multi-turn conversations with context awareness.
    """
    try:
        agent = get_agent()
        
        # Prepare user context
        user_context = None
        if request.user_context:
            user_context = request.user_context.model_dump(exclude_none=True)
        
        # Process the message
        result = agent.process_message(
            user_message=request.message,
            user_id=request.user_id,
            user_context=user_context
        )
        
        return ChatResponse(
            success=result["success"],
            message=result["message"],
            user_id=result["user_id"],
            tools_used=result.get("tools_used", []),
            error=result.get("error")
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing message: {str(e)}"
        )


@router.get("/history/{user_id}", response_model=List[ConversationMessage])
async def get_chat_history(
    user_id: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Retrieve conversation history for a user.
    
    Args:
        user_id: The user's unique identifier
        limit: Number of recent messages to retrieve (max 100)
    
    Returns:
        List of recent chat messages
    """
    if limit > 100:
        limit = 100
    if limit < 1:
        limit = 10
    
    try:
        agent = get_agent()
        history = agent.get_conversation_history(user_id, limit)
        
        return [
            ConversationMessage(**msg)
            for msg in history
        ]
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving history: {str(e)}"
        )


@router.delete("/history/{user_id}")
async def clear_chat_history(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Clear chat history for a user.
    
    Args:
        user_id: The user's unique identifier
    
    Returns:
        Confirmation message
    """
    try:
        from app.db.models import ChatMessage
        
        deleted_count = (
            db.query(ChatMessage)
            .filter(ChatMessage.user_id == user_id)
            .delete()
        )
        db.commit()
        
        return {
            "success": True,
            "message": f"Deleted {deleted_count} messages from chat history"
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing history: {str(e)}"
        )


@router.post("/feedback/{message_id}")
async def submit_feedback(
    message_id: int,
    helpful: bool,
    feedback_text: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Submit feedback on a specific message from the agent.
    
    Args:
        message_id: ID of the chat message
        helpful: Whether the response was helpful
        feedback_text: Optional feedback text
    
    Returns:
        Confirmation of feedback submission
    """
    try:
        from app.db.models import ChatMessage
        
        message = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        message.helpful = helpful
        db.commit()
        
        return {
            "success": True,
            "message": "Thank you for your feedback!",
            "message_id": message_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error submitting feedback: {str(e)}"
        )


@router.get("/test")
async def test_chat():
    """
    Test endpoint to verify chat system is working.
    """
    return {
        "status": "Chat API is running",
        "endpoints": {
            "send_message": "POST /api/chat/send",
            "get_history": "GET /api/chat/history/{user_id}",
            "clear_history": "DELETE /api/chat/history/{user_id}",
            "submit_feedback": "POST /api/chat/feedback/{message_id}"
        }
    }
