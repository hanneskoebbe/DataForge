# 🧰 DataForge

**DataForge** ist ein flexibles Werkzeug zur **Datenverarbeitung, Transformation und Analyse** – mit einer intuitiven grafischen Oberfläche.  
Das Ziel des Projekts ist es, alltägliche Aufgaben der Datenaufbereitung (z. B. Filtern, Mergen, Aggregieren, Exportieren) ohne komplizierte Skripte durchzuführen, aber trotzdem mit der vollen Power von Python zu kombinieren.

---

## 🚀 Funktionen

- Benutzerfreundliche GUI zum Laden, Anzeigen und Bearbeiten von Datensätzen  
- Unterstützung für **CSV**, **Excel**, und **JSON**-Dateien  
- Datenoperationen wie Filtern, Spaltenauswahl, Mergen und Aggregation  
- Export der Ergebnisse in verschiedene Formate  
- Automatisierte Einrichtung über ein **PowerShell-Skript (`setup.ps1`)**  
- Erweiterbar über eigene Python-Skripte im `scripts/`-Ordner  

---

## 🧩 Verzeichnisstruktur
```
DataForge/
├── gui/ # GUI-Komponenten der App
├── scripts/ # Zusatzfunktionen & Verarbeitungsskripte
├── main.py # Einstiegspunkt der Anwendung
├── requirements.txt # Python-Abhängigkeiten
├── setup.ps1 # Automatisches Setup-Skript für Windows
└── README.md #
```

---

## ⚙️ Installation

Voraussetzung: **Python 3.10+**

### 🪟 Windows (einfachster Weg)
```powershell
# Klonen und Setup ausführen
git clone https://github.com/hanneskoebbe/DataForge.git
cd DataForge
./setup.ps1
```
