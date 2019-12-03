#!/usr/bin/env python3
""" This script could be useful for retreiving filters from filters.xlsx,
    inserting them to correct easylistpolish file, commiting changes automatically 
    after each insert and creating pull-request message. 
    
    Run with 0-3 parameters:
    python script.py [branch-name [path_to_repository [onlyfix]]] """

### HUB COMMAND
"""
- first message is PR title
- msgs are conncatenated with blank line btwn
- see: https://hub.github.com/hub-pull-request.1.html
hub pull-request --base easylistpolish:master --head adblock-filters:update-127 --message portaltatrzanski --message "![image](https://raw.githubusercontent.com/adblock-filters/filter-scripts/master/screens/portaltatrzanski.pl.png)" --message "[http://portaltatrzanski.pl/](http://portaltatrzanski.pl/)"
"""

# Import key modules
import datetime, sys, os, subprocess
import pandas as pd
from git import Repo

# Set default location of easylistpolish repository and its files
REPOPATH = "..\\easylistpolish"
DIRPATH = "\\easylistpolish\\easylistpolish_"

# Set default names and options
FILEREAD = "filters-testing.xlsx"
FILTERSHEET = 'filters'
ONLYFIX = 'no' # TODO


def setup():
    """ If any command-line param is set, change default ones """
    if len(sys.argv) == 2:
        BRANCH = str(sys.argv[1]) # to fix
    elif len(sys.argv) == 3:
        REPOPATH = str(sys.argv[2]) # to fix
    elif len(sys.argv) == 4:
        ONLYFIX = str(sys.argv[3]) # to fix


def open_file_to_write():
    """ Create and set the name of the .txt file with pull message in .md format """
    file_write = "pulls\\pull-request-" + str(datetime.datetime.now())[:19].replace(":","") + ".txt"
    openfile = open(file_write, "x")
    return openfile


def open_filter_lists():
    """ Open particular file from easylistpolish repo """
    files = {
        'BLOCK': open(REPOPATH + DIRPATH + "specific_block.txt", "a"),
        'HIDE': open(REPOPATH + DIRPATH + "specific_hide.txt", "a"),
        'POPUP': open(REPOPATH + DIRPATH + "specific_block_popup.txt", "a"),
        '3RD': open(REPOPATH + DIRPATH + "thirdparty.txt", "a"),
        '3RDPOPUP': open(REPOPATH + DIRPATH + "thirdparty_popup.txt", "a"), 
        'AD': open(REPOPATH + DIRPATH + "adservers.txt", "a"),
        'ADPOPUP': open(REPOPATH + DIRPATH + "adservers_popup.txt", "a"), 
        'WHITE': open(REPOPATH + DIRPATH + "whitelist.txt", "a"),
        'WHITEDIM': open(REPOPATH + DIRPATH + "whitelist_dimensions.txt", "a"), 
        'WHITEPOPUP': open(REPOPATH + DIRPATH + "whitelist_popup.txt", "a"),
        'GENBLOCK': open(REPOPATH + DIRPATH + "general_block.txt", "a"),
        'GENHIDE': open(REPOPATH + DIRPATH + "general_hide.txt", "a"),
        'GENPOPUP': open(REPOPATH + DIRPATH + "general_block_popup.txt", "a"), 
        }
    return files


def write_filter_to_file(filtertype, filter):
    """ Write filter to particular file """
    files = open_filter_lists()
    filter_file = files.get(filtertype)
    filter_file.write(filter  + "\n")
    filter_file.close()
    print(f"> write:\t {filter}")


def open_sheet(file_path, sheetname):
    """ Open and return .xls sheet """
    sheet = pd.read_excel(file_path, sheetname)
    sheet = sheet.fillna('')
    return sheet


def domains_to_list(file_path):
    """ Open domains list from .xls and return python list of them """
    domains_sheet = pd.read_excel(file_path, 'domains')
    domains = []
    for i in domains_sheet.index:
        domains.append(domains_sheet['Domain'][i])
    return domains


def repo_open(repo_path, branch):
    """ Open and return git repository on new branch """
    repo = Repo(repo_path)
    assert not repo.bare
    repo.git.checkout('master')
    repo.git.branch(branch)
    repo.git.checkout(branch)
    return repo


def repo_commit(repo, message):
    """ Add last changes and commit with commit message """
    repo.git.add(update=True)
    repo.git.commit('-m', message)
    print(f"> commit:\t {message}")
    return str(repo.head.commit)[:7]


