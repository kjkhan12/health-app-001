# Health App Quick Start Script
Write-Host "=== Health Assessment App Setup ===" -ForegroundColor Cyan
Write-Host ""

# Backend Setup
Write-Host "Setting up Backend..." -ForegroundColor Yellow
Set-Location backend

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Green
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Green
pip install -r requirements.txt

Write-Host ""
Write-Host "Backend setup complete!" -ForegroundColor Green
Write-Host "To start the backend server, run: python main.py" -ForegroundColor Cyan
Write-Host ""

# Return to root
Set-Location ..

# Frontend Setup
Write-Host "Setting up Frontend..." -ForegroundColor Yellow
Set-Location frontend

# Install dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Green
npm install

Write-Host ""
Write-Host "Frontend setup complete!" -ForegroundColor Green
Write-Host "To start the frontend server, run: npm run dev" -ForegroundColor Cyan
Write-Host ""

# Return to root
Set-Location ..

Write-Host "=== Setup Complete! ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Open a terminal and run: cd backend; .\venv\Scripts\Activate.ps1; python main.py" -ForegroundColor White
Write-Host "2. Open another terminal and run: cd frontend; npm run dev" -ForegroundColor White
Write-Host "3. Visit http://localhost:3000 in your browser" -ForegroundColor White
Write-Host ""
