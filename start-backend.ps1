# Start Backend Server
Write-Host "Starting FastAPI Backend..." -ForegroundColor Cyan
Set-Location backend
.\venv\Scripts\Activate.ps1
python main.py
