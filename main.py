from github import Github

# Authentication is defined via github.Auth
from github import Auth

from ChangeRephraser import ChangeRephraser

TOKEN = open("token", "r").read()
PR_NUMBER = 5
REPO_NAME = "mohmiim/Algo"

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
print(change)
print(rephraser.convert(change).get("description"))
g.close()
