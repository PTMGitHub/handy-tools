# format-osm-scout-details — Requirements

This is the agreed spec, reconciling your original notes (preserved
verbatim at the bottom of this file) with decisions made while working
through the ambiguous/underspecified bits together. Where the two
disagreed, the resolution taken is noted inline.

## Purpose

As a Scout leader, key details about each Scout live in an online system
(OSM). This tool takes an OSM "Personal Details" export and produces a
single, compact, printable sheet — one row per Scout — with just what a
leader needs at a glance: who they are, their age, patrol/role, address,
both parents' names and phone numbers, medical/dietary/emergency info, and
photo consent.

## Reference files

- `reference_files/example_input.xlsx` — an OSM-shaped export (sheet
  "Scouts") with **fake** test data: 6 scouts across 3 patrols (Foxes,
  Badgers, Otters), covering the range of cases the tool must handle (one or
  two primary contacts, missing Phone 2, missing Member address block,
  Patrol Leader / Assistant Patrol Leader / plain Member roles, a `Known As`
  entry, and varied Doctor's Surgery / Essential Information field
  combinations).
- `reference_files/example_output.xlsx` — the exact expected output for that
  input, hand-built by applying the rules below. This is the ground-truth
  fixture for tests.

## Input format (OSM "Personal Details" export)

Sheet `Scouts`. Two header rows:
- Row 1: group name (forward-filled across merged-looking blocks, e.g.
  "Primary Contact 1", "Doctor's Surgery", "Member", "Essential
  Information", "Additional Information", "Consents"), blank for
  ungrouped columns.
- Row 2: field name within that group (e.g. "First Name", "Phone 1").

Data starts row 3. **Do not assume fixed column letters** — OSM lets users
customise which columns are included/ordered in the report, so the tool
must locate columns by `(group, field name)` lookup against rows 1–2, not by
position.

## Output format

Single header row: `Name, DOB, Patrol, Role, Address, Parents/Guardians,
Photo?` (7 columns). Each Scout occupies **two physical rows**:
- Row 1 (identity): `Name, DOB, Patrol, Role, Address, Parents/Guardians,
  Photo?` — one value per column.
- Row 2 (info): the `Info` text, merged across all 7 columns, right-aligned,
  wrapped. No separate header for this row — it's a continuation of the
  Scout above it, not its own column.

`Parents/Guardians` merges P1 and P2 into a single cell: one contact per
line (`{P1 Name} {P1 Phone}` then `{P2 Name} {P2 Phone}` on the line below,
via an embedded line break), omitting a contact's line entirely if that
contact doesn't exist. This replaced separate P1 Name / P1 Phone / P2 Name
/ P2 Phone columns.

Each Scout's two-row block gets a bottom border (closing it off from the
next Scout) and every other Scout is lightly shaded, so blocks read clearly
without needing gridlines everywhere.

(An earlier two-row-per-Scout attempt — a different split, with contacts
kept as four separate columns — was tried and reverted for not looking
right. This version, based on your own hand-edited mockup, is the current
one.)

### Field mapping rules

- **Name**: `{First name} {Last name}`, with `({Known As})` appended if
  `Additional Information > Known As` is present. E.g.
  `"Amelia Clarke (Millie)"`.
- **DOB**: formatted `dd-mm-yyyy` only, e.g. `12-03-2014`. (Age used to be
  appended in parentheses; removed — it would silently go stale on any
  printout kept for more than a few months, so isn't shown.)
- **Patrol Name**: copied as-is from `Patrol Name`.
- **Role**: derived from `Patrol Role` (case-insensitive match):
  - "Patrol Leader" → `PL`
  - "Assistant Patrol Leader" → `APL`
  - anything else (including plain "Member") → blank
- **Address**: the Member's own address block (`Member` > Address 1–4 +
  Postcode), joined with `", "`, postcode last. If the Member address block
  is entirely blank, fall back to Primary Contact 1's address block instead
  (this fallback isn't in the original notes — added to handle Scouts where
  the Member address fields are just never filled in in OSM).
- **Parents/Guardians**: one line per contact who exists, each line
  `{First Name} {Last Name} ({Relationship}) {Phone 1}{" / "+Phone 2 if
  present}` — e.g. `"Sarah Clarke (Mum) 07700 900111"`. Primary Contact 1's
  line first, then Primary Contact 2's on the line below (an embedded line
  break within the cell) if they exist; a contact with no name on record is
  omitted entirely (not a blank line).
