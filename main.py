from github import Github

# Authentication is defined via github.Auth
from github import Auth

from ChangeRephraser import ChangeRephraser


def update_pr_description(repo_name, pr_number, new_description):
    g = Github(TOKEN)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    pr.edit(body=new_description)


PR_NUMBER = 5
REPO_NAME = "mohmiim/Algo"
TOKEN = open("token", "r").read()
# using an access token
auth = Auth.Token(TOKEN)

# First create a Github instance:
# Public Web Github
g = Github(auth=auth)

# Github Enterprise with custom hostname
# g = Github(base_url="https://{hostname}/api/v3", auth=auth)

repo = g.get_repo(REPO_NAME, lazy=False)
pr = repo.get_pull(PR_NUMBER)
changed_files = pr.get_files()
change = "changes : \n"
for changed_file in changed_files:
    change += " The file : " + changed_file.filename + " has been"
    if changed_file.status == "added":
        change += " added, "
    elif changed_file.status == "removed":
        change += " removed, "
    elif changed_file.status == "modified":
        change += " modified, "

    change += " the change in github patch format is : \n\t" + changed_file.patch + "\n\n"
    changes = changed_file.changes
    status = changed_file.status
    additions = changed_file.additions
    deletion = changed_file.deletions
    patch = changed_file.patch

rephraser = ChangeRephraser()
description = rephraser.convert(change)
update_pr_description(REPO_NAME, PR_NUMBER, description)
g.close()
