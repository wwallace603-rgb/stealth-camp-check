# stealth-camp-check

Overnight parking and rest-area rules for all 50 US states + DC, in your terminal. Know what's legal **before you pull over.**

Built by [CarSteader](https://carsteader.com/) — a guide site for stealth camping and vanlife. This package ships the same state-by-state data that powers the interactive web tool.

> **The one thing most people get wrong:** in states that define the term, *camping* and *sleeping in your vehicle* are not the same thing. Camping means setting up outside the van — a tent, awning, chairs, a stove. Sleeping inside a legally parked vehicle is usually the permitted use. Georgia's statute names "resting, sleeping, eating" as exactly what rest areas are for. If everything stays inside the vehicle, you're resting — not camping.

## Install

**Node.js (no install needed):**
```bash
npx stealth-camp-check tx
```

**Python:**
```bash
pip install stealth-camp-check
stealth-camp-check tx
```

## Usage

```bash
# Rules for one state (code or full name)
stealth-camp-check tx
stealth-camp-check georgia

# Table of all 50 states + DC
stealth-camp-check --list

# Raw JSON for scripting
stealth-camp-check ca --json
```

### Example output

```
$ stealth-camp-check tx

Texas
Rest areas: LIMITED — 24 hours
  A full day in any rest area — among the most permissive caps
  (Tex. Transp. Code 545.411). Tents/shelters prohibited.

  BLM land ........ Yes — 14-day rule applies (western states)
  National forests  Dispersed camping generally OK unless posted (7–21 day limits vary)
  Big-box lots .... Private property, store-by-store — ask at the entrance

  Source: https://texas.public.law/statutes/tex._transp._code_section_545.411

More from CarSteader:
  Web tool ........ https://carsteader.com/tools/stealth-camp-check/?state=TX
  Legal guide ..... https://carsteader.com/legal-stealth-camping-usa/
  Stealth gear .... https://carsteader.com/stealth-camping-gear-list/
```

## Status legend

| Tag | Meaning |
|-----|---------|
| `OK` | Overnight vehicle sleeping allowed in writing (e.g. GA, UT, WY) |
| `LIMITED` | Allowed but with a time cap — from 2h (PA) to 24h (TX, NM) |
| `NO` | Overnight parking banned outright (VA, MD, TN, CO) |
| `SIGNS GOVERN` | No statewide rule — the posted sign at that rest area is the law |

## Beyond rest areas

- **BLM public land** (12 western states): dispersed camping generally allowed under the **14-day rule** — max 14 days in one location per 28-day period, then move ≥25 miles.
- **National forests**: dispersed camping permitted unless a forest manager's order or sign prohibits it; limits vary by forest (7–21 days), keep 200 ft from water.
- **Walmart / big-box lots**: private property — a store decision, not a legal right. Ask at the entrance, keep everything inside, leave if asked.

## More guides

- [Legal Stealth Camping in the USA](https://carsteader.com/legal-stealth-camping-usa/) — BLM, Forest Service, and 14-day rule deep dive
- [Stealth Camping Gear List](https://carsteader.com/stealth-camping-gear-list/) — what to pack for a discreet overnight stay
- [Stealth Camping Windows & Covers](https://carsteader.com/stealth-camping-windows-covers/) — stay invisible from the outside
- [Interactive web tool (all states)](https://carsteader.com/tools/stealth-camp-check/)

## Data & disclaimer

Rules are a snapshot of state DOT pages and statutes where available, compiled for convenience. **This is not legal advice.** Regulations change and local ordinances can override state rules — when the stakes are high, confirm with the specific agency or a local call before relying on any single source.

## Contributing

Spotted an outdated rule? Open an issue or PR against `stealth_camp_check/states.json` (the single source of truth for both the Node and Python CLIs).

## License

MIT — see [LICENSE](./LICENSE).
