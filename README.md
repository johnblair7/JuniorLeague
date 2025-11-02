# JuniorLeague

A fantasy baseball auction and roster calculator for long-standing keeper leagues.

## Features

- **Auction Calculator**: Historical and predictive bidding estimates
- **Roster Calculator**: Track teams, players, and contracts
- **Live Auction Tracking**: Real-time updates during the auction
- **Contract Management**: Handles keepers, rotation rounds, and various contract types
- **Historical Data**: Import and analyze past auction data

## League Details

- 10 teams
- Keeper league with multiple contract types
- Contract types:
  - Auction purchases (keepers)
  - In-season acquisitions
  - Rotation round picks (draft-based contracts)

## Getting Started

This is a local desktop application that runs on your machine. No web hosting needed!

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application (runs locally at http://localhost:5000)
python app.py
```

Just open http://localhost:5000 in your browser and you're good to go!

## Project Structure

```
JuniorLeague/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── calculators/           # Auction and roster calculators
├── data/                  # Historical data and uploads
├── templates/             # HTML templates
├── static/                # CSS, JS, images
└── requirements.txt       # Python dependencies
```
