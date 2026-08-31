# format-osm-scout-details

Converts an Online Scout Manager (OSM) "Personal Details" export into a
single, compact, printable sheet — one row per Scout — with just what a
leader needs at a glance on camp/trips: name, age, patrol/role, address,
both parents' names and phone numbers, medical/dietary/emergency info, and
photo consent.

See `claude.md` for the full field-mapping spec.

## Usage

```bash
poetry install
poetry run format-osm-scout-details path/to/osm_export.xlsx
```

Writes `path/to/osm_export_formatted.xlsx` next to the input by default, or
pass `-o/--output` to choose a different path:

```bash
poetry run format-osm-scout-details path/to/osm_export.xlsx -o leaders_sheet.xlsx
```

## Development

```bash
poetry install
poetry run pytest
```

`reference_files/example_input.xlsx` and `reference_files/example_output.xlsx`
are fake test data and the corresponding expected output — used as the
end-to-end regression fixture in `tests/test_end_to_end.py`.
