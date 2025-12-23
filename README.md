# Community Resource Navigation AI Agent

An intelligent, agentic AI system that helps vulnerable populations discover and access critical social services. Built with modern AI/ML practices, this project demonstrates real-world impact through technology.

## 🎯 Problem Statement

Over 600,000+ people experience homelessness in the India. Millions struggle with food insecurity, lack access to healthcare, and don't know where to find job training. Information about social services is fragmented, hard to discover, and often outdated. 

**Our Solution:** An AI agent that acts like a knowledgeable social worker—understanding context, searching available resources, verifying relevance, and guiding people to help.

## ✨ Key Features

### 1. **Agentic AI System**
- Multi-tool AI agent using LangChain
- Tools: Resource search, service verification, eligibility checking, appointment scheduling
- Conversational understanding of user needs (homelessness, hunger, health, employment)
- Context-aware recommendations based on location, eligibility, and urgency

### 2. **Intelligent Resource Search**
- RAG (Retrieval-Augmented Generation) over community resources
- Real-time service availability & operating hours
- Eligibility matching (income levels, residency, age requirements)
- Distance-based recommendations with transit information

### 3. **Impact Dashboard**
- Track individuals helped through the system
- Service effectiveness metrics
- Geographic hotspot analysis
- Crisis response patterns

### 4. **Accessibility First**
- SMS/Text interface for those without smartphones
- Multi-language support (English, Spanish, Mandarin)
- WCAG 2.1 AA compliant web interface
- Offline support for essential information

## 🏗️ Architecture

```
community-resource-agent/
├── backend/                    # FastAPI + LangChain
│   ├── app/
│   │   ├── agents/            # AI agent logic
│   │   │   ├── resource_agent.py
│   │   │   ├── tools.py
│   │   │   └── llm_config.py
│   │   ├── api/               # REST endpoints
│   │   │   ├── chat.py
│   │   │   ├── resources.py
│   │   │   └── analytics.py
│   │   ├── db/                # Database layer
│   │   │   ├── models.py
│   │   │   ├── database.py
│   │   │   └── seed_data.py
│   │   ├── main.py
│   │   └── config.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                   # React + TypeScript
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.tsx
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🚀 Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **AI/ML**: LangChain, OpenAI API, FAISS (vector search)
- **Database**: PostgreSQL + pgvector extension (vector embeddings)
- **Frontend**: React 18, TypeScript, Tailwind CSS
- **DevOps**: Docker, Docker Compose
- **APIs**: Google Maps (transit), Twilio (SMS)

## 📦 Installation

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend)
- OpenAI API key

### Quick Start with Docker

```bash
git clone https://github.com/yourusername/community-resource-agent.git
cd community-resource-agent

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run everything
docker-compose up -d

# Access:
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

## 💬 How It Works

### Chat Flow Example
```
User: "I'm homeless and need shelter tonight"

Agent:
1. [Understands context] → Homelessness + Urgent
2. [Searches resources] → Uses tools to find nearby shelters
3. [Verifies eligibility] → Checks bed availability, requirements
4. [Provides options] → "Found 3 shelters within 2 miles with availability"
5. [Facilitates access] → "Would you like me to help you call? Here's the number..."
```

## 🎓 For Tech Recruiters

This project demonstrates:

✅ **Full-stack expertise**: Backend API design, database architecture, frontend UX  
✅ **AI/ML proficiency**: LangChain agents, RAG systems, prompt engineering  
✅ **Software engineering**: Clean code, testing, documentation, DevOps  
✅ **Product thinking**: Real problem solving, user research, impact metrics  
✅ **Scalability**: Can handle millions of users with proper infrastructure  

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test
```

## 📊 Impact Metrics

- **Users helped**: Track daily active users discovering services
- **Services accessed**: Monitor which services are most utilized
- **Crisis interventions**: Count urgent cases successfully redirected
- **Geographic coverage**: Map unserved areas needing more resources

## 🤝 Contributing

This is an open-source social impact project. Contributions welcome:
- Add more service categories
- Improve AI prompts & tool definitions
- Expand to new cities/regions
- Build SMS interface
- Create mobile app

## 📄 License

MIT License - Free for social good projects

## 📞 Contact & Support

- **GitHub Issues**: For bugs and features
- **Impact Metrics**: See `/dashboard` for real-time statistics

---

**Built with ❤️ to help people find the support they need.**
