# Installation Guide for macOS

## Prerequisites Check

Your system is missing some development tools. Follow these steps to get everything working:

## Step 1: Install Xcode Command Line Tools (Required)

```bash
xcode-select --install
```

A dialog will appear. Click **Install** and wait for completion (~5 minutes).

After installation, verify:
```bash
xcode-select -p
# Should show: /Applications/Xcode.app/Contents/Developer
```

## Step 2: Install Homebrew (Recommended)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Verify:
```bash
brew --version
```

## Step 3: Install Node.js (For Frontend)

```bash
brew install node
```

Verify:
```bash
node --version
npm --version
```

## Step 4: Setup Backend

```bash
cd /private/tmp/community-resource-agent/backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -m app.db.seed_data
```

## Step 5: Setup Frontend

```bash
cd /private/tmp/community-resource-agent/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Step 6: Run Backend (in new terminal)

```bash
cd /private/tmp/community-resource-agent/backend
source venv/bin/activate
uvicorn app.main:app --reload
```

## Step 7: Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Troubleshooting

### "Command not found: brew"
Make sure you completed Step 2 fully. After installation, you may need to add Homebrew to your PATH:
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc
```

### "ModuleNotFoundError" when running Python
Make sure virtual environment is activated:
```bash
source venv/bin/activate
```

### Port already in use
If port 8000 or 3000 is already in use, specify different ports:
```bash
# Backend on different port
uvicorn app.main:app --reload --port 8001

# Frontend on different port
npm run dev -- --port 3001
```

## Docker Alternative (If you have Docker installed)

```bash
cd /private/tmp/community-resource-agent
docker-compose up -d
```

Access at: http://localhost:3000

---

After completing these steps, your application will be fully functional!
