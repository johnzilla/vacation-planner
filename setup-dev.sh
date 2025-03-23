#!/bin/bash
# Setup script for Vacation Planner development environment

echo "Setting up Vacation Planner development environment..."

# Create backend .env file if it doesn't exist
if [ ! -f backend/.env ]; then
  echo "Creating backend/.env file..."
  cp backend/.env.example backend/.env
  echo "Please update backend/.env with your specific configuration."
else
  echo "backend/.env already exists."
fi

# Create frontend .env file if it doesn't exist
if [ ! -f frontend/web/.env ]; then
  echo "Creating frontend/web/.env file..."
  cp frontend/web/.env.example frontend/web/.env
  echo "Please update frontend/web/.env with your specific configuration."
else
  echo "frontend/web/.env already exists."
fi

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install development dependencies
echo "Installing development dependencies..."
pip install -r requirements-dev.txt

# Create a helper script to run tests
echo "Creating test helper script..."
cat > run_tests.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
pytest "$@"
EOF
chmod +x run_tests.sh

cd ..

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend/web
npm install

# Install frontend development dependencies
echo "Installing frontend development dependencies..."
npm install --save-dev eslint eslint-plugin-svelte prettier prettier-plugin-svelte
cd ../..

# Initialize database
echo "Initializing database..."
cd backend
source venv/bin/activate
python initialize_db.py
python add_sample_holidays.py
cd ..

echo "Setup complete! You can now start the application:"
echo "Backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "Frontend: cd frontend/web && npm run dev"
