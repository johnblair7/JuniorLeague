# Setup Guide for JuniorLeague

## Quick Start

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Initialize the database**
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database created!')"
```

Or visit `http://localhost:5000/init_db` after starting the app.

3. **Run the application**
```bash
python app.py
```

4. **Open in browser**
```
http://localhost:5000
```

## Adding Your Data

### Option 1: Manual Entry (Recommended to Start)

1. Go to Roster Manager
2. Click "Add Team" for each of your 10 teams
3. Add players manually
4. Record contracts

### Option 2: Import CSV

1. Prepare CSV files based on examples in `data/imports/`
2. Import functionality coming soon!

## Next Steps

- [ ] Add your 10 teams
- [ ] Upload historical auction data
- [ ] Add player projections
- [ ] Configure league budget if different from $260
- [ ] Customize stat calculations for your league's scoring

## Troubleshooting

**Port 5000 already in use?**
Change the port in `app.py` line 147: `app.run(debug=True, host='127.0.0.1', port=5001)`

**Database errors?**
Delete `juniorleague.db` and run init_db again

**Missing dependencies?**
Run: `pip install --upgrade -r requirements.txt`

