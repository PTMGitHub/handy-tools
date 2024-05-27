from collections import defaultdict
from typing import List, Tuple
import random
import argparse

PLATFORM_TEAMS = ["B&D", "DDCOps", "Infras", "PlatDocs", "PlatOps", "PlatSec", "PlatUI", "PlatUCD", "Telemetry"]


def group_names(names: List[Tuple[str, str, str]], num_groups: int) -> List[List[Tuple[str, str, str]]]:
    groups = [[] for _ in range(num_groups)]
    for i, name_team in enumerate(names):
        groups[i % num_groups].append(name_team)
    return groups


def ensure_unique_team_group(groups: List[List[Tuple[str, str, str]]]) -> List[List[Tuple[str, str, str]]]:
    for _ in range(100):  # Retry up to 100 times
        random.shuffle(groups)
        for group in groups:
            teams_in_group = {team for _, team, _ in group}
            if len(teams_in_group) == len(group):
                return groups
        all_names = [name for group in groups for name in group]
        num_groups = len(groups)
        groups = group_names(all_names, num_groups)
    return groups


def assign_platform_teams(groups: List[List[Tuple[str, str, str]]], platform_teams) -> List[Tuple[str, List[Tuple[str, str, str]]]]:
    available_teams = platform_teams
    group_with_platform = []

    for group in groups:
        random.shuffle(available_teams)
        for platform_team in available_teams:
            if not any(member_team == platform_team for _, member_team, _ in group):
                group_with_platform.append((platform_team, group))
                available_teams.remove(platform_team)
                break

    return group_with_platform, available_teams


def main():
    parser = argparse.ArgumentParser(description="Group names into teams.")
    parser.add_argument("num_remote_groups", type=int, help="Number of groups for remote names.")
    parser.add_argument("num_office_groups", type=int, help="Number of groups for office names.")
    parser.add_argument("names_teams_locations", nargs="+", help="Names, their teams, and locations in the format 'Name,Team,Location'.")

    args = parser.parse_args()

    num_remote_groups = args.num_remote_groups
    num_office_groups = args.num_office_groups
    names_teams_locations = args.names_teams_locations

    names = [tuple(ntl.split(",")) for ntl in names_teams_locations]

    remote_names = [name for name in names if name[2] == "remote"]
    office_names = [name for name in names if name[2] == "office"]

    remote_groups = group_names(remote_names, num_remote_groups)
    office_groups = group_names(office_names, num_office_groups)

    remote_groups = ensure_unique_team_group(remote_groups)
    office_groups = ensure_unique_team_group(office_groups)

    remote_groups_with_platform, available_teams = assign_platform_teams(remote_groups, PLATFORM_TEAMS)
    office_groups_with_platform, unassigned_teams = assign_platform_teams(office_groups, available_teams)

    print("Remote Groups:")
    for i, (platform_team, group) in enumerate(remote_groups_with_platform, 1):
        formatted_group = [(name, team) for name, team, _ in group]
        print(f"Group {i} (Platform Team: {platform_team}): {formatted_group}")

    print("\nOffice Groups:")
    for i, (platform_team, group) in enumerate(office_groups_with_platform, 1):
        formatted_group = [(name, team) for name, team, _ in group]
        print(f"Group {i} (Platform Team: {platform_team}): {formatted_group}")

    print("\nUnassigned Platform teams:")
    for i in unassigned_teams:
        print(f"{i}")


if __name__ == "__main__":
    main()
