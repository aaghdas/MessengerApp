#!/bin/bash

set -e

echo "========================================"
echo " Messenger App Setup"
echo " Stack: FastAPI + React + PostgreSQL"
echo " Environment: WSL Ubuntu 22.04" 
echo "========================================"
echo ""
echo "This setup script will install/use:"
echo ""
echo "Global WSL tools:"
echo "- git"
echo "- curl"
echo "- build-essential"
echo "- lsof"
echo "- python3"
echo "- python3-pip"
echo "- python3-venv"
echo "- postgresql"
echo "- postgresql-contrib"
echo "- nodejs"
echo "- npm"
echo ""
echo "Backend Python packages in each service venv:"
echo "- fastapi"
echo "- uvicorn[standard]"
echo "- python-jose[cryptography]"
echo "- passlib[bcrypt]"
echo "- sqlalchemy"
echo "- alembic"
echo "- asyncpg"
echo "- psycopg[binary]"
echo "- pydantic-settings"
echo "- python-dotenv"
echo "- email-validator"
echo "- python-multipart"
echo "- websockets"
echo ""
echo "Frontend packages:"
echo "- vite"
echo "- react"
echo "- react-dom"
echo "- axios"
echo "- react-router-dom"
echo "========================================"
echo ""

echo "=== Updating Ubuntu package list ==="
sudo apt update

echo ""
echo "=== Upgrading existing Ubuntu packages ==="
sudo apt upgrade -y

echo ""
echo "=== Installing Git ==="
echo "Git is used for version control and GitHub."
sudo apt install -y git

echo ""
echo "=== Installing curl ==="
echo "curl is used to download files/installers from the terminal."
sudo apt install -y curl

echo ""
echo "=== Installing build-essential ==="
echo "build-essential contains compiler tools needed by some Python packages."
sudo apt install -y build-essential

echo ""
echo "=== Installing lsof ==="
echo "lsof is used to find which process is using a port."
sudo apt install -y lsof

echo ""
echo "=== Installing Python 3 ==="
echo "Python 3 is used for the FastAPI backend services."
sudo apt install -y python3

echo ""
echo "=== Installing pip ==="
echo "pip is used to install Python packages."
sudo apt install -y python3-pip

echo ""
echo "=== Installing python3-venv ==="
echo "python3-venv is used to create isolated Python virtual environments."
sudo apt install -y python3-venv

echo ""
echo "=== Installing PostgreSQL ==="
echo "PostgreSQL is the database server for users, messages, contacts, and tokens."
sudo apt install -y postgresql

echo ""
echo "=== Installing PostgreSQL contrib ==="
echo "postgresql-contrib provides extra PostgreSQL utilities and extensions."
sudo apt install -y postgresql-contrib

echo ""
echo "=== Installing Node.js and npm if missing ==="
echo "Node.js runs JavaScript tools. npm installs frontend packages."

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js not found. Installing Node.js 22.x with npm..."
  curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
  sudo apt install -y nodejs
else
  echo "Node.js already installed: $(node -v)"
fi

echo ""
echo "=== Checking npm ==="
if ! command -v npm >/dev/null 2>&1; then
  echo "npm not found. Installing npm..."
  sudo apt install -y npm
else
  echo "npm already installed: $(npm -v)"
fi

echo ""
echo "=== Checking installed versions ==="

echo "Git:"
git --version || true

echo "Python:"
python3 --version || true

echo "pip:"
pip3 --version || true

echo "Node.js:"
node -v || true

echo "npm:"
npm -v || true

echo "PostgreSQL:"
psql --version || true

echo ""
echo "=== Starting PostgreSQL service ==="
sudo service postgresql start || true

echo ""
echo "=== Creating project folders ==="
mkdir -p auth_service/app
mkdir -p user_service/app
mkdir -p messaging_service/app
mkdir -p shared
mkdir -p frontend

echo ""
echo "=== Creating backend requirements file ==="
echo "This file contains all Python packages for the backend services."

cat > requirements-backend.txt << 'EOF'
fastapi
uvicorn[standard]
python-jose[cryptography]
passlib[bcrypt]
sqlalchemy
alembic
asyncpg
psycopg[binary]
pydantic-settings
python-dotenv
email-validator
python-multipart
websockets
EOF

echo ""
echo "Backend Python packages:"
echo "- fastapi: backend API framework"
echo "- uvicorn[standard]: runs FastAPI apps"
echo "- python-jose[cryptography]: JWT token handling"
echo "- passlib[bcrypt]: password hashing"
echo "- sqlalchemy: database ORM"
echo "- alembic: database migrations"
echo "- asyncpg: async PostgreSQL driver"
echo "- psycopg[binary]: PostgreSQL driver"
echo "- pydantic-settings: environment/settings management"
echo "- python-dotenv: loads .env files"
echo "- email-validator: validates email addresses"
echo "- python-multipart: form and file upload support"
echo "- websockets: WebSocket support"