def get_site_from_link(link, domains):
    """ Cut link with domain from hyperlink """
    newlink = link[link.find('://')+3:]    
    if newlink[:3] == 'www': 
        newlink = newlink[4:]

    # check if link has a valid domain
    # and return site name in website.domain format
    for domain in domains:
        result = newlink.find(domain)
        if result != -1:
            location = result+len(domain)
            return newlink[:location]


def convert_to_md_link(link, notes, domains):
    """ Return: hyperlink in .md format, site name with optional notes"""
    site = get_site_from_link(link, domains)
    if notes == "":
        return "[" + site + "](" + link + ")\n", site
    else:
        return "[" + site + "-" + str(notes) + "](" + link + ")\n", site + "-" + str(notes)


def runPowerShell(branch, link, title):
    goto_dir = 'cd ..\\easylistpolish\\'
    returnto_dir = 'cd ..\\filter-scripts\\'
    hub = 'hub pull-request'
    base = 'adblock-filters:master'
    head = 'adblock-filters:' + branch
    title = title
    link = link
    image = (f'\"![image](https://raw.githubusercontent.com/adblock-filters/filter-scripts/master/screens/{title}.png)\"')
    ps_script = (f'{goto_dir} ; {hub} --base {base} --head {head} --message {title} --message {link} --message {image}; {returnto_dir};')
    print(ps_script)
    # hub pull-request --base adblock-filters:master --head adblock-filters:update-127 --message portaltatrzanski --message "![image](https://raw.githubusercontent.com/adblock-filters/filter-scripts/master/screens/portaltatrzanski.pl.png)" --message "[http://portaltatrzanski.pl/](http://portaltatrzanski.pl/)"; cd ..\\filter-scripts\\ '
                    
    p = subprocess.Popen(["powershell.exe", ps_script], stdout=sys.stdout)
    p.communicate()

def add_commit_create_pull(sheet):
    """ Check if key cells have valid content, 
        add filters to easylistpolish files,
        commit changes,
        create pull-request message for all commits """
    domains = domains_to_list(FILEREAD)
    # pull = open_file_to_write()
    commit_msg = ""
    PREV_LINK = ""
    BRANCH = "filterpatch-init"

    # Iterate through whole sheet
    for i in sheet.index:
        CHECK = sheet['Check'][i]
        PUSH = sheet['Push'][i]
        LINK = sheet['Link'][i]
        
        # If filter is checked and hasn't been pushed yet
        if (CHECK=='yes' and PUSH=='no'):

            # Set rest of the params from sheet
            NUMBER = str(sheet['No'][i])[:-2]
            FILTER = sheet['Filter'][i]
            FILTERTYPE = sheet['Type'][i]

            # If link is not empty (so we have a new link), create .md format hyperlink with optional notes
            if LINK != "":
                MD_LINK = convert_to_md_link(LINK, sheet['Notes'][i], domains)

            # If number is empty (so we continue in same commit), 
            # add next hyperlink (if no filter) or next filter
            if NUMBER is "":
                if FILTER is "":
                    PREV_LINK = PREV_LINK + "+" + MD_LINK[0]
                else:
                    write_filter_to_file(FILTERTYPE, FILTER)

            # If number is NOT empty (so we have new number = new set of filters), 
            # commit previous changes and add next filter
            else:
                # commit last changes and reset variables
                if BRANCH != "filterpatch-init": # if it's not first commit
                    COMMIT = repo_commit(repo, commit_msg)
                    runPowerShell(BRANCH, PREV_LINK, commit_msg)
                    PREV_LINK = ""

                # create new set
                PREV_LINK = PREV_LINK + "+" + MD_LINK[0]
                BRANCH = "filterpatch-" + NUMBER

                repo = repo_open(REPOPATH, BRANCH)                                  
                write_filter_to_file(FILTERTYPE, FILTER) # OPEN REPO ON BRANCH == NUMBER
                commit_msg = MD_LINK[1]                  # COMMIT IMMIDIATELY == P R O B L E M !

                # COMMIT = repo_commit(repo, commit_msg)
                # runPowerShell(BRANCH, PREV_LINK, commit_msg)

                
                
                # PREBRANCH = BRANCH


    # # Commit last change (last filter from list)
    if commit_msg != "":
        COMMIT = repo_commit(repo, commit_msg)
        runPowerShell(BRANCH, PREV_LINK, commit_msg)

    repo.git.checkout('master')



def main():
    """ Main """
    print("> script is running")
    setup()
    sheet = open_sheet(FILEREAD, FILTERSHEET)
    add_commit_create_pull(sheet)
    print("> script has finished")


if __name__== "__main__":
  main()