- **Info**: every one of the following fields that has a value, each
  labelled, joined with `" | "` (omit any label whose source field is
  blank):
  - `Medical: {Essential Information > Medical details}`
  - `Allergies: {Essential Information > Allergies}`
  - `Dietary: {Essential Information > Dietary requirements}`
  - `Other: {Essential Information > Other useful information}`
  - `Surgery Medical Info: {Doctor's Surgery > Medical Information}`
  - `Surgery Dietary Needs: {Doctor's Surgery > Dietary Needs}`

  Note: Tetanus year and the Doctor's Surgery's own name/phone number are
  **not** included — confirmed against the original mapping table, which
  only calls for the six fields above.
- **Photo?**: copied as-is from `Consents > Photographs`.

### Row order

Grouped by `Patrol Name` (patrols in the order they first appear in the
input), then within each patrol ordered by **DOB, oldest to youngest**.

### Printability

- A4, landscape.
- Down to 7 columns (from 11) by merging P1/P2 into one `Parents/Guardians`
  cell and moving `Info` to its own full-width row — this was the actual
  fix for "fitting everything on one page made the text too small to
  read," which a two-row-split-by-column attempt (reverted) hadn't solved.
- The header row repeats on every printed page (Excel print titles).
- Wrap text on `Address`, `Parents/Guardians`, and the `Info` row.
- Frozen panes below the header for on-screen viewing too.
- Column widths sized so nothing is unreadably cramped.

## Tech stack

Python + Poetry, matching every other tool in this repo (see
`team_grouper`, `sweepstake-generator`, etc.): a `pyproject.toml` +
`poetry.lock`, package directory with `__init__.py`, `tests/`, a
`[tool.poetry.scripts]` CLI entry point, `argparse` for the CLI, `pytest`
for tests. `openpyxl` is the new dependency this tool introduces (for
reading/writing `.xlsx`).

## Open assumptions (flag if wrong)

- Only the `Scouts` worksheet is read; other worksheets in the input file
  (if any) are ignored.
- No filtering/redaction of "Secret Info" or "Sensitive information" fields
  is applied — those columns simply aren't among the ones pulled into
  `Info`, so they never appear in the output regardless of value.
- Where multiple patrols happen to have the same DOB for two Scouts, sort
  order between them is whatever Python's stable sort does with the
  input-row order (no explicit tiebreaker was specified).
- `Date of birth` is read defensively: a real Excel date parses normally; a
  text cell in `dd/mm/yyyy`, `dd/mm/yy`, `yyyy-mm-dd` or `dd-mm-yyyy` format
  also parses; anything blank or unparseable is treated as "no DOB" rather
  than crashing the run — that record still appears in the output (sorted
  last within its patrol), with a blank `DOB` column instead of a formatting
  error. Surfaced by a real OSM export containing at least one row without a
  usable DOB.

---

## Original claude.md

*(preserved verbatim — this is what was originally written but never saved
to disk before this project started; recovered from the editor buffer
partway through)*

# Project overview
## Context

As a Scout leader we keep details of our Scout on an online system but I want a hard copy of key information that I can print off so I have it readily avaliable

## Requirements:

A simple tool, `format-osm-scout-details`, that takes a .xlsx Input file (see example: `reference_files/example_input.xlsx`) of all the Scout information and produces a output file in the desired format (see example: `reference_files/example_output.xlsx`)

### Output file requirements
- A4 Landscape
- All columns should be visble in one page width but records can continue on to multiple pages.
- If it continues onto multiple pages
- Should be printable
- Scout records should be Grouped by `Patrol Name` and then ordered by their Date of Birth (DOB), oldest to youngest.
- If there is a `Known As` entry this should be included in `()`
- in the DOB, put their age in `()`
- Appart from `Name`, `P1 Name` and `P2 Name`, seperted each value with `, `
- If there is not a value for a field, dont include it.

#### Input to output field mapping
| Output field | Input field(s) |
|--------------|----------------|
| Name | `First name`, `Last name` AND `Additional Information`: `Known As` |
| DOB | `Date of birth` |
| Patrol Name | `Patrol Name` |
| Role | `Patrol Role` |
| Address | `Memeber`: `Address 1`, `Address 2`, `Address 3`, `Address 4`, `Postcode` |
| P1 Name | `Primary Contact 1`: `First name`, `Last name` |
| P1 Phone | `Primary Contact 1`: `Phone 1`, `Phone 2` |
| P2 Name | `Primary Contact 2`: `First name`, `Last name` |
| P2 Phone | `Primary Contact 2`: `Phone 1`, `Phone 2` |
| Info | `Doctor's Surgery`: `Medical Information`, `Dietary Needs` AND `Essential Information`: `Medical details`, `Allergies`, `Dietary requirements`, `Other useful information` |
| Photo? |`Consents`: `Photographs` |
