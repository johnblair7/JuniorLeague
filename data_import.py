"""
Data import utility for JuniorLeague historical auction data

Handles the wide-format CSV files with team columns
"""
import csv
import re
from typing import List, Dict, Tuple
from models import db, Team, Player, Contract, HistoricalAuction
from app import app


def extract_year_from_filename(filename: str) -> int:
    """Extract year from filename like JuniorLeague2025.csv"""
    match = re.search(r'(\d{4})', filename)
    if match:
        return int(match.group(1))
    return None


def parse_last_name(player_str: str) -> str:
    """Extract last name from various formats"""
    if not player_str or player_str.strip() == '':
        return None
    
    # Handle "LastName, First" format
    if ',' in player_str:
        last, first = player_str.split(',', 1)
        return last.strip()
    
    # Handle "FirstName LastName"
    parts = player_str.strip().split()
    if len(parts) > 1:
        # Check if first part looks like a common first name
        # Otherwise assume it's a last name (some cultures)
        return parts[-1]  # Take the last part as surname
    
    return player_str.strip()


def parse_wide_format_csv(filepath: str, year: int) -> List[Dict]:
    """
    Parse the wide-format JuniorLeague CSV
    
    Expected format:
    - Row 0: Team names alternating with empty columns
    - Row 1: Column headers (Position, Player, $, Player, $, ...)
    - Row 2+: Data rows
    - Last row: Totals (skip)
    """
    results = []
    
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        
        # Read header rows
        team_row = next(reader)
        header_row = next(reader)
        
        # Extract team names from row 0
        # Format: ,Team1,,Team2,,Team3,...
        team_names = []
        for i, cell in enumerate(team_row):
            if cell and cell.strip() and cell.strip() not in ['Position', 'Player', '$']:
                team_names.append(cell.strip())
        
        print(f"Extracted teams: {team_names}")
        num_teams = len(team_names)
        
        # Process data rows
        for row_idx, row in enumerate(reader):
            # Skip empty rows and totals
            if not row or row[0] == '':
                continue
            
            # Skip totals row
            if 'SPENT' in row[0]:
                break
            
            position = row[0]
            
            # Process each team's data
            # Format: Position, Player, $, Player, $, ...
            # So skip index 0 (position), then process Player,$ pairs
            team_col_idx = 1  # Start after position column
            
            for team_idx in range(num_teams):
                if team_col_idx + 1 >= len(row):
                    break
                
                player_name = row[team_col_idx]
                salary_str = row[team_col_idx + 1]
                team_col_idx += 2  # Move to next team pair
                
                # Skip if no player
                if not player_name or player_name.strip() == '':
                    continue
                
                try:
                    salary = int(salary_str.strip())
                except (ValueError, AttributeError):
                    continue
                
                last_name = parse_last_name(player_name)
                
                if last_name:
                    results.append({
                        'year': year,
                        'position': position,
                        'player': player_name,
                        'last_name': last_name,
                        'salary': salary,
                        'team_idx': team_idx,
                    })
        
        # Store team names for reference
        results.append({
            'team_names': team_names,
        })
    
    return results


def get_or_create_team(team_name: str) -> Team:
    """Get or create a team by name"""
    team = Team.query.filter_by(name=team_name).first()
    if not team:
        # Create a placeholder owner
        team = Team(name=team_name, owner='TBD')
        db.session.add(team)
        db.session.commit()
    return team


def find_or_suggest_player(last_name: str, position: str, year: int) -> Tuple[Player, List[Player]]:
    """
    Find existing player or return suggestions for disambiguation
    
    Returns: (best_match or None, list of suggestions)
    """
    # Simple exact match on last name
    exact_matches = Player.query.filter(Player.name.ilike(f'%{last_name}%')).all()
    
    if len(exact_matches) == 1:
        return exact_matches[0], []
    
    elif len(exact_matches) > 1:
        return None, exact_matches
    
    # No matches found
    return None, []