echo ""
echo "=== Setting up auth_service virtual environment ==="

if [ ! -d auth_service/venv ]; then
  echo "Creating auth_service/venv..."
  python3 -m venv auth_service/venv
else
  echo "auth_service/venv already exists."
fi

echo "Upgrading pip inside auth_service/venv..."
auth_service/venv/bin/pip install --upgrade pip

echo "Installing backend Python packages inside auth_service/venv..."
auth_service/venv/bin/pip install -r requirements-backend.txt

echo "Copying requirements.txt to auth_service..."
cp requirements-backend.txt auth_service/requirements.txt

echo "Creating empty Python files for auth_service..."
touch auth_service/app/__init__.py
touch auth_service/app/main.py

echo "Creating auth_service/.env.example..."
cat > auth_service/.env.example << 'EOF'
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/messenger_auth
JWT_SECRET_KEY=change_this_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF

echo ""
echo "=== Setting up user_service virtual environment ==="

if [ ! -d user_service/venv ]; then
  echo "Creating user_service/venv..."
  python3 -m venv user_service/venv
else
  echo "user_service/venv already exists."
fi

echo "Upgrading pip inside user_service/venv..."
user_service/venv/bin/pip install --upgrade pip

echo "Installing backend Python packages inside user_service/venv..."
user_service/venv/bin/pip install -r requirements-backend.txt

echo "Copying requirements.txt to user_service..."
cp requirements-backend.txt user_service/requirements.txt

echo "Creating empty Python files for user_service..."
touch user_service/app/__init__.py
touch user_service/app/main.py

echo "Creating user_service/.env.example..."
cat > user_service/.env.example << 'EOF'
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/messenger_user
EOF

echo ""
echo "=== Setting up messaging_service virtual environment ==="

if [ ! -d messaging_service/venv ]; then
  echo "Creating messaging_service/venv..."
  python3 -m venv messaging_service/venv
else
  echo "messaging_service/venv already exists."
fi

echo "Upgrading pip inside messaging_service/venv..."
messaging_service/venv/bin/pip install --upgrade pip

echo "Installing backend Python packages inside messaging_service/venv..."
messaging_service/venv/bin/pip install -r requirements-backend.txt

echo "Copying requirements.txt to messaging_service..."
cp requirements-backend.txt messaging_service/requirements.txt

echo "Creating empty Python files for messaging_service..."
touch messaging_service/app/__init__.py
touch messaging_service/app/main.py

echo "Creating messaging_service/.env.example..."
cat > messaging_service/.env.example << 'EOF'
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/messenger_messages
JWT_SECRET_KEY=change_this_secret_key
JWT_ALGORITHM=HS256
EOF

echo ""
echo "=== Creating React frontend with Vite ==="
echo "Vite creates the React frontend project."
echo "React is the frontend UI library."

if [ ! -f frontend/package.json ]; then
  echo "frontend/package.json not found."
  echo "Creating new Vite React project in frontend/..."

  rm -rf frontend
  npm create vite@latest frontend -- --template react

  cd frontend

  echo ""
  echo "Installing default frontend packages..."
  npm install

  echo ""
  echo "Installing axios..."
  echo "axios is used to send HTTP requests from React to FastAPI."
  npm install axios

  echo ""
  echo "Installing react-router-dom..."
  echo "react-router-dom is used for frontend routing/pages."
  npm install react-router-dom

  cd ..
else
  echo "Frontend already exists. Skipping frontend creation."
fi

echo ""
echo "=== Creating .gitignore ==="

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc
venv/
.env

# Node
node_modules/
dist/
.env.local

# VS Code
.vscode/

# System
.DS_Store
Thumbs.db
EOF

echo ""
echo "========================================"
echo " Setup finished successfully"
echo "========================================"
echo ""
echo "Created project structure:"
echo "- auth_service/"
echo "- user_service/"
echo "- messaging_service/"
echo "- shared/"
echo "- frontend/"
echo ""
echo "Created backend virtual environments:"
echo "- auth_service/venv"
echo "- user_service/venv"
echo "- messaging_service/venv"
echo ""
echo "Created empty Python app files:"
echo "- auth_service/app/main.py"
echo "- user_service/app/main.py"
echo "- messaging_service/app/main.py"
echo ""
echo "You should write your FastAPI code manually in those Python files."
echo ""
echo "Next steps:"
echo "1. Make sure starter.sh and stop.sh exist."
echo "2. Run:"
echo "   chmod +x setup_project.sh starter.sh stop.sh"
echo "3. Start the app:"
echo "   ./starter.sh"
echo ""