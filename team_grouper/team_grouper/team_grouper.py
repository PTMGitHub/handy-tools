import argparse
import csv
import random
from typing import List, Tuple, Dict

Person = Tuple[str, str, str, str]  # (Name, Team, Role, Location)


def read_people_from_file(filepath: str) -> List[Person]:
    """Read people from a CSV file with columns: Name,Team,Role,Location"""
    people: List[Person] = []
    with open(filepath, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row["Name"].strip()
            team = row["Team"].strip()
            role = row["Role"].strip()
            location = row["Location"].strip().lower()
            people.append((name, team, role, location))
    return people


def group_balanced(people: List[Person], num_groups: int) -> List[List[Person]]:
    """
    Distribute people into groups:
    - Try to ensure each group has at least one of each role (if possible)
    - Keep groups roughly even in size
    - Spread same teams across groups as much as possible
    """
    if num_groups <= 0:
        raise ValueError("Number of groups must be positive")

    random.shuffle(people)
    groups: List[List[Person]] = [[] for _ in range(num_groups)]

    # Track counts
    team_counts: List[Dict[str, int]] = [dict() for _ in range(num_groups)]
    role_counts: List[Dict[str, int]] = [dict() for _ in range(num_groups)]

    # Group people by role
    role_buckets: Dict[str, List[Person]] = {}
    for person in people:
        _, _, role, _ = person
        role_buckets.setdefault(role, []).append(person)

    # --- Pass 1: Distribute role by role, keeping group sizes balanced ---
    for role, bucket in role_buckets.items():
        random.shuffle(bucket)
        for person in bucket:
            # Pick the group with the fewest people so far,
            # break ties by minimizing team/role collisions
            best_group = min(
                range(num_groups),
                key=lambda g: (
                    len(groups[g]),
                    team_counts[g].get(person[1], 0),
                    role_counts[g].get(role, 0),
                ),
            )
            groups[best_group].append(person)
            team_counts[best_group][person[1]] = team_counts[best_group].get(person[1], 0) + 1
            role_counts[best_group][role] = role_counts[best_group].get(role, 0) + 1

    return groups

def main():
    parser = argparse.ArgumentParser(description="Group names into balanced teams.")
    parser.add_argument("num_remote_groups", type=int, help="Number of groups for remote names.")
    parser.add_argument("num_office_groups", type=int, help="Number of groups for office names.")
    parser.add_argument("--file", required=True, help="Path to CSV file containing Name,Team,Role,Location")

    args = parser.parse_args()

    people = read_people_from_file(args.file)

    remote_people = [p for p in people if p[3] == "remote"]
    office_people = [p for p in people if p[3] == "office"]

    role_priority = {
        "PO": 0,
        "DL": 1,
        "TL": 2,
        "BA": 3,
        "UR": 4,
        "Engineer": 5,
    }

    if remote_people:
        remote_groups = group_balanced(remote_people, args.num_remote_groups)
        print("Remote Groups:")
        for i, group in enumerate(remote_groups, 1):
            sorted_group = sorted(group, key=lambda x: role_priority.get(x[2], 999))
            formatted = [f"{name} ({team}, {role})" for name, team, role, _ in sorted_group]
            print(f"Group {i}: {', '.join(formatted)}")

    if office_people:
        office_groups = group_balanced(office_people, args.num_office_groups)
        print("\nOffice Groups:")
        for i, group in enumerate(office_groups, 1):
            sorted_group = sorted(group, key=lambda x: role_priority.get(x[2], 999))
            formatted = [f"\n{name} ({team}, {role})" for name, team, role, _ in sorted_group]
            print(f"\nGroup {i}: {', '.join(formatted)}")


if __name__ == "__main__":
    main()