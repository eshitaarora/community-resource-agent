# Community Resource Navigation AI Agent - Complete Implementation

This is a fully-fledged, production-ready AI agent system designed to help vulnerable populations find critical social services.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Deployment](#deployment)

## 🚀 Quick Start

### Using Docker Compose (Recommended)

```bash
# Clone repository
git clone <repo-url>
cd community-resource-agent

# Copy environment template
cp backend/.env.example backend/.env

# Edit .env with your API keys
nano backend/.env

# Start all services
docker-compose up -d

# Application will be available at:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Local Development

#### Backend Setup

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
nano .env  # Add your API keys

# Initialize database
python -m app.db.seed_data

# Run server
uvicorn app.main:app --reload
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Application available at http://localhost:3000
```

## ✨ Features

### 1. **Intelligent AI Agent**
- Multi-turn conversations with context awareness
- Understands user needs and circumstances
- Natural language processing powered by GPT-4
- Tool-calling agents for precise resource matching

### 2. **Comprehensive Resource Search**
- Search by category (shelter, food, health, employment, etc.)
- Geolocation-based nearby resource discovery
- Eligibility matching based on income, age, residency
- Operating hours and contact information

### 3. **User Profile Management**
- Track location and service needs
- Store eligibility information
- Record accessibility requirements
- Personalized recommendations

### 4. **Analytics Dashboard**
- Real-time impact metrics
- User engagement tracking
- Service utilization statistics
- Category-wise analysis
- Outcome tracking (completed, pending, no-show)

### 5. **Multi-Interface Access**
- Web chat interface
- Resource browser with detailed information
- User profile management
- Impact dashboard

## 🏗️ Architecture

```
Community Resource Agent
├── Backend (FastAPI + LangChain)
│   ├── API Endpoints
│   │   ├── /api/chat - Conversational AI
│   │   ├── /api/resources - CRUD operations
│   │   └── /api/analytics - Impact metrics
│   ├── AI Agent
│   │   ├── LangChain Agent with Tool Calling
│   │   ├── Vector search & embedding
│   │   └── Conversation memory
│   ├── Database
│   │   ├── PostgreSQL (services, users, messages)
│   │   └── Redis (caching, session management)
│   └── Tools
│       ├── Resource search
│       ├── Eligibility checking
│       ├── Service verification
│       └── Appointment scheduling
│
├── Frontend (React + Vite)
│   ├── Pages
│   │   ├── Chat Interface
│   │   ├── Resource Browser
│   │   ├── User Profile
│   │   └── Dashboard
│   ├── Components
│   │   ├── ChatInterface
│   │   ├── ResourceBrowser
│   │   └── UserProfile
│   ├── Store (Zustand)
│   └── API Client
│
└── Infrastructure
    ├── Docker & Docker Compose
    ├── PostgreSQL Database
    ├── Redis Cache
    └── Nginx Proxy
```

## 📦 Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)
- PostgreSQL 13+ (if not using Docker)
- Redis (if not using Docker)

### Backend Installation

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -m app.db.seed_data

# Run migrations (if needed)
alembic upgrade head
```

### Frontend Installation

```bash
cd frontend

# Install dependencies
npm install

# Build for production
npm run build
```

## ⚙️ Configuration

### Environment Variables

Create `backend/.env` based on `backend/.env.example`:

```bash
# Required
OPENAI_API_KEY=sk-your-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/community_resources

# Optional
GOOGLE_MAPS_API_KEY=your-key
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_PHONE=+1234567890
```

### Database Configuration

The system uses PostgreSQL with SQLAlchemy ORM. Tables are automatically created on startup.

**Seed Data**: Default community resources are loaded from `backend/app/db/seed_data.py`. Customize by editing this file.

## 📚 API Documentation

### Chat Endpoints

#### Send Message
```
POST /api/chat/send
Content-Type: application/json

{
  "user_id": "user-123",
  "message": "I need help finding shelter",
  "user_context": {
    "location": "Downtown, City",
    "needs": ["shelter", "food"],
    "eligibility_info": {"income_level": "very_low"},
    "accessibility_needs": ["mobility"]
  }
}

Response:
{
  "success": true,
  "message": "Here are the shelters near you...",
  "user_id": "user-123",
  "tools_used": ["search_resources", "check_eligibility"]
}
```

#### Get Chat History
```
GET /api/chat/history/{user_id}?limit=10

Response:
[
  {
    "id": 1,
    "user_message": "...",
    "agent_response": "...",
    "tools_used": [...],
    "timestamp": "2024-01-01T12:00:00"
  }
]
```

### Resource Endpoints

#### List Resources
```
GET /api/resources?category=shelter&skip=0&limit=50

Response:
[
  {
    "id": 1,
    "name": "Downtown Shelter",
    "category": "shelter",
    "address": "123 Main St",
    "phone": "(555) 123-4567",
    "operating_hours": {...},
    "eligibility_criteria": {...}
  }
]
```

#### Search Nearby
```
GET /api/resources/search/nearby?latitude=40.7128&longitude=-74.0060&radius_miles=5

Response: [List of nearby services]
```

### Analytics Endpoints

#### Dashboard Stats
```
GET /api/analytics/stats?days=30

Response:
{
  "total_users": 150,
  "total_conversations": 450,
  "total_services_accessed": 200,
  "helpful_response_rate": 87.5,
  "most_accessed_services": [...]
}
```

## 🛠️ Development

### Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Configuration
│   ├── agents/
│   │   ├── llm_config.py       # OpenAI setup
│   │   ├── tools.py            # Agent tools
│   │   └── resource_agent.py   # Main agent logic
│   ├── api/
│   │   ├── chat.py             # Chat endpoints
│   │   ├── resources.py        # Resource CRUD
│   │   └── analytics.py        # Analytics endpoints
│   └── db/
│       ├── models.py           # SQLAlchemy models
│       ├── database.py         # DB setup
│       └── seed_data.py        # Initial data
├── requirements.txt
└── Dockerfile

frontend/
├── src/
│   ├── components/
│   │   ├── ChatInterface.jsx
│   │   ├── ResourceBrowser.jsx
│   │   └── UserProfile.jsx
│   ├── pages/
│   │   └── Dashboard.jsx
│   ├── services/
│   │   └── api.js              # API client
│   ├── store/
│   │   └── index.js            # State management
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── package.json
├── vite.config.js
└── index.html
```

### Adding New Resources

Edit `backend/app/db/seed_data.py` and add to `SEED_RESOURCES` array:

```python
{
    "name": "New Service Name",
    "description": "...",
    "category": "shelter",
    "address": "...",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "phone": "...",
    "website": "...",
    "operating_hours": {"monday": "9AM-5PM", ...},
    "eligibility_criteria": {...},
    "services_provided": [...],
    "is_active": True
}
```

### Extending the Agent

Add new tools in `backend/app/agents/tools.py`:

```python
@tool
def my_new_tool(param1: str) -> Dict[str, Any]:
    """
    Tool description
    """
    # Implementation
    return result

# Add to AGENT_TOOLS
AGENT_TOOLS = [
    ...,
    my_new_tool,
]
```

## 🚀 Deployment

### Docker Compose Production

```bash
# Build images
docker-compose build

# Start services
docker-compose -f docker-compose.yml up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Environment Variables for Production

```bash
DEBUG=False
OPENAI_MODEL=gpt-4-turbo-preview
ALLOWED_ORIGINS=["https://yourdomain.com"]
DATABASE_URL=postgresql://user:pass@prod-db:5432/resources
REDIS_URL=redis://prod-redis:6379/0
```

### Health Checks

- Backend: `GET /health`
- Frontend: `GET /`
- Database: Automatic PostgreSQL health check
- Redis: Automatic Redis health check

### Scaling

The architecture supports horizontal scaling:

1. **Database**: Use managed PostgreSQL (AWS RDS, GCP Cloud SQL)
2. **Cache**: Use managed Redis (AWS ElastiCache, Azure Cache)
3. **API**: Deploy multiple backend instances behind load balancer
4. **Frontend**: Deploy to CDN (Cloudflare, AWS CloudFront)

## 📊 Monitoring

Key metrics to monitor:

- Chat response latency
- User engagement (conversations/day)
- Service access success rate
- AI response helpfulness rate
- Resource search accuracy
- System uptime and errors

## 🔒 Security

- CORS enabled for specified origins
- Input validation on all endpoints
- Database parameterized queries (SQLAlchemy ORM)
- Environment variable secrets management
- Non-root Docker user
- HTTPS ready (configure in nginx.conf)

## 📝 License

[Your License Here]

## 🤝 Contributing

Contributions welcome! Please follow:

1. Create feature branch
2. Make changes
3. Submit pull request
4. Ensure tests pass

## 📞 Support

For issues or questions:
- Open GitHub issue
- Contact development team
- Email: support@example.com

---

**Built with ❤️ for vulnerable populations in need of critical resources.**
