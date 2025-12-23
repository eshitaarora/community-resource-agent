"""
Analytics API endpoints for impact metrics and dashboard data
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import ChatMessage, ServiceAccess, SocialService, UserProfile
from pydantic import BaseModel

router = APIRouter()


class MetricResponse(BaseModel):
    """Schema for metric response"""
    metric: str
    value: Any
    timestamp: datetime


class DashboardStats(BaseModel):
    """Schema for dashboard statistics"""
    total_users: int
    total_conversations: int
    total_services_accessed: int
    unique_services_used: int
    average_messages_per_user: float
    most_accessed_services: List[Dict[str, Any]]
    most_requested_categories: List[Dict[str, Any]]
    helpful_response_rate: float


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    db: Session = Depends(get_db)
):
    """
    Get overall dashboard statistics and impact metrics.
    
    Args:
        days: Number of recent days to analyze (default 30)
    """
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Total unique users
        total_users = db.query(func.count(func.distinct(ChatMessage.user_id))).filter(
            ChatMessage.timestamp >= start_date
        ).scalar() or 0
        
        # Total conversations
        total_conversations = db.query(func.count(ChatMessage.id)).filter(
            ChatMessage.timestamp >= start_date
        ).scalar() or 0
        
        # Total service accesses
        total_accesses = db.query(func.count(ServiceAccess.id)).filter(
            ServiceAccess.access_date >= start_date
        ).scalar() or 0
        
        # Unique services used
        unique_services = db.query(func.count(func.distinct(ServiceAccess.service_id))).filter(
            ServiceAccess.access_date >= start_date
        ).scalar() or 0
        
        # Average messages per user
        avg_messages = 0.0
        if total_users > 0:
            avg_messages = total_conversations / total_users
        
        # Most accessed services
        most_accessed = (
            db.query(
                ServiceAccess.service_name,
                func.count(ServiceAccess.id).label("count")
            )
            .filter(ServiceAccess.access_date >= start_date)
            .group_by(ServiceAccess.service_name)
            .order_by(func.count(ServiceAccess.id).desc())
            .limit(10)
            .all()
        )
        
        most_accessed_services = [
            {"service": service, "count": count}
            for service, count in most_accessed
        ]
        
        # Most requested categories
        most_requested = (
            db.query(
                SocialService.category,
                func.count(ChatMessage.id).label("count")
            )
            .join(ChatMessage, ChatMessage.agent_tools_used.contains(SocialService.category))
            .filter(ChatMessage.timestamp >= start_date)
            .group_by(SocialService.category)
            .order_by(func.count(ChatMessage.id).desc())
            .limit(10)
            .all()
        )
        
        most_requested_categories = [
            {"category": category, "count": count}
            for category, count in most_requested
        ] if most_requested else []
        
        # Helpful response rate
        total_feedback = db.query(func.count(ChatMessage.id)).filter(
            ChatMessage.helpful != None,
            ChatMessage.timestamp >= start_date
        ).scalar() or 0
        
        helpful_count = db.query(func.count(ChatMessage.id)).filter(
            ChatMessage.helpful == True,
            ChatMessage.timestamp >= start_date
        ).scalar() or 0
        
        helpful_rate = (helpful_count / total_feedback * 100) if total_feedback > 0 else 0.0
        
        return DashboardStats(
            total_users=total_users,
            total_conversations=total_conversations,
            total_services_accessed=total_accesses,
            unique_services_used=unique_services,
            average_messages_per_user=round(avg_messages, 2),
            most_accessed_services=most_accessed_services,
            most_requested_categories=most_requested_categories,
            helpful_response_rate=round(helpful_rate, 2)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving dashboard stats: {str(e)}"
        )


@router.get("/impact/users")
async def get_user_impact(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Get user engagement and impact metrics.
    """
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Daily active users
        daily_users = (
            db.query(
                func.date(ChatMessage.timestamp).label("date"),
                func.count(func.distinct(ChatMessage.user_id)).label("users")
            )
            .filter(ChatMessage.timestamp >= start_date)
            .group_by(func.date(ChatMessage.timestamp))
            .order_by(func.date(ChatMessage.timestamp))
            .all()
        )
        
        # New users per day
        new_users = (
            db.query(
                func.date(UserProfile.created_at).label("date"),
                func.count(UserProfile.id).label("count")
            )
            .filter(UserProfile.created_at >= start_date)
            .group_by(func.date(UserProfile.created_at))
            .order_by(func.date(UserProfile.created_at))
            .all()
        )
        
        return {
            "daily_active_users": [
                {"date": str(date), "users": users}
                for date, users in daily_users
            ],
            "new_users_daily": [
                {"date": str(date), "count": count}
                for date, count in new_users
            ]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving user impact: {str(e)}"
        )


