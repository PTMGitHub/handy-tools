# 1, 2, 4, all pair organiser.

This programme is designed to;
* organise a list of names into groups
* assigns a platform team to each group.
* List out unassigned platform teams

Inputs:
* name
* team
* remote or office
* Number of remote groups
* Number of office groups

It has the following constraint:
* Randomly assigns groups
* tries to separate those in the same teams
* assigns a platform team once across the remote and office assignments
* assigns a platform team to a group without a member of that platform team is in


## Usage
```bash
poetry run python team_grouper/team_grouper.py 2 3 "<name1>,<team>,<office/remote>" "<name2>,<team>,<office/remote>" "<name3>,<team>,<office/remote>"  
```