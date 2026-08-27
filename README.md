# Currency Exchange Rate Monitor

A Python tool that offers the user the means for **keeping track of the exchange rates** among currencies, an important task in business contexts or for personal finances. It gathers and stores information about rates, facilitating user to **take well-timed exchange decisions**.

---

## Features:

- Fetch rates for multiple currency pairs
- Configure primary currencies (active use) and watch currencies (passive monitoring)
- Configurable update interval (default: 1 hour)
- Store historical data in a database (SQLite)


## Installation

```
# Clone the repository
git clone https://github.com/javierenriquemartinez2006/currency-monitor.git
cd currency-monitor

# Create virtual enviroment
python -m venv venv
# Linux/macOS: source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy configuration template
cp .env.example .env
```

## Usage:

```
python3 main.py
```
- It will occupy the executing terminal. For running in background:
```bash
## Linux/macOS

# Start
nohup python3 main.py 

# Stop
ps aux | grep "python main.py"
kill <PID>
```

```powershell
## Windows (PowerShell)

# Start
Start-Job -Name "CurrencyMonitor" -ScriptBlock {
  cd C:\path\to\currency-monitor
  python main.y
}

# Stop
Stop-Job -Name "CurrencyMonitor"
Remove-Job -Name "CurrencyMonitor"
```

## Structure

```
currency-monitor/
├── src/
│   ├── __init__.py          # Package marker
│   ├── config.py            # Environment configuration
│   ├── database.py          # SQLite operations
│   ├── api_client.py        # Frankfurter API client (fetch logic)
│   └── schemas.py           # Pydantic models (validation)
├── main.py                  # Entry point & scheduler
├── requirements.txt         # Dependencies
├── .env.example             # Configuration template
├── .gitignore
└── README.md
```

## Configuration
Edit the programs variables at `.env`:
```
env
# Required: Frankfurter API endpoint
API_BASE_URL=https://api.frankfurter.dev/v2

# Currency lists (comma-separated, no spaces)
PRIMARY_CURRENCIES=USD,EUR,GBP    # Currencies you actively use
WATCH_CURRENCIES=JPY,CHF,CAD      # Currencies to monitor passively

# Update interval
FETCH_INTERVAL_HOURS=1

# Database path (relative or absolute)
DB_PATH=currency_exhange_rates.db

# Logging level
LOG_LEVEL=INFO
```

## Planned enhancements

- **Testing module**: Tests for the app functions
- **Alert mechanism**: Notify user when a rate threshold is surpassed
---
### Notes:

- The Frankfurter API (information source of the app) provides rates with **date-only precision**. To track multiple fetches per day maintining uniqueness in records, this program:
  - Uses the API's `date` as the date component
  - Adds the current **time** at fetch time
- The update interval is 1 hour minimum for limitig requests to the API. Even if rates dont change drastically in short periods:
  - It is **not intended for critical systems**.
  - For **large exchanges** make sure no much time has past since the last update, or wait for the next one.
  - You can also force an update by reinitiating the program.

## License
MIT
  

