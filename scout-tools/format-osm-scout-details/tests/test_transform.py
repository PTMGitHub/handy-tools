from datetime import date

from format_osm_scout_details.reader import ScoutRecord
from format_osm_scout_details.transform import (
    build_address,
    build_dob,
    build_info,
    build_name,
    build_role,
    sort_records,
    transform,
)

def make_record(**overrides) -> ScoutRecord:
    defaults = dict(
        first_name="Amelia",
        last_name="Clarke",
        known_as="",
        dob=date(2014, 3, 12),
        patrol_name="Foxes",
        patrol_role="Patrol Leader",
    )
    defaults.update(overrides)
    return ScoutRecord(**defaults)


def test_build_name_without_known_as():
    record = make_record(known_as="")
    assert build_name(record) == "Amelia Clarke"


def test_build_name_with_known_as():
    record = make_record(known_as="Millie")
    assert build_name(record) == "Amelia Clarke (Millie)"


def test_build_dob_formats_date_without_age():
    record = make_record(dob=date(2014, 3, 12))
    assert build_dob(record) == "12-03-2014"


def test_build_dob_is_blank_when_dob_missing():
    record = make_record(dob=None)
    assert build_dob(record) == ""


def test_build_role_abbreviates_patrol_leader():
    assert build_role(make_record(patrol_role="Patrol Leader")) == "PL"


def test_build_role_abbreviates_assistant_patrol_leader():
    assert build_role(make_record(patrol_role="Assistant Patrol Leader")) == "APL"


def test_build_role_is_blank_for_plain_member():
    assert build_role(make_record(patrol_role="Member")) == ""


def test_build_address_uses_member_address_when_present():
    record = make_record(
        member_address_parts=["22 Elm Street", "", "", "Bristol", "BS7 9QW"],
        p1_address_parts=["14 Willow Grove", "", "", "Bristol", "BS8 2AB"],
    )
    assert build_address(record) == "22 Elm Street, Bristol, BS7 9QW"


def test_build_address_falls_back_to_p1_when_member_address_is_blank():
    record = make_record(
        member_address_parts=["", "", "", "", ""],
        p1_address_parts=["14 Willow Grove", "", "", "Bristol", "BS8 2AB"],
    )
    assert build_address(record) == "14 Willow Grove, Bristol, BS8 2AB"


def test_transform_p1_name_includes_relationship():
    record = make_record(p1_first_name="Sarah", p1_last_name="Clarke", p1_relationship="Mum")
    row = transform(record)
    assert row.p1_name == "Sarah Clarke (Mum)"


def test_transform_p2_name_and_phone_blank_when_no_second_contact():
    record = make_record(p2_first_name="", p2_last_name="", p2_relationship="", p2_phone_1="", p2_phone_2="")
    row = transform(record)
    assert row.p2_name == ""
    assert row.p2_phone == ""


def test_transform_phone_joins_both_numbers_with_slash():
    record = make_record(p1_phone_1="07700 900112", p1_phone_2="0117 900 2222")
    row = transform(record)
    assert row.p1_phone == "07700 900112 / 0117 900 2222"


def test_transform_phone_uses_whichever_number_is_present():
    record = make_record(p1_phone_1="", p1_phone_2="0117 900 4444")
    row = transform(record)
    assert row.p1_phone == "0117 900 4444"


def test_build_info_labels_and_joins_present_fields_only():
    record = make_record(
        medical_details="Mild asthma, carries inhaler",
        allergies="",
        dietary_requirements="",
        other_useful_information="Nervous around dogs",
        surgery_medical_information="",
        surgery_dietary_needs="",
    )
    assert build_info(record) == "Medical: Mild asthma, carries inhaler | Other: Nervous around dogs"


def test_build_info_excludes_tetanus_and_surgery_contact_details():
    # ScoutRecord has no tetanus_year / surgery name / surgery phone fields at
    # all -- Info is only built from the six fields in the agreed spec.
    record = make_record(surgery_medical_information="Confirmed anaphylaxis to peanuts")
    assert "Tetanus" not in build_info(record)
    assert build_info(record) == "Surgery Medical Info: Confirmed anaphylaxis to peanuts"


def test_build_info_is_blank_when_no_fields_present():
    assert build_info(make_record()) == ""


def test_sort_records_orders_by_dob_oldest_first_across_patrols():
    older_fox = make_record(first_name="Oliver", patrol_name="Foxes", dob=date(2013, 11, 2))
    younger_fox = make_record(first_name="Amelia", patrol_name="Foxes", dob=date(2014, 3, 12))
    older_badger = make_record(first_name="Jack", patrol_name="Badgers", dob=date(2013, 1, 30))

    # Input order deliberately scrambled relative to expected output order.
    records = [younger_fox, older_badger, older_fox]

    sorted_records = sort_records(records)

    assert [r.first_name for r in sorted_records] == ["Jack", "Oliver", "Amelia"]


def test_sort_records_puts_missing_dob_last():
    dated_fox = make_record(first_name="Amelia", patrol_name="Foxes", dob=date(2014, 3, 12))
    no_dob_fox = make_record(first_name="Alex", patrol_name="Foxes", dob=None)

    sorted_records = sort_records([no_dob_fox, dated_fox])

    assert [r.first_name for r in sorted_records] == ["Amelia", "Alex"]
