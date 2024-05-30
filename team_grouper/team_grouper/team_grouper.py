from typing import List, Tuple
import random
import argparse

def group_names(names: List[Tuple[str, str, str]], num_groups: int) -> List[List[Tuple[str, str, str]]]:
    random.shuffle(names)
    groups = [[] for _ in range(num_groups)]
    for i, name in enumerate(names):
        groups[i % num_groups].append(name)
    return groups

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

    print("Remote Groups:")
    for i, group in enumerate(remote_groups, 1):
        formatted_group = [(name, team) for name, team, _ in group]
        print(f"Group {i}: {formatted_group}")

    print("\nOffice Groups:")
    for i, group in enumerate(office_groups, 1):
        formatted_group = [(name, team) for name, team, _ in group]
        print(f"Group {i}: {formatted_group}")

if __name__ == "__main__":
    main()
