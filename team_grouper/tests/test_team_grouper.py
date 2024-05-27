from team_grouper.team_grouper import group_names, ensure_unique_team_group, assign_platform_teams, PLATFORM_TEAMS

def test_group_names():
    remote_names = [
        ("Alice Johnson", "Team1", "remote"), ("Charlie Brown", "Team3", "remote"),
        ("Eve Davis", "Team2", "remote"), ("Grace Hopper", "Team1", "remote")
    ]
    office_names = [
        ("Bob Smith", "Team2", "office"), ("David Lee", "Team1", "office"),
        ("Frank Wright", "Team3", "office"), ("Heidi Klum", "Team2", "office")
    ]
    num_remote_groups = 2
    num_office_groups = 2

    remote_groups = group_names(remote_names, num_remote_groups)
    office_groups = group_names(office_names, num_office_groups)

    assert len(remote_groups) == num_remote_groups
    assert len(office_groups) == num_office_groups
    assert all(len(group) <= (len(remote_names) // num_remote_groups) + 1 for group in remote_groups)
    assert all(len(group) <= (len(office_names) // num_office_groups) + 1 for group in office_groups)

def test_ensure_unique_team_group():
    remote_names = [
        ("Alice Johnson", "Team1", "remote"), ("Charlie Brown", "Team3", "remote"),
        ("Eve Davis", "Team2", "remote"), ("Grace Hopper", "Team1", "remote")
    ]
    office_names = [
        ("Bob Smith", "Team2", "office"), ("David Lee", "Team1", "office"),
        ("Frank Wright", "Team3", "office"), ("Heidi Klum", "Team2", "office")
    ]
    num_remote_groups = 2
    num_office_groups = 2

    remote_groups = group_names(remote_names, num_remote_groups)
    office_groups = group_names(office_names, num_office_groups)

    remote_groups = ensure_unique_team_group(remote_groups)
    office_groups = ensure_unique_team_group(office_groups)

    unique_team_remote_groups = [group for group in remote_groups if len({team for _, team, _ in group}) == len(group)]
    unique_team_office_groups = [group for group in office_groups if len({team for _, team, _ in group}) == len(group)]

    assert len(unique_team_remote_groups) >= 1 or len(unique_team_office_groups) >= 1

def test_assign_platform_teams():
    remote_names = [
        ("Alice Johnson", "Team1", "remote"), ("Charlie Brown", "Team3", "remote"),
        ("Eve Davis", "Team2", "remote"), ("Grace Hopper", "Team1", "remote")
    ]
    office_names = [
        ("Bob Smith", "Team2", "office"), ("David Lee", "Team1", "office"),
        ("Frank Wright", "Team3", "office"), ("Heidi Klum", "Team2", "office")
    ]
    num_remote_groups = 2
    num_office_groups = 2

    remote_groups = group_names(remote_names, num_remote_groups)
    office_groups = group_names(office_names, num_office_groups)

    remote_groups = ensure_unique_team_group(remote_groups)
    office_groups = ensure_unique_team_group(office_groups)

    remote_groups_with_platform = assign_platform_teams(remote_groups)
    office_groups_with_platform = assign_platform_teams(office_groups)

    for platform_team, group in remote_groups_with_platform:
        assert platform_team in PLATFORM_TEAMS
        assert all(member_team != platform_team for _, member_team, _ in group)

    for platform_team, group in office_groups_with_platform:
        assert platform_team in PLATFORM_TEAMS
        assert all(member_team != platform_team for _, member_team, _ in group)

if __name__ == "__main__":
    test_group_names()
    test_ensure_unique_team_group()
    test_assign_platform_teams()
    print("All tests passed!")
