"""
Seed data for community resources database
Contains example social services across different categories
"""

from sqlalchemy.orm import Session
from datetime import datetime
from app.db.models import SocialService, Base
from app.db.database import SessionLocal, engine
import logging

logger = logging.getLogger(__name__)

# Sample community resources - India focused (Hyderabad & Delhi)
SEED_RESOURCES = [
    # HYDERABAD SHELTERS
    {
        "name": "Hyderabad Homeless Shelter - Begumpet",
        "description": "24-hour shelter with meals, showers, counseling and job placement services",
        "category": "shelter",
        "address": "Begumpet, Hyderabad, Telangana 500016",
        "latitude": 17.3718,
        "longitude": 78.4680,
        "phone": "+91-40-2335-6789",
        "website": "https://example.com/hyderabad-shelter",
        "operating_hours": {
            "monday": "24 hours",
            "tuesday": "24 hours",
            "wednesday": "24 hours",
            "thursday": "24 hours",
            "friday": "24 hours",
            "saturday": "24 hours",
            "sunday": "24 hours"
        },
        "eligibility_criteria": {
            "age_minimum": 18,
            "residency": "Any",
            "income_limit": "No limit",
            "nationality": "Any"
        },
        "services_provided": ["shelter", "meals", "showers", "counseling", "case_management", "job_training"],
        "is_active": True
    },
    {
        "name": "Food Security Initiative - Hyderabad",
        "description": "Provides daily meals and nutritional support for homeless and vulnerable people",
        "category": "food",
        "address": "Secunderabad, Hyderabad, Telangana 500003",
        "latitude": 17.3688,
        "longitude": 78.5016,
        "phone": "+91-40-2334-5678",
        "website": "https://example.com/food-security",
        "operating_hours": {
            "monday": "7AM-9PM",
            "tuesday": "7AM-9PM",
            "wednesday": "7AM-9PM",
            "thursday": "7AM-9PM",
            "friday": "7AM-9PM",
            "saturday": "7AM-9PM",
            "sunday": "7AM-9PM"
        },
        "eligibility_criteria": {
            "documentation": "No ID required",
            "income_limit": "None"
        },
        "services_provided": ["meal_programs", "nutrition_counseling", "food_pantry"],
        "is_active": True
    },
    {
        "name": "Hyderabad Public Health Center",
        "description": "Free healthcare clinic with OPD, vaccinations, and emergency services",
        "category": "health",
        "address": "Panjagutta, Hyderabad, Telangana 500482",
        "latitude": 17.3847,
        "longitude": 78.4735,
        "phone": "+91-40-2330-6789",
        "website": "https://example.com/health-center",
        "operating_hours": {
            "monday": "8AM-6PM",
            "tuesday": "8AM-6PM",
            "wednesday": "8AM-6PM",
            "thursday": "8AM-6PM",
            "friday": "8AM-4PM",
            "saturday": "9AM-1PM",
            "sunday": "Closed"
        },
        "eligibility_criteria": {
            "income_limit": "No limit",
            "insurance_status": "Not required",
            "age": "All ages"
        },
        "services_provided": ["primary_care", "emergency_services", "vaccination", "maternal_health"],
        "is_active": True
    },
    {
        "name": "Hyderabad Skills Training Center",
        "description": "Free vocational training for employment in IT, construction, and hospitality",
        "category": "employment",
        "address": "HITEC City, Hyderabad, Telangana 500081",
        "latitude": 17.3604,
        "longitude": 78.4390,
        "phone": "+91-40-2345-6789",
        "website": "https://example.com/training-center",
        "operating_hours": {
            "monday": "10AM-6PM",
            "tuesday": "10AM-6PM",
            "wednesday": "10AM-6PM",
            "thursday": "10AM-6PM",
            "friday": "10AM-5PM",
            "saturday": "10AM-2PM",
            "sunday": "Closed"
        },
        "eligibility_criteria": {
            "employment_status": "Any",
            "age_minimum": 18,
            "income_limit": "No limit"
        },
        "services_provided": ["vocational_training", "skill_development", "job_placement", "internship"],
        "is_active": True
    },
    # DELHI SHELTERS
    {
        "name": "Delhi Night Shelter - Kasturba Nagar",
        "description": "24-hour shelter for homeless with meals, medical aid and skill training",
        "category": "shelter",
        "address": "Kasturba Nagar, New Delhi, Delhi 110065",
        "latitude": 28.5355,
        "longitude": 77.2707,
        "phone": "+91-11-2332-5678",
        "website": "https://example.com/delhi-shelter",
        "operating_hours": {
            "monday": "24 hours",
            "tuesday": "24 hours",
            "wednesday": "24 hours",
            "thursday": "24 hours",
            "friday": "24 hours",
            "saturday": "24 hours",
            "sunday": "24 hours"
        },
        "eligibility_criteria": {
            "age_minimum": 13,
            "housing_status": "Homeless",
            "documentation": "Optional"
        },
        "services_provided": ["shelter", "meals", "medical_aid", "skill_training", "counseling"],
        "is_active": True
    },
    {
        "name": "Delhi Food Security Program",
        "description": "Free meal distribution and nutrition programs for vulnerable populations",
        "category": "food",
        "address": "Connaught Place, New Delhi, Delhi 110001",
        "latitude": 28.6295,
        "longitude": 77.1895,
        "phone": "+91-11-2303-5678",
        "website": "https://example.com/delhi-food",
        "operating_hours": {
            "monday": "6AM-9PM",
            "tuesday": "6AM-9PM",
            "wednesday": "6AM-9PM",
            "thursday": "6AM-9PM",
            "friday": "6AM-9PM",
            "saturday": "6AM-9PM",
            "sunday": "6AM-9PM"
        },
        "eligibility_criteria": {
            "documentation": "No ID required",
            "income_limit": "None"
        },
        "services_provided": ["meal_distribution", "nutrition_education", "food_bank"],
        "is_active": True
    },
    {
        "name": "Delhi Public Health Clinic",
        "description": "Free government healthcare with OPD, emergency services, and chronic disease management",
        "category": "health",
        "address": "Mandi House, New Delhi, Delhi 110001",
        "latitude": 28.6140,
        "longitude": 77.2297,
        "phone": "+91-11-2330-6789",
        "website": "https://example.com/delhi-health",
        "operating_hours": {
            "monday": "8AM-8PM",
            "tuesday": "8AM-8PM",
            "wednesday": "8AM-8PM",
            "thursday": "8AM-8PM",
            "friday": "8AM-8PM",
            "saturday": "9AM-2PM",
            "sunday": "10AM-2PM"
        },
        "eligibility_criteria": {
            "age": "All ages",
            "insurance_status": "Not required",
            "income_limit": "No limit"
        },
        "services_provided": ["OPD", "emergency_services", "chronic_disease_management", "vaccination"],
        "is_active": True
    },
    {
        "name": "Delhi Skill Development Institute",
        "description": "Free vocational and skill training programs for employment",
        "category": "employment",
        "address": "Rajouri Garden, New Delhi, Delhi 110027",
        "latitude": 28.6661,
        "longitude": 77.0595,
        "phone": "+91-11-2345-6789",
        "website": "https://example.com/delhi-training",
        "operating_hours": {
            "monday": "10AM-6PM",
            "tuesday": "10AM-6PM",
            "wednesday": "10AM-6PM",
            "thursday": "10AM-6PM",
            "friday": "10AM-5PM",
            "saturday": "10AM-2PM",
            "sunday": "Closed"
        },
        "eligibility_criteria": {
            "age_minimum": 18,
            "income_limit": "No limit"
        },
        "services_provided": ["vocational_training", "skill_certification", "job_placement", "apprenticeship"],
        "is_active": True
    },
    {
        "name": "Delhi Mental Health Support Center",
        "description": "24/7 crisis counseling and mental health support services",
        "category": "mental_health",
        "address": "Ram Manohar Lohia Hospital Campus, New Delhi, Delhi 110001",
        "latitude": 28.5940,
        "longitude": 77.2070,
        "phone": "+91-11-4141-2000",
        "website": "https://example.com/delhi-mental-health",
        "operating_hours": {
            "monday": "24 hours",
            "tuesday": "24 hours",
            "wednesday": "24 hours",
            "thursday": "24 hours",
            "friday": "24 hours",
            "saturday": "24 hours",
            "sunday": "24 hours"
        },
        "eligibility_criteria": {
            "age": "13+",
            "insurance": "Not required"
        },
        "services_provided": ["crisis_support", "counseling", "psychiatric_care", "group_therapy"],
        "is_active": True
    }
]


def seed_database():
    """Populate database with initial community resources"""
    # Create all tables first
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    
    db = SessionLocal()
    try:
        # Check if data already exists
        existing_count = db.query(SocialService).count()
        if existing_count > 0:
            logger.info(f"Database already contains {existing_count} resources. Skipping seed.")
            return
        
        # Add all resources
        for resource_data in SEED_RESOURCES:
            service = SocialService(
                **resource_data,
                last_verified=datetime.utcnow()
            )
            db.add(service)
        
        db.commit()
        logger.info(f"Successfully seeded {len(SEED_RESOURCES)} resources into database")
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
