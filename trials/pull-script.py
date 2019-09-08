# git log --pretty=oneline --after="2019-7-25" > "C:\Users\Bartek\OneDrive\02_PROJEKTY\01_Projekty_praca\AdblockPlus\filters\pull-requests\commits.txt"

import datetime

path = 'C:\\Users\\Bartek\\OneDrive\\02_PROJEKTY\\01_Projekty_praca\\AdblockPlus\\filters\\pull-requests\\'
file_read = path + "commits.txt"
file_write = path + str(datetime.datetime.now())[:19].replace(":","-") + ".txt"
i = 1

commits = [line.rstrip('\n') for line in open(file_read)]
pull_request = open(file_write, "x")

for commit in commits:
    pull_request.write("**# " + str(i) + "**\n")
    pull_request.write(commit[:7] + "\n")
    pull_request.write("[" + commit[41:] + "](" +")\n")
    pull_request.write("\n")
    pull_request.write("__________________________\n")
    i += 1
