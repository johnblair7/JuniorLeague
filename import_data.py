"""
Historical Auction Data Import Script
Parses Junior League CSV format and imports into database
"""
import csv
import sys
from pathlib import Path
from models import db, Player, Team, Contract, HistoricalAuction
from app import app
import re


def parse_junior_league_csv(filepath):
    """
    Parse Junior League CSV format:
    - Position column on left
    - Player, Salary pairs for each team
    - Team names in header
    - Empty cells where team didn't draft that position
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    if len(rows) < 3:
        return []
    
    # Extract year from filename
    filename = Path(filepath).stem
    year_match = re.search(r'20\d{2}', filename)
    year = int(year_match.group()) if year_match else None
    
    # First row has team names alternating with empty columns
    # Second row is header: Position, Player, $, Player, $, etc.
    team_row = rows[0]
    header_row = rows[1]
    
    # Extract team names (every other column starting from index 1)
    teams = []
    for i in range(1, len(team_row), 2):
        team_name = team_row[i].strip()
        if team_name:
            teams.append({
                'index': i,
                'name': team_name,
                'player_col': i,  # Team name is at i, player is at same col (i+1), salary at i+2
                'salary_col': i + 1
            })
    
    
    # Extract data rows (skip header rows and "SPENT:" row)
    data_rows = []
    for row in rows[2:]:
        if not row or row[0].strip().upper() == 'SPENT:':
            break
        position = row[0].strip()
        if not position:
            continue
        
        # Extract players for each team
        for team_info in teams:
            player_col = team_info['player_col']
            salary_col = team_info['salary_col']
            
            if player_col < len(row) and salary_col < len(row):
                player_name = row[player_col].strip()
                salary_str = row[salary_col].strip()
                
                if player_name and salary_str:
                    try:
                        salary = int(salary_str)
                        data_rows.append({
                            'year': year,
                            'team': team_info['name'],
                            'position': position,
                            'player': player_name,
                            'salary': salary
                        })
                    except ValueError:
                        pass
    
    return data_rows


def normalize_player_name(name):
    """Clean up player names"""
    # Remove extra whitespace
    name = ' '.join(name.split())
    return name


def import_historical_data(filepath):
    """Import historical data from CSV"""
    print(f"\n📥 Importing: {filepath}")
    
    # Parse CSV
    data = parse_junior_league_csv(filepath)
    print(f"   Found {len(data)} player entries")
    
    if not data:
        print("   ⚠️  No data found")
        return
    
    # Get or create teams
    team_map = {}
    for entry in data:
        team_name = entry['team']
        if team_name not in team_map:
            team = Team.query.filter_by(name=team_name).first()
            if not team:
                team = Team(name=team_name, owner="TBD")  # Will need to update manually
                db.session.add(team)
                db.session.flush()
                print(f"   ✨ Created team: {team_name}")
            team_map[team_name] = team
    
    # Import players and contracts
    imported_count = 0
    skipped_count = 0
    
    for entry in data:
        player_name = normalize_player_name(entry['player'])
        team = team_map[entry['team']]
        
        # Try to find existing player
        player = Player.query.filter_by(name=player_name).first()
        
        if not player:
            # Create new player
            player = Player(
                name=player_name,
                position=entry['position'],
                mlb_team=None  # Not in CSV
            )
            db.session.add(player)
            db.session.flush()
            print(f"   ✨ Created player: {player_name}")
        
        # Check if we already have this historical auction entry
        existing = HistoricalAuction.query.filter_by(
            player_id=player.id,
            team_id=team.id,
            year=entry['year']
        ).first()
        
        if existing:
            # Update existing
            existing.salary = entry['salary']
            skipped_count += 1
        else:
            # Create new historical entry
            hist_entry = HistoricalAuction(
                player_id=player.id,
                team_id=team.id,
                year=entry['year'],
                salary=entry['salary'],
                contract_type='C'  # Default, can refine later
            )
            db.session.add(hist_entry)
            imported_count += 1
    
    db.session.commit()
    print(f"   ✅ Imported: {imported_count}, Skipped: {skipped_count}")


def main():
    """Main import function"""
    if len(sys.argv) < 2:
        print("Usage: python import_data.py <csv_file1> [csv_file2] ...")
        print("Example: python import_data.py data/imports/JuniorLeague2025.csv")
        sys.exit(1)
    
    with app.app_context():
        db.create_all()
        
        for filepath in sys.argv[1:]:
            if Path(filepath).exists():
                import_historical_data(filepath)
            else:
                print(f"⚠️  File not found: {filepath}")
        
        print("\n✅ Import complete!")


if __name__ == '__main__':
    main()

