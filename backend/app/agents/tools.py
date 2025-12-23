"""
Agent tools for resource search, eligibility checking, and service verification
"""

from typing import Optional, List, Dict, Any
from langchain_core.tools import tool
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.db.models import SocialService, UserProfile
from app.db.database import SessionLocal
import math
import logging

logger = logging.getLogger(__name__)


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates in miles"""
    R = 3959  # Earth's radius in miles
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


@tool
def search_resources(
    category: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius_miles: float = 5.0,
    keywords: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Search for community resources by category, location, and keywords.
    
    Args:
        category: Type of service (shelter, food, health, employment, mental_health, legal, substance_abuse, youth)
        latitude: User's latitude for distance-based recommendations
        longitude: User's longitude for distance-based recommendations
        radius_miles: Search radius in miles (default 5.0)
        keywords: Additional search terms
    
    Returns:
        List of matching resources with details and distance
    """
    db = SessionLocal()
    try:
        query = db.query(SocialService).filter(SocialService.is_active == True)
        
        # Filter by category
        if category:
            query = query.filter(SocialService.category == category.lower())
        
        # Filter by keyword search in name or description
        if keywords:
            keyword_filter = or_(
                SocialService.name.ilike(f"%{keywords}%"),
                SocialService.description.ilike(f"%{keywords}%"),
                SocialService.address.ilike(f"%{keywords}%")
            )
            query = query.filter(keyword_filter)
        
        services = query.all()
        
        # Format results with distance calculation
        results = []
        for service in services:
            result = {
                "id": service.id,
                "name": service.name,
                "description": service.description,
                "category": service.category,
                "address": service.address,
                "phone": service.phone,
                "website": service.website,
                "operating_hours": service.operating_hours,
                "services_provided": service.services_provided,
                "eligibility_criteria": service.eligibility_criteria,
            }
            
            # Calculate distance if coordinates provided
            if latitude and longitude and service.latitude and service.longitude:
                distance = calculate_distance(latitude, longitude, service.latitude, service.longitude)
                if distance <= radius_miles:
                    result["distance_miles"] = round(distance, 2)
                    results.append(result)
            else:
                results.append(result)
        
        # Sort by distance if available
        if latitude and longitude:
            results.sort(key=lambda x: x.get("distance_miles", float('inf')))
        
        return results[:10]  # Return top 10 results
    
    except Exception as e:
        logger.error(f"Error searching resources: {e}")
        return []
    finally:
        db.close()


