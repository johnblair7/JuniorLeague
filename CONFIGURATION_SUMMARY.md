# Junior League Configuration Summary

## League Setup

**League Name:** Junior League  
**Teams:** 10  
**Auction Budget:** $280 per team

---

## Roster Structure

### Active Roster (25 players)
- 5 Outfielders
- 2 Catchers
- 1 Second Baseman
- 1 Shortstop
- 1 Middle Infielder (2B or SS)
- 1 First Baseman
- 1 Third Baseman
- 1 Corner Man (1B or 3B)
- 2 DH slots
- 10 Pitchers

### Reserve Roster
- **Max:** 15 players
- **Exception:** 16th slot allowed for players on 60-day IL

---

## Auction Draft Rules

- **Minimum bid:** $1
- **Minimum increment:** $1
- **Budget:** $280 (teams not required to spend full amount)
- **Eligibility:** AL players on 26-man roster or AL IL as of Draft Day

---

## Rotation Draft

- **Rounds:** 15
- **Order:** 5th, 6th, 7th, 8th, 9th, 10th, 4th, 3rd, 2nd, 1st
- **Salaries by round:**
  - Round 1: $15
  - Rounds 2-10: $10
  - Rounds 11-14: $5
  - Round 15: $2
- **Eligibility:** Any player except NL players or already rostered
- **No position requirement:** Can select all pitchers, all hitters, or mix

---

## Contract Types

| Type | Description | Years |
|------|-------------|-------|
| **A** | One-year contract (acquired Sept 1+) | 1 |
| **B** | Second year of C contract | 1 |
| **C** | Standard contract (option year) | 2-3 |
| **F** | Free agent/prospect (rookie) | Until rookie status lost |
| **LONG_TERM** | Guaranteed contract | Variable (+$5/year) |

### Contract Notes
- F contracts migrate to C when rookie status lost (over 130 AB or 50 IP)
- Long-term contracts: `salary + ($5 × additional_years)`
- Option year available for C contracts
- All contracts transferable via trades

---

## Keeper/Freeze Rules

**Max Players Frozen:**
- **Active Roster:** 10 players
- **Reserve Roster:** 10 players
- **Total Combined:** 18 players

**Eligibility:**
- **Active:** Players on AL active roster, AL IL, or AL suspended list
- **Reserve:** NOT on major league 26-man active roster/IL/suspended list

**Important:** Frozen salaries count against $280 auction budget

---

## Scoring Categories (Standings)

**Hitting:**
1. **OBP** - Composite On-base Percentage
2. **R** - Total Runs
3. **HR** - Total Home Runs
4. **RBI** - Total RBIs
5. **SB** - Total Stolen Bases

**Pitching:**
6. **ERA** - Composite ERA
7. **W** - Total Wins
8. **WHIP** - (Walks + Hits)/Innings Pitched
9. **K** - Total Strikeouts
10. **SHOLDS** - Saves + Holds (1.0 for save, 0.5 for hold)

---

## Position Eligibility Rules

### Draft Day Eligibility
- **Rule 3.A:** 20+ games at position in previous season
- **Rule 3.B:** Position with most games if no 20+ games
- **Aggregation:** MIF (2B+SS), CO (1B+3B) - 20+ combined games

### In-Season Eligibility
- **Rule 3.E:** Position after 1 game played in current season

### Special Rules
- **Spencer Torkelson (3.G):** Minor leaguers - 20+ games or plurality
- **Shea Langeliers (3.J):** Late-season call-ups, owner choice
- **Ben Rice:** Deployment flexibility
- **Shohei Ohtani (3.I):** Separate hitter/pitcher tracking

---

## Notes

This configuration is based on the Junior League Constitution 2025 Revision.

All rules are implemented in `/config/league_settings.py` for programmatic use.

