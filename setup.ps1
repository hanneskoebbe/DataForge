$VENV_DIR = ".venv"

# 1. venv anlegen (falls nicht vorhanden)
if (!(Test-Path $VENV_DIR)) {
    Write-Output "Erstelle virtual environment..."
    python -m venv $VENV_DIR
} else {
    Write-Output "Virtual environment existiert bereits."
}

# 2. Dependencies installieren
if (Test-Path "requirements.txt") {
    Write-Output "Installiere Dependencies aus requirements.txt..."
    & "$VENV_DIR\Scripts\python.exe" -m pip install --upgrade pip
    & "$VENV_DIR\Scripts\python.exe" -m pip install -r requirements.txt
} else {
    Write-Output "Keine requirements.txt gefunden. Installiere Basis-Dependencies..."
    & "$VENV_DIR\Scripts\python.exe" -m pip install --upgrade pip
    & "$VENV_DIR\Scripts\python.exe" -m pip install numpy matplotlib pytest
    & "$VENV_DIR\Scripts\python.exe" -m pip freeze > requirements.txt
}

Write-Output "Setup abgeschlossen"
Write-Output "Aktiviere dein venv mit:"
Write-Output "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
Write-Output ".\.venv\Scripts\Activate.ps1"
Write-Output "Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Default"