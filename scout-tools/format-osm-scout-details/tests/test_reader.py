from datetime import date
from pathlib import Path

import openpyxl
import pytest

from format_osm_scout_details.reader import _read_dob, read_scouts

REFERENCE_DIR = Path(__file__).resolve().parent.parent / "reference_files"


def test_read_scouts_returns_one_record_per_row():
    records = read_scouts(REFERENCE_DIR / "example_input.xlsx")
    assert len(records) == 6


def test_read_scouts_extracts_fields_from_the_correct_group():
    records = read_scouts(REFERENCE_DIR / "example_input.xlsx")
    amelia = records[0]

    assert amelia.first_name == "Amelia"
    assert amelia.last_name == "Clarke"
    assert amelia.known_as == "Millie"
    assert amelia.dob == date(2014, 3, 12)
    assert amelia.patrol_name == "Foxes"
    assert amelia.patrol_role == "Patrol Leader"

    # Primary Contact 1 fields must not be confused with Primary Contact 2's,
    # despite sharing the same field names ("First Name", "Phone 1", ...).
    assert amelia.p1_first_name == "Sarah"
    assert amelia.p1_relationship == "Mum"
    assert amelia.p2_first_name == "David"
    assert amelia.p2_relationship == "Dad"

    assert amelia.medical_details == "Mild asthma, carries inhaler"
    assert amelia.photographs == "Yes"


def test_read_scouts_handles_missing_second_contact():
    records = read_scouts(REFERENCE_DIR / "example_input.xlsx")
    oliver = next(r for r in records if r.first_name == "Oliver")

    assert oliver.p1_first_name == "Helen"
    assert oliver.p2_first_name == ""
    assert oliver.p2_relationship == ""


def test_read_scouts_pulls_doctors_surgery_fields_separately_from_essential_information():
    records = read_scouts(REFERENCE_DIR / "example_input.xlsx")
    oliver = next(r for r in records if r.first_name == "Oliver")

    assert oliver.allergies == "Peanuts - carries EpiPen"
    assert oliver.surgery_medical_information == (
        "Confirmed anaphylaxis to peanuts - see care plan on file"
    )
    assert oliver.surgery_dietary_needs == "Strict nut-free, EpiPen in bag"


def _dob_worksheet_with_value(value):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append([None])
    ws.append(["Date of birth"])
    ws.append([value])
    lookup = {(None, "Date of birth"): 1}
    return ws, lookup


@pytest.mark.parametrize(
    "raw_value,expected",
    [
        (date(2014, 3, 12), date(2014, 3, 12)),
        ("12/03/2014", date(2014, 3, 12)),
        ("2014-03-12", date(2014, 3, 12)),
        (None, None),
        ("", None),
        ("not a date", None),
    ],
)
def test_read_dob_is_defensive_about_source_formatting(raw_value, expected):
    ws, lookup = _dob_worksheet_with_value(raw_value)
    assert _read_dob(ws, 3, lookup, None, "Date of birth") == expected
