# API Usage Examples

## 🔌 Base URL
```
http://localhost:8000/api
```

## 📚 Chat Endpoints

### 1. Send Message to AI Agent

```bash
curl -X POST http://localhost:8000/api/chat/send \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-123",
    "message": "I am homeless and need shelter tonight. I am in downtown area.",
    "user_context": {
      "location": "Downtown, Main Street",
      "needs": ["shelter", "food"],
      "latitude": 40.7128,
      "longitude": -74.0060,
      "eligibility_info": {
        "income_level": "very_low"
      },
      "accessibility_needs": ["mobility"]
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "I found several shelters near you that can help. The Downtown Homeless Shelter is 0.2 miles away and available 24/7...",
  "user_id": "user-123",
  "tools_used": ["search_resources", "check_eligibility"],
  "timestamp": "2024-01-01T12:00:00"
}
```

### 2. Get Chat History

```bash
curl http://localhost:8000/api/chat/history/user-123?limit=10
```

**Response:**
```json
[
  {
    "id": 1,
    "user_message": "I need shelter",
    "agent_response": "Here are the nearest shelters...",
    "tools_used": ["search_resources"],
    "timestamp": "2024-01-01T11:00:00"
  }
]
```

### 3. Submit Feedback on Response

```bash
curl -X POST http://localhost:8000/api/chat/feedback/1 \
  -H "Content-Type: application/json" \
  -d '{
    "helpful": true,
    "feedback_text": "Found the shelter, very helpful!"
  }'
```

### 4. Clear Chat History

```bash
curl -X DELETE http://localhost:8000/api/chat/history/user-123
```

## 🏢 Resource Endpoints

### 1. List All Resources

```bash
curl "http://localhost:8000/api/resources?skip=0&limit=50"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Downtown Homeless Shelter",
    "description": "24-hour shelter with meals, showers, and counseling services",
    "category": "shelter",
    "address": "123 Main St, Downtown City, CA 90210",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "phone": "(555) 123-4567",
    "website": "https://example.com/downtown-shelter",
    "operating_hours": {
      "monday": "24 hours",
      "tuesday": "24 hours"
    },
    "eligibility_criteria": {
      "age_minimum": 18
    },
    "services_provided": ["shelter", "meals", "showers", "counseling"],
    "is_active": true,
    "last_verified": "2024-01-01T00:00:00"
  }
]
```

### 2. Filter Resources by Category

```bash
curl "http://localhost:8000/api/resources?category=shelter&active_only=true"
```

### 3. Get Resources by Category Name

```bash
curl http://localhost:8000/api/resources/category/shelter
```

### 4. Get Single Resource Details

```bash
curl http://localhost:8000/api/resources/1
```

### 5. Search Nearby Resources

```bash
curl "http://localhost:8000/api/resources/search/nearby?latitude=40.7128&longitude=-74.0060&radius_miles=5&category=shelter"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Downtown Homeless Shelter",
    "distance_miles": 0.2,
    "category": "shelter",
    ...
  }
]
```

### 6. Create New Resource

```bash
curl -X POST http://localhost:8000/api/resources/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Service Name",
    "description": "Service description",
    "category": "shelter",
    "address": "456 Oak Ave",
    "latitude": 40.7180,
    "longitude": -74.0050,
    "phone": "(555) 234-5678",
    "website": "https://example.com",
    "operating_hours": {
      "monday": "9AM-5PM",
      "tuesday": "9AM-5PM"
    },
    "eligibility_criteria": {
      "age_minimum": 18
    },
    "services_provided": ["service1", "service2"],
    "is_active": true
  }'
```

### 7. Update Resource

```bash
curl -X PUT http://localhost:8000/api/resources/1 \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "(555) 999-9999",
    "is_active": true
  }'
```

### 8. Delete Resource (Soft Delete)

```bash
curl -X DELETE http://localhost:8000/api/resources/1
```

### 9. Verify/Update Service Information

```bash
curl -X POST http://localhost:8000/api/resources/1/verify
```

## 📊 Analytics Endpoints

### 1. Get Dashboard Statistics

```bash
curl "http://localhost:8000/api/analytics/stats?days=30"
```

**Response:**
```json
{
  "total_users": 150,
  "total_conversations": 450,
  "total_services_accessed": 200,
  "unique_services_used": 8,
  "average_messages_per_user": 3.0,
  "most_accessed_services": [
    {
      "service": "Downtown Homeless Shelter",
      "count": 45
    }
  ],
  "most_requested_categories": [
    {
      "category": "shelter",
      "count": 120
    }
  ],
  "helpful_response_rate": 87.5
}
```

### 2. Get User Impact Metrics

```bash
curl "http://localhost:8000/api/analytics/impact/users?days=30"
```

**Response:**
```json
{
  "daily_active_users": [
    {
      "date": "2024-01-01",
      "users": 45
    }
  ],
  "new_users_daily": [
    {
      "date": "2024-01-01",
      "count": 12
    }
  ]
}
```

### 3. Get Service Impact Metrics

```bash
curl "http://localhost:8000/api/analytics/impact/services?days=30"
```

**Response:**
```json
{
  "daily_service_accesses": [
    {
      "date": "2024-01-01",
      "count": 25
    }
  ],
  "outcomes": [
    {
      "outcome": "completed",
      "count": 180
    },
    {
      "outcome": "pending",
      "count": 15
    }
  ],
  "contact_methods": [
    {
      "method": "phone",
      "count": 120
    }
  ]
}
```

### 4. Get Category Impact Metrics

```bash
curl "http://localhost:8000/api/analytics/impact/categories?days=30"
```

**Response:**
```json
{
  "categories": [
    {
      "category": "shelter",
      "total_accesses": 120,
      "unique_users_served": 80
    },
    {
      "category": "food",
      "total_accesses": 60,
      "unique_users_served": 50
    }
  ]
}
```

### 5. Log Service Access

```bash
curl -X POST http://localhost:8000/api/analytics/service-access \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-123",
    "service_id": 1,
    "service_name": "Downtown Homeless Shelter",
    "contact_method": "phone",
    "outcome": "completed",
    "notes": "User successfully accessed shelter services"
  }'
```

## 🏥 Health Check

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "app": "Community Resource Navigation AI",
  "debug": true
}
```

## 📖 Interactive API Documentation

Once running, visit: **http://localhost:8000/docs**

This provides an interactive Swagger UI where you can:
- Try all endpoints
- See request/response examples
- View parameter requirements
- Test with real data

## 🔐 Authentication (Future)

Currently, all endpoints are public. For production, add:

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/protected")
async def protected_route(credentials = Depends(security)):
    # Verify token
    return {"data": "protected"}
```

## 📱 Example: Complete User Journey

```bash
# 1. User sends message to AI
curl -X POST http://localhost:8000/api/chat/send \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "john-doe",
    "message": "I need food help",
    "user_context": {
      "location": "Downtown",
      "needs": ["food"],
      "latitude": 40.7128,
      "longitude": -74.0060
    }
  }'

# 2. User gets recommendations and views resource details
curl http://localhost:8000/api/resources/2

# 3. User accesses the service
curl -X POST http://localhost:8000/api/analytics/service-access \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "john-doe",
    "service_id": 2,
    "service_name": "Community Food Bank",
    "contact_method": "in_person",
    "outcome": "completed"
  }'

# 4. View impact of help provided
curl http://localhost:8000/api/analytics/stats?days=1
```

---

**Try these examples in your terminal or use the interactive Swagger UI at /docs!**
