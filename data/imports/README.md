# Historical Data Import

This folder is for importing your historical auction data.

## Supported Formats

- CSV files with auction history
- CSV files with player projections
- Manual entry through the web interface

## CSV Structure Examples

### Auction History CSV
```
year,player_name,position,salary,contract_type,team,mlb_team
2023,Mike Trout,OF,45,auction_keeper,Blue Jays,LAA
2023,Aaron Judge,OF,42,auction_keeper,Yankees,NYY
```

### Projections CSV
```
player_name,position,projected_avg,projected_hr,projected_rbi,projected_sb
Mookie Betts,OF,0.310,32,95,12
```

### Rotation Round CSV
```
year,player_name,round,salary,team
2023,Shohei Ohtani,Round 1,30,Astros
```

## Import Process

1. Prepare your CSV files
2. Go to Admin panel
3. Upload via "Import Historical Data"
4. Review and confirm import

