import argparse
from pathlib import Path

from format_osm_scout_details.reader import read_scouts
from format_osm_scout_details.transform import sort_records, transform
from format_osm_scout_details.writer import write_output


def default_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}_formatted.xlsx")


def run(input_path: Path, output_path: Path) -> None:
    records = read_scouts(input_path)
    records = sort_records(records)
    rows = [transform(record) for record in records]
    write_output(rows, output_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Convert an OSM 'Personal Details' export into a compact, "
            "printable leader's reference sheet."
        )
    )
    parser.add_argument("input_path", type=Path, help="Path to the OSM Personal Details .xlsx export")
    parser.add_argument(
        "-o", "--output", type=Path, default=None,
        help="Path for the formatted output .xlsx (default: <input>_formatted.xlsx)",
    )
    args = parser.parse_args()

    output_path = args.output or default_output_path(args.input_path)
    run(args.input_path, output_path)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
