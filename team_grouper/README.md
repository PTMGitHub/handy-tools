# Team grouper.

There are 2 versions

## team_grouper/team_grouper.py
This programme is designed to;
* organise a list of names into groups

It has the following constraint:
* Randomly assigns groups
* tries to separate those in the same teams (Not totally sure on this need to double check)

## team_grouper_assign_platform_team.py
This programme is designed to;
* organise a list of names into groups
* assigns a platform team to each group.
* List out unassigned platform teams

It has the following constraint:
* Randomly assigns groups
* tries to separate those in the same teams
* assigns a platform team once across the remote and office assignments
* assigns a platform team to a group without a member of that platform team is in
* 
## Inputs:
* name
* team
* remote or office
* Number of remote groups
* Number of office groups


## Usage
```bash
poetry run python team_grouper/<team_grouper_assign_platform_team/team_grouper>.py <int_num_of_remote_groups> <int_num_of_office_groups> "<name1>,<team>,<office/remote>" "<name2>,<team>,<office/remote>" "<name3>,<team>,<office/remote>"  
```