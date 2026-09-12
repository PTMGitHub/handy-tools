from dataclasses import dataclass
from datetime import date
from typing import List

from format_osm_scout_details.reader import ScoutRecord

ROLE_ABBREVIATIONS = {
    "patrol leader": "PL",
    "assistant patrol leader": "APL",
}


@dataclass
class OutputRow:
    name: str
    dob: str
    patrol_name: str
    role: str
    address: str
    p1_name: str
    p1_phone: str
    p2_name: str
    p2_phone: str
    info: str
    photo: str


def _join(parts, sep=", "):
    return sep.join(part for part in parts if part)


def build_name(record: ScoutRecord) -> str:
    name = f"{record.first_name} {record.last_name}".strip()
    if record.known_as:
        name += f" ({record.known_as})"
    return name


def build_dob(record: ScoutRecord) -> str:
    if record.dob is None:
        return ""
    return record.dob.strftime("%d-%m-%Y")


def build_role(record: ScoutRecord) -> str:
    return ROLE_ABBREVIATIONS.get(record.patrol_role.strip().lower(), "")


def build_address(record: ScoutRecord) -> str:
    member_address = _join(record.member_address_parts)
    if member_address:
        return member_address
    return _join(record.p1_address_parts)


def _build_contact_name(first_name: str, last_name: str, relationship: str) -> str:
    if not first_name and not last_name:
        return ""
    name = f"{first_name} {last_name}".strip()
    if relationship:
        name += f" ({relationship})"
    return name


def _build_contact_phone(phone_1: str, phone_2: str) -> str:
    return " / ".join(phone for phone in (phone_1, phone_2) if phone)


def build_info(record: ScoutRecord) -> str:
    labelled_fields = [
        ("Medical", record.medical_details),
        ("Allergies", record.allergies),
        ("Dietary", record.dietary_requirements),
        ("Other", record.other_useful_information),
        ("Surgery Medical Info", record.surgery_medical_information),
        ("Surgery Dietary Needs", record.surgery_dietary_needs),
    ]
    return " | ".join(f"{label}: {value}" for label, value in labelled_fields if value)


def transform(record: ScoutRecord) -> OutputRow:
    return OutputRow(
        name=build_name(record),
        dob=build_dob(record),
        patrol_name=record.patrol_name,
        role=build_role(record),
        address=build_address(record),
        p1_name=_build_contact_name(record.p1_first_name, record.p1_last_name, record.p1_relationship),
        p1_phone=_build_contact_phone(record.p1_phone_1, record.p1_phone_2),
        p2_name=_build_contact_name(record.p2_first_name, record.p2_last_name, record.p2_relationship),
        p2_phone=_build_contact_phone(record.p2_phone_1, record.p2_phone_2),
        info=build_info(record),
        photo=record.photographs,
    )


def sort_records(records: List[ScoutRecord]) -> List[ScoutRecord]:
    """Oldest DOB first. Records with no parseable DOB sort last rather
    than crashing the comparison."""

    def sort_key(record: ScoutRecord):
        return (
            record.dob is None,
            record.dob or date.min,
        )

    return sorted(records, key=sort_key)
