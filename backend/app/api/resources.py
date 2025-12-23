"""
Resources API endpoints for CRUD operations on community services
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import SocialService
from datetime import datetime

router = APIRouter()


class ServiceCreate(BaseModel):
    """Schema for creating a new service"""
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(...)
    category: str = Field(..., min_length=1, max_length=50)
    address: str = Field(...)
    latitude: float
    longitude: float
    phone: Optional[str] = None
    website: Optional[str] = None
    operating_hours: Optional[Dict[str, str]] = None
    eligibility_criteria: Optional[Dict[str, Any]] = None
    services_provided: Optional[List[str]] = None
    is_active: bool = True


class ServiceUpdate(BaseModel):
    """Schema for updating a service"""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    operating_hours: Optional[Dict[str, str]] = None
    eligibility_criteria: Optional[Dict[str, Any]] = None
    services_provided: Optional[List[str]] = None
    is_active: Optional[bool] = None


class ServiceResponse(BaseModel):
    """Schema for service response"""
    id: int
    name: str
    description: str
    category: str
    address: str
    latitude: float
    longitude: float
    phone: Optional[str]
    website: Optional[str]
    operating_hours: Optional[Dict[str, str]]
    eligibility_criteria: Optional[Dict[str, Any]]
    services_provided: Optional[List[str]]
    is_active: bool
    last_verified: Optional[datetime]
    created_at: Optional[datetime]


@router.post("/", response_model=ServiceResponse)
async def create_service(
    service: ServiceCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new community service resource.
    
    Requires:
    - name: Service name
    - description: Detailed description
    - category: Type of service (shelter, food, health, etc.)
    - address, latitude, longitude: Location
    """
    try:
        new_service = SocialService(**service.model_dump())
        db.add(new_service)
        db.commit()
        db.refresh(new_service)
        return new_service
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error creating service: {str(e)}"
        )


@router.get("/", response_model=List[ServiceResponse])
async def list_services(
    category: Optional[str] = Query(None, description="Filter by category"),
    active_only: bool = Query(True, description="Only show active services"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    List all community services with optional filters.
    
    Query Parameters:
    - category: Filter by service category (shelter, food, health, employment, etc.)
    - active_only: Show only active services (default: true)
    - skip: Number of results to skip (pagination)
    - limit: Number of results to return (max 100)
    """
    try:
        query = db.query(SocialService)
        
        if active_only:
            query = query.filter(SocialService.is_active == True)
        
        if category:
            query = query.filter(SocialService.category.ilike(f"%{category}%"))
        
        services = query.offset(skip).limit(limit).all()
        return services
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error listing services: {str(e)}"
        )


@router.get("/{service_id}", response_model=ServiceResponse)
async def get_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific service.
    
    Args:
        service_id: The ID of the service
    """
    try:
        service = db.query(SocialService).filter(SocialService.id == service_id).first()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        return service
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error retrieving service: {str(e)}"
        )


@router.put("/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: int,
    service_update: ServiceUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a community service resource.
    
    Args:
        service_id: The ID of the service to update
        service_update: Fields to update
    """
    try:
        service = db.query(SocialService).filter(SocialService.id == service_id).first()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        
        update_data = service_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(service, field, value)
        
        service.last_verified = datetime.utcnow()
        db.commit()
        db.refresh(service)
        return service
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error updating service: {str(e)}"
        )


@router.delete("/{service_id}")
async def delete_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a service (soft delete - marks as inactive).
    
    Args:
        service_id: The ID of the service to delete
    """
    try:
        service = db.query(SocialService).filter(SocialService.id == service_id).first()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        
        service.is_active = False
        db.commit()
        
        return {"success": True, "message": f"Service {service_id} marked as inactive"}
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error deleting service: {str(e)}"
        )


@router.get("/category/{category_name}", response_model=List[ServiceResponse])
async def get_services_by_category(
    category_name: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all services in a specific category.
    
    Common categories:
    - shelter
    - food
    - health
    - employment
    - mental_health
    - legal
    - substance_abuse
    - youth
    """
    try:
        services = (
            db.query(SocialService)
            .filter(
                (SocialService.category.ilike(f"%{category_name}%")) &
                (SocialService.is_active == True)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        if not services:
            raise HTTPException(
                status_code=404,
                detail=f"No services found in category: {category_name}"
            )
        
        return services
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error retrieving services: {str(e)}"
        )


@router.post("/{service_id}/verify")
async def verify_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    """
    Mark a service as recently verified/updated.
    
    Args:
        service_id: The ID of the service
    """
    try:
        service = db.query(SocialService).filter(SocialService.id == service_id).first()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        
        service.last_verified = datetime.utcnow()
        db.commit()
        
        return {
            "success": True,
            "message": f"Service {service_id} verified",
            "last_verified": service.last_verified.isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error verifying service: {str(e)}"
        )


@router.get("/search/nearby", response_model=List[ServiceResponse])
async def search_nearby(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius_miles: float = Query(5.0, ge=0.1, le=50),
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Search for services near a specific location.
    
    Args:
        latitude: User's latitude
        longitude: User's longitude
        radius_miles: Search radius in miles (default 5, max 50)
        category: Optional category filter
    """
    try:
        # Get all active services
        query = db.query(SocialService).filter(SocialService.is_active == True)
        
        if category:
            query = query.filter(SocialService.category.ilike(f"%{category}%"))
        
        services = query.all()
        
        # Calculate distances and filter
        import math
        nearby = []
        
        for service in services:
            if service.latitude and service.longitude:
                # Haversine formula
                lat1_rad = math.radians(latitude)
                lat2_rad = math.radians(service.latitude)
                delta_lat = math.radians(service.latitude - latitude)
                delta_lon = math.radians(service.longitude - longitude)
                
                a = math.sin(delta_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)**2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                distance_miles = 3959 * c  # Earth's radius in miles
                
                if distance_miles <= radius_miles:
                    nearby.append((service, distance_miles))
        
        # Sort by distance
        nearby.sort(key=lambda x: x[1])
        
        return [service for service, _ in nearby]
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error searching nearby services: {str(e)}"
        )


@router.get("/search/locations")
async def search_locations(
    query: str = Query(..., min_length=1, max_length=100),
    db: Session = Depends(get_db)
):
    """
    Search for available locations (cities) where services are available.
    
    Args:
        query: Search query (e.g., "Hyderabad", "Delhi")
    
    Returns:
        List of available cities/locations with coordinates
    """
    try:
        # Extract unique cities/locations from service addresses
        services = db.query(SocialService).filter(SocialService.is_active == True).all()
        
        locations = {}
        for service in services:
            if service.address and service.latitude and service.longitude:
                # Extract city from address (simplified - usually after the last comma)
                address_parts = service.address.split(',')
                city = address_parts[-2].strip() if len(address_parts) > 1 else address_parts[0].strip()
                
                # Check if query matches city name (case insensitive)
                if query.lower() in city.lower():
                    if city not in locations:
                        locations[city] = {
                            "city": city,
                            "latitude": service.latitude,
                            "longitude": service.longitude,
                            "service_count": 0
                        }
                    locations[city]["service_count"] += 1
        
        result = list(locations.values())
        return result if result else [{"message": "No locations found matching your search"}]
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error searching locations: {str(e)}"
        )
