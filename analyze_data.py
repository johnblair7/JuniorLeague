"""
Analyze imported historical data to find keeper patterns and ambiguous matches
"""
from app import app, db
from models import Player, HistoricalAuction, Team
from collections import defaultdict
from datetime import datetime


def find_keeper_candidates():
    """Find players who appear multiple years (likely keepers)"""
    with app.app_context():
        # Find players with multiple years
        multi_year_query = db.session.query(
            HistoricalAuction.player_id,
            HistoricalAuction.team_id,
            db.func.min(HistoricalAuction.year).label('first_year'),
            db.func.max(HistoricalAuction.year).label('last_year'),
            db.func.count().label('years')
        ).group_by(
            HistoricalAuction.player_id,
            HistoricalAuction.team_id
        ).having(db.func.count() > 1)
        
        print(f"\n{'='*80}")
        print("KEEPER CANDIDATES (Players with Multiple Years)")
        print(f"{'='*80}\n")
        
        print(f"{'Player':<30} {'Team':<15} {'Years':<10} {'Range':<15}")
        print("-" * 80)
        
        keepers = []
        for row in multi_year_query:
            player = Player.query.get(row.player_id)
            team = Team.query.get(row.team_id)
            keepers.append({
                'player': player,
                'team': team,
                'years': row.years,
                'range': f"{row.first_year}-{row.last_year}"
            })
        
        # Sort by years (most kept first)
        keepers.sort(key=lambda x: x['years'], reverse=True)
        
        for keeper in keepers[:50]:  # Show top 50
            print(f"{keeper['player'].name:<30} {keeper['team'].name:<15} {keeper['years']:<10} {keeper['range']:<15}")
        
        print(f"\nTotal keepers identified: {len(keepers)}")
        return keepers


def find_ambiguous_players():
    """Find players who might need disambiguation"""
    with app.app_context():
        print(f"\n{'='*80}")
        print("AMBIGUOUS PLAYERS (Same Name, Different Context)")
        print(f"{'='*80}\n")
        
        # Find names that appear multiple times as different players
        name_counts = db.session.query(
            Player.name,
            db.func.count(Player.id)
        ).group_by(Player.name).having(db.func.count(Player.id) > 1).all()
        
        print(f"{'Player Name':<40} {'Occurrences':<15}")
        print("-" * 60)
        
        ambiguous = []
        for name, count in name_counts:
            players = Player.query.filter_by(name=name).all()
            years = []
            for p in players:
                auctions = HistoricalAuction.query.filter_by(player_id=p.id).all()
                years.extend([(a.year, a.team_id) for a in auctions])
            
            print(f"{name:<40} {count:<15}")
            ambiguous.append({'name': name, 'count': count, 'players': players})
        
        print(f"\nTotal ambiguous names: {len(ambiguous)}")
        return ambiguous


def show_team_summaries():
    """Show spending per team per year"""
    with app.app_context():
        print(f"\n{'='*80}")
        print("TEAM SPENDING BY YEAR")
        print(f"{'='*80}\n")
        
        for team in Team.query.order_by(Team.name).all():
            print(f"\n{team.name}:")
            year_stats = db.session.query(
                HistoricalAuction.year,
                db.func.count().label('players'),
                db.func.sum(HistoricalAuction.salary).label('total')
            ).filter_by(team_id=team.id).group_by(HistoricalAuction.year).order_by(HistoricalAuction.year).all()
            
            for year, players, total in year_stats:
                print(f"  {year}: {players} players, ${total}")


def find_salary_changes():
    """Identify players with significant salary changes (likely keepers)"""
    with app.app_context():
        print(f"\n{'='*80}")
        print("SALARY CHANGES (Keeper Pattern Analysis)")
        print(f"{'='*80}\n")
        
        # Find players with salary changes across years on same team
        changes = db.session.query(
            HistoricalAuction.player_id,
            HistoricalAuction.team_id,
            HistoricalAuction.year,
            HistoricalAuction.salary
        ).filter_by(
            team_id=HistoricalAuction.team_id
        ).order_by(
            HistoricalAuction.player_id,
            HistoricalAuction.team_id,
            HistoricalAuction.year
        ).all()
        
        # Group by player+team
        player_teams = defaultdict(list)
        for change in changes:
            key = (change.player_id, change.team_id)
            player_teams[key].append((change.year, change.salary))
        
        # Find keepers with salary changes
        keeper_changes = []
        for (player_id, team_id), history in player_teams.items():
            if len(history) > 1:
                history.sort()
                first_salary = history[0][1]
                last_salary = history[-1][1]
                if first_salary != last_salary:
                    player = Player.query.get(player_id)
                    team = Team.query.get(team_id)
                    keeper_changes.append({
                        'player': player.name,
                        'team': team.name,
                        'first_year': history[0][0],
                        'first_salary': first_salary,
                        'last_year': history[-1][0],
                        'last_salary': last_salary,
                        'change': last_salary - first_salary
                    })
        
        keeper_changes.sort(key=lambda x: abs(x['change']), reverse=True)
        
        print(f"{'Player':<30} {'Team':<15} {'Change':<15} {'Years':<15}")
        print("-" * 80)
        
        for change in keeper_changes[:30]:
            years_str = f"{change['first_year']}-{change['last_year']}"
            change_str = f"${change['first_salary']}→${change['last_salary']}"
            print(f"{change['player']:<30} {change['team']:<15} {change_str:<15} {years_str:<15}")
        
        print(f"\nTotal keepers with salary changes: {len(keeper_changes)}")


def main():
    """Run all analyses"""
    with app.app_context():
        print("\n" + "="*80)
        print("JUNIOR LEAGUE DATA ANALYSIS")
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        find_keeper_candidates()
        find_ambiguous_players()
        find_salary_changes()
        show_team_summaries()
        
        print("\n" + "="*80)
        print("ANALYSIS COMPLETE")
        print("="*80 + "\n")


if __name__ == '__main__':
    main()