@router.get("/impact/services")
async def get_service_impact(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Get service utilization and impact metrics.
    """
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Services accessed per day
        daily_services = (
            db.query(
                func.date(ServiceAccess.access_date).label("date"),
                func.count(ServiceAccess.id).label("count")
            )
            .filter(ServiceAccess.access_date >= start_date)
            .group_by(func.date(ServiceAccess.access_date))
            .order_by(func.date(ServiceAccess.access_date))
            .all()
        )
        
        # Service outcomes
        outcomes = (
            db.query(
                ServiceAccess.outcome,
                func.count(ServiceAccess.id).label("count")
            )
            .filter(ServiceAccess.access_date >= start_date)
            .group_by(ServiceAccess.outcome)
            .all()
        )
        
        # Contact method breakdown
        contact_methods = (
            db.query(
                ServiceAccess.contact_method,
                func.count(ServiceAccess.id).label("count")
            )
            .filter(ServiceAccess.access_date >= start_date)
            .group_by(ServiceAccess.contact_method)
            .all()
        )
        
        return {
            "daily_service_accesses": [
                {"date": str(date), "count": count}
                for date, count in daily_services
            ],
            "outcomes": [
                {"outcome": outcome or "unknown", "count": count}
                for outcome, count in outcomes
            ],
            "contact_methods": [
                {"method": method or "unknown", "count": count}
                for method, count in contact_methods
            ]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving service impact: {str(e)}"
        )


@router.get("/impact/categories")
async def get_category_impact(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Get impact metrics by service category.
    """
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Services accessed by category
        category_access = (
            db.query(
                SocialService.category,
                func.count(ServiceAccess.id).label("access_count"),
                func.count(func.distinct(ServiceAccess.user_id)).label("unique_users")
            )
            .join(ServiceAccess, ServiceAccess.service_id == SocialService.id)
            .filter(ServiceAccess.access_date >= start_date)
            .group_by(SocialService.category)
            .order_by(func.count(ServiceAccess.id).desc())
            .all()
        )
        
        return {
            "categories": [
                {
                    "category": category,
                    "total_accesses": access_count,
                    "unique_users_served": unique_users
                }
                for category, access_count, unique_users in category_access
            ]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving category impact: {str(e)}"
        )


@router.post("/service-access")
async def log_service_access(
    user_id: str,
    service_id: int,
    service_name: str,
    contact_method: str,
    outcome: Optional[str] = None,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Log that a user accessed a service.
    
    This tracks successful resource connections for impact metrics.
    
    Args:
        user_id: User identifier
        service_id: Service ID
        service_name: Service name
        contact_method: How they contacted (phone, in_person, online)
        outcome: Result (completed, pending, no_show)
        notes: Additional notes
    """
    try:
        access = ServiceAccess(
            user_id=user_id,
            service_id=service_id,
            service_name=service_name,
            contact_method=contact_method,
            outcome=outcome,
            notes=notes
        )
        db.add(access)
        db.commit()
        
        return {
            "success": True,
            "message": "Service access logged",
            "access_id": access.id
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error logging service access: {str(e)}"
        )


@router.get("/health")
async def analytics_health():
    """Health check for analytics API"""
    return {
        "status": "healthy",
        "service": "Analytics API",
        "endpoints": {
            "dashboard": "/api/analytics/stats",
            "user_impact": "/api/analytics/impact/users",
            "service_impact": "/api/analytics/impact/services",
            "category_impact": "/api/analytics/impact/categories"
        }
    }
