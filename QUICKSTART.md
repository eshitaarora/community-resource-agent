# Getting Started with Community Resource Agent

## 🎯 Start in 5 Minutes

### Option 1: Docker (Easiest)

```bash
# 1. Clone and navigate
git clone <repo> && cd community-resource-agent

# 2. Setup environment
cp backend/.env.example backend/.env
# Edit with your OpenAI key: nano backend/.env

# 3. Start everything
docker-compose up -d

# 4. Open browser
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

#### Terminal 1 - Backend:
```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Edit with your API keys
python -m app.db.seed_data
uvicorn app.main:app --reload
```

#### Terminal 2 - Frontend:
```bash
cd frontend
npm install
npm run dev
```

## 📖 Using the Application

### 1. Chat Interface
- Type your needs: "I need shelter tonight"
- Agent searches and recommends resources
- Get details about each service

### 2. Profile Setup
- Set your location for better recommendations
- Specify your needs (shelter, food, healthcare, etc.)
- Enter income level for eligibility matching
- Note accessibility requirements

### 3. Browse Resources
- View all available services
- Filter by category
- Search nearby with your location
- See full details and contact info

### 4. View Impact
- Check usage statistics
- See which services help most people
- Track outcomes

## 🔑 Required API Keys

1. **OpenAI API Key** (Required)
   - Get from: https://platform.openai.com/api-keys
   - Cost: Pay-as-you-go (GPT-4 recommended)

2. **Google Maps API** (Optional)
   - Get from: https://developers.google.com/maps
   - Used for transit information

3. **Twilio** (Optional)
   - For SMS notifications
   - Get from: https://www.twilio.com/

## 📁 Project Structure

```
backend/
├── app/main.py              ← FastAPI app
├── app/agents/              ← AI agent logic
├── app/api/                 ← REST endpoints
├── app/db/                  ← Database models
└── requirements.txt         ← Python dependencies

frontend/
├── src/App.jsx              ← Main app
├── src/components/          ← React components
├── src/pages/               ← Page views
└── package.json             ← npm dependencies
```

## 🧪 Testing the API

### Using curl:
```bash
# Send message to agent
curl -X POST http://localhost:8000/api/chat/send \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user",
    "message": "I need food assistance"
  }'

# Get resources
curl http://localhost:8000/api/resources?category=food

# View API docs
# Open http://localhost:8000/docs
```

## 🛠️ Customization

### Add Your Own Resources
Edit `backend/app/db/seed_data.py`:
```python
SEED_RESOURCES = [
    {
        "name": "Your Service",
        "category": "shelter",
        "address": "123 Your St",
        # ... other fields
    }
]
```

### Change AI Behavior
Edit `backend/app/agents/llm_config.py`:
- Modify `SYSTEM_PROMPT` for different AI personality
- Change `OPENAI_MODEL` for different models
- Adjust `temperature` for response randomness

### Update Styling
Edit `frontend/src/index.css` or Tailwind config.

## 🚀 Deploy to Production

### Using Docker:
```bash
# Build
docker-compose -f docker-compose.yml build

# Deploy with environment variables
DATABASE_URL=postgresql://... \
OPENAI_API_KEY=sk-... \
docker-compose up -d
```

### Using cloud platforms:
- **Heroku**: Deploy Docker image
- **AWS**: ECS + RDS + ElastiCache
- **Google Cloud**: Cloud Run + Cloud SQL
- **Azure**: Container Instances + PostgreSQL

## 📊 View Real-Time Metrics

Visit http://localhost:3000 and click "Impact Dashboard":
- Total users helped
- Conversations completed
- Services accessed
- Helpful response rate

## 🐛 Troubleshooting

### API not starting?
```bash
# Check logs
docker-compose logs backend

# Test database connection
python -c "from app.db.database import SessionLocal; SessionLocal()"
```

### Frontend can't connect to API?
- Check `REACT_APP_API_URL` in frontend/.env
- Ensure backend is running on port 8000
- Check CORS settings in backend/app/main.py

### Database errors?
```bash
# Reset database (careful!)
docker-compose exec backend python -c "from app.db.database import drop_all_tables; drop_all_tables()"

# Reseed data
docker-compose exec backend python -m app.db.seed_data
```

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs
- **API Schema**: http://localhost:8000/openapi.json
- **Full Setup Guide**: See COMPLETE_SETUP.md

## 💡 Pro Tips

1. **Save your user ID** - Found in the app for continuity
2. **Use profile** - Better recommendations with complete profile
3. **Check hours** - Resources have different operating hours
4. **Call first** - Availability can change, always verify
5. **Provide feedback** - Helps improve the AI

## ❓ Questions?

- Check COMPLETE_SETUP.md for detailed info
- Review API docs at `/docs`
- Check backend logs: `docker-compose logs -f backend`

---

**Ready to help vulnerable populations find critical resources!** 🎯