def import_csv_file(filepath: str, confirm_matches: bool = True):
    """
    Import a single JuniorLeague CSV file
    
    Args:
        filepath: Path to CSV file
        confirm_matches: If True, will prompt for confirmation on ambiguous matches
    """
    year = extract_year_from_filename(filepath)
    if not year:
        print(f"Could not extract year from filename: {filepath}")
        return
    
    print(f"\n{'='*60}")
    print(f"Importing {filepath} (Year: {year})")
    print(f"{'='*60}\n")
    
    # Parse the CSV
    data = parse_wide_format_csv(filepath, year)
    
    if not data:
        print("No data found in file")
        return
    
    # Extract team names from last item
    team_names_raw = data[-1].get('team_names', [])
    team_names = []
    
    # Fix team names - they may have extra columns
    for name in team_names_raw[:10]:  # Should be 10 teams
        if name and name.strip():
            team_names.append(name.strip())
    
    print(f"Found teams: {team_names}")
    print(f"Total records to import: {len(data) - 1}\n")  # -1 for team_names dict
    
    # Group by team
    team_players = {}
    for item in data[:-1]:  # Exclude team_names dict
        if not isinstance(item, dict) or 'team_idx' not in item:
            continue
            
        team_idx = item['team_idx']
        if team_idx >= len(team_names):
            continue
            
        team_name = team_names[team_idx]
        
        if team_name not in team_players:
            team_players[team_name] = []
        
        team_players[team_name].append(item)
    
    # Import data
    import_stats = {
        'created_players': 0,
        'matched_players': 0,
        'created_contracts': 0,
        'created_auctions': 0,
        'ambiguous': [],
    }
    
    for team_name, players in team_players.items():
        print(f"\nProcessing team: {team_name}")
        
        # Get or create team
        team = get_or_create_team(team_name)
        
        for item in players:
            last_name = item['last_name']
            position = item['position']
            salary = item['salary']
            player_full = item['player']
            
            # Try to find or create player
            player, suggestions = find_or_suggest_player(last_name, position, year)
            
            if player:
                # Found exact match
                import_stats['matched_players'] += 1
                print(f"  ✓ Matched: {player.name} ({last_name})")
            elif suggestions:
                # Multiple matches - need disambiguation
                import_stats['ambiguous'].append({
                    'year': year,
                    'team': team_name,
                    'last_name': last_name,
                    'full_name': player_full,
                    'position': position,
                    'salary': salary,
                    'suggestions': suggestions,
                })
                print(f"  ⚠ Ambiguous: {last_name} - {len(suggestions)} matches found - SKIPPING")
                continue  # Skip this record for now
            else:
                # Create new player
                player = Player(name=player_full, mlb_team='UNK')
                db.session.add(player)
                db.session.commit()
                import_stats['created_players'] += 1
                print(f"  + Created: {player_full} ({last_name})")
            
            # Create historical auction record
            if player:  # Double-check we have a valid player
                auction = HistoricalAuction(
                    player_id=player.id,
                    team_id=team.id,
                    year=year,
                    salary=salary,
                    contract_type='auction',  # Placeholder
                )
                db.session.add(auction)
                import_stats['created_auctions'] += 1
    
    # Commit all changes
    db.session.commit()
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Import Summary")
    print(f"{'='*60}")
    print(f"Created {import_stats['created_players']} new players")
    print(f"Matched {import_stats['matched_players']} existing players")
    print(f"Created {import_stats['created_auctions']} historical auction records")
    print(f"Ambiguous matches: {len(import_stats['ambiguous'])}")
    
    if import_stats['ambiguous']:
        print(f"\n⚠ Ambiguous matches requiring review:")
        for item in import_stats['ambiguous']:
            print(f"\n  {item['last_name']} ({item['year']}, {item['team']})")
            print(f"    Full name: {item['full_name']}")
            print(f"    Position: {item['position']}, Salary: ${item['salary']}")
            for i, sug in enumerate(item['suggestions'][:5], 1):
                print(f"    {i}. {sug.name} (ID: {sug.id})")


if __name__ == '__main__':
    # Example usage
    with app.app_context():
        import_csv_file('data/imports/uploads/JuniorLeague2025.csv')

