import os, argparse

USER = ''
BRANCH = ''
USER_BRANCH = ''
# parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("user", help="display a square of a given number")
    parser.add_argument("branch", help="display a square of a given number")
    args = parser.parse_args()
    USER = args.user
    BRANCH = args.branch
    USER_BRANCH = f"{USER}-{BRANCH}"


def git_pull():
    print(f"merge pull request: {USER_BRANCH} to master")

    git_pull_master 	= "git pull"
    checkout_to_branch 	= f"git checkout -b {USER_BRANCH} master"
    pull_from_branch 	= f"git pull https://github.com/{USER}/easylistpolish.git {BRANCH}"

    # pull
    print(f"pull from {USER_BRANCH}")
    os.system(git_pull_master)
    os.system(checkout_to_branch)
    os.system(pull_from_branch)


def git_merge():
    git_add 		    = "git add ."
    commit_conflicts 	= "git commit -m \"resolve conflicts\""
    push_to_branch 		= f"git push origin {USER_BRANCH}"
    checkout_master 	= "git checkout master"

    merge_branch 		= f"git merge --no-ff {USER_BRANCH}"
    commit_merge		= "git commit -m \"merge\""
    git_push_master 	= "git push origin master"

    # commit and push
    print(f"commit and push to {USER_BRANCH}")
    os.system(git_add)
    os.system(commit_conflicts)
    os.system(push_to_branch)
    os.system(checkout_master)

    # merge
    print(f"merge to master")
    os.system(merge_branch)
    os.system(commit_merge)
    os.system(git_push_master)

    print(f"PR {BRANCH} merged")


def ask_user():
    check = str(input("Changes provided and saved? (y/n): ")).lower().strip()
    try:
        if check[0] == 'y':
            return True
        elif check[0] == 'n':
            return False
        else:
            print('Invalid Input')
            return ask_user()
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return ask_user()


def main():
    parse()
    if (len(USER_BRANCH) > 1):
        git_pull()
        ask_user()
        git_merge()