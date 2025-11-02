# Historical Data Import Guide

## Quick Match Strategy

For historical data imports, here are different approaches we can use:

### Option 1: Interactive Matching (Recommended for Now)
1. Upload CSV with last names
2. System shows possible matches (with MLB teams/years)
3. You confirm which player is correct
4. We save the match for future imports

### Option 2: Fuzzy Matching (Good Baseline)
- Use fuzzy string matching on last names
- Weight by:
  - Years active
  - Positions
  - MLB teams
  - Auction years

### Option 3: Fangraphs Integration (Best Long-term)
- Use Fangraphs API to lookup players
- Store Fangraphs IDs
- Future data imports auto-match

## CSV Columns Expected

**Required:**
- `last_name` (or `name`)
- `year`
- `salary`

**Helpful for matching:**
- `mlb_team` (helps disambiguate)
- `position` (helps disambiguate)
- `keeper` (y/n or 1/0)

**Optional:**
- `first_name`
- `first_initial`
- `contract_type` (A/B/C/F/Long-term)
- `rotation_round` (if rotation pick)

## Example Data Formats

### Format 1: Just Last Names
```csv
year,last_name,salary,team,mlb_team
2023,Trout,45,Blue Jays,LAA
2023,Judge,42,Yankees,NYY
```

### Format 2: Full Names
```csv
year,name,salary,team,mlb_team,keeper
2023,Mike Trout,45,Blue Jays,LAA,1
2023,Aaron Judge,42,Yankees,NYY,1
```

### Format 3: With Contract Info
```csv
year,last_name,salary,contract_type,team,mlb_team
2023,Trout,45,C,Blue Jays,LAA
2022,Judge,42,C,Yankees,NYY
2023,Ohtani,15,F,Rotation,Rotation
```

## Keeper Detection Notes

Since keepers aren't always indicated:
- We can infer from:
  - Same player, multiple consecutive years
  - Same team, same salary/similar salary
  - Contract types
- You can mark manually during review

## Next Steps

1. Upload your historical CSV
2. We'll generate a matching report
3. Review and confirm matches
4. Import the data