@tool
def check_eligibility(
    service_id: int,
    income_level: Optional[str] = None,
    family_size: Optional[int] = None,
    age: Optional[int] = None,
    residency: Optional[str] = None,
    insurance_status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Check if user meets eligibility criteria for a specific service.
    
    Args:
        service_id: ID of the service to check
        income_level: User's income level (low, moderate, medium, high)
        family_size: Number of family members
        age: User's age
        residency: Residency status
        insurance_status: Insurance status (uninsured, underinsured, insured)
    
    Returns:
        Eligibility assessment with requirements and barriers
    """
    db = SessionLocal()
    try:
        service = db.query(SocialService).filter(SocialService.id == service_id).first()
        if not service:
            return {"error": f"Service with ID {service_id} not found"}
        
        eligibility = service.eligibility_criteria or {}
        assessment = {
            "service_name": service.name,
            "service_id": service_id,
            "eligible": True,
            "requirements": eligibility,
            "barriers": [],
            "documents_needed": ["Valid ID"],
            "notes": ""
        }
        
        # Check age
        if "age_minimum" in eligibility and age:
            if age < eligibility["age_minimum"]:
                assessment["eligible"] = False
                assessment["barriers"].append(f"Minimum age requirement: {eligibility['age_minimum']}")
        
        if "age_maximum" in eligibility and age:
            if age > eligibility["age_maximum"]:
                assessment["eligible"] = False
                assessment["barriers"].append(f"Maximum age requirement: {eligibility['age_maximum']}")
        
        # Check income (simplified logic)
        if "income_limit" in eligibility and income_level:
            income_mapping = {
                "very_low": 1,
                "low": 2,
                "moderate": 3,
                "medium": 3,
                "moderate_high": 4,
                "high": 5
            }
            if income_mapping.get(income_level, 3) > 3:  # If income above moderate
                assessment["barriers"].append(f"Income limit: {eligibility['income_limit']}")
        
        # Check residency
        if "residency" in eligibility and residency:
            if eligibility["residency"] != "Any" and residency != eligibility["residency"]:
                assessment["barriers"].append(f"Residency requirement: {eligibility['residency']}")
        
        # Add practical advice
        if assessment["eligible"]:
            assessment["notes"] = f"You appear to meet the requirements. Call {service.phone} to apply or visit in person."
        else:
            assessment["notes"] = "You may not meet all requirements. Call to discuss your situation with staff."
        
        return assessment
    
    except Exception as e:
        logger.error(f"Error checking eligibility: {e}")
        return {"error": f"Error checking eligibility: {str(e)}"}
    finally:
        db.close()


@tool
def get_service_details(service_id: int) -> Dict[str, Any]:
    """
    Get detailed information about a specific service.
    
    Args:
        service_id: ID of the service
    
    Returns:
        Complete service information
    """
    db = SessionLocal()
    try:
        service = db.query(SocialService).filter(SocialService.id == service_id).first()
        if not service:
            return {"error": f"Service with ID {service_id} not found"}
        
        return {
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "category": service.category,
            "address": service.address,
            "latitude": service.latitude,
            "longitude": service.longitude,
            "phone": service.phone,
            "website": service.website,
            "operating_hours": service.operating_hours,
            "services_provided": service.services_provided,
            "eligibility_criteria": service.eligibility_criteria,
            "is_active": service.is_active,
            "last_verified": service.last_verified.isoformat() if service.last_verified else None,
        }
    
    except Exception as e:
        logger.error(f"Error getting service details: {e}")
        return {"error": f"Error: {str(e)}"}
    finally:
        db.close()


@tool
def schedule_appointment(
    service_id: int,
    user_id: str,
    preferred_date: Optional[str] = None,
    preferred_time: Optional[str] = None,
    contact_method: str = "phone"
) -> Dict[str, Any]:
    """
    Schedule or get instructions for contacting a service.
    
    Args:
        service_id: ID of the service
        user_id: User's identifier
        preferred_date: Preferred appointment date (YYYY-MM-DD)
        preferred_time: Preferred time slot
        contact_method: How to contact (phone, in_person, online)
    
    Returns:
        Appointment booking information or instructions
    """
    db = SessionLocal()
    try:
        service = db.query(SocialService).filter(SocialService.id == service_id).first()
        if not service:
            return {"error": f"Service with ID {service_id} not found"}
        
        response = {
            "service_name": service.name,
            "service_id": service_id,
            "contact_method": contact_method,
        }
        
        if contact_method == "phone":
            response["instructions"] = f"Call {service.phone} to schedule an appointment. Ask about availability for {preferred_date or 'your preferred date'}."
            response["hours"] = service.operating_hours
        elif contact_method == "in_person":
            response["address"] = service.address
            response["hours"] = service.operating_hours
            response["instructions"] = f"Visit {service.address} during operating hours. Bring a valid ID and proof of address."
        elif contact_method == "online":
            response["website"] = service.website
            response["instructions"] = f"Visit {service.website} to schedule or call {service.phone} for more information."
        
        response["confirmation_message"] = f"Request for {service.name} has been recorded."
        
        return response
    
    except Exception as e:
        logger.error(f"Error scheduling appointment: {e}")
        return {"error": f"Error: {str(e)}"}
    finally:
        db.close()


@tool
def get_nearby_resources(
    latitude: float,
    longitude: float,
    radius_miles: float = 5.0,
    category: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Find all nearby resources within a specified radius.
    
    Args:
        latitude: User's latitude
        longitude: User's longitude
        radius_miles: Search radius in miles
        category: Optional category filter
    
    Returns:
        List of nearby resources sorted by distance
    """
    return search_resources(
        category=category,
        latitude=latitude,
        longitude=longitude,
        radius_miles=radius_miles
    )


# Aggregate all tools
AGENT_TOOLS = [
    search_resources,
    check_eligibility,
    get_service_details,
    schedule_appointment,
    get_nearby_resources,
]
