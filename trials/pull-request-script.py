#!/usr/bin/env python3
""" This script could be useful for retreiving filters from filters.xlsx,
    analysing them, adding to correct easylistpolish files, 
    auto commiting changes and creating pull-request message. 
    
    Run with 0-3 parameters:
    script.py [branch-name [path_to_repository [onlyfix]]] """

# Import key modules
import datetime, sys
import pandas as pd
from git import Repo

# Set default location of easylistpolish repository and its files
REPOPATH = "easylistpolish"
DIRPATH = "\\easylistpolish\\easylistpolish_"

# Set default names and options
BRANCH = "update-proposals-2"
FILEREAD = "filters.xlsx"
FILTERSHEET = 'filters'
ONLYFIX = 'no'


def setup():
    """ If any command-line param is set, change default ones """
    if len(sys.argv) == 2:
        BRANCH = str(sys.argv[1])
    elif len(sys.argv) == 3:
        REPOPATH = str(sys.argv[2])
    elif len(sys.argv) == 4:
        ONLYFIX = str(sys.argv[3])


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
    """ Open and return git repository on selected branch """
    repo = Repo(repo_path)
    assert not repo.bare
    repo.git.checkout(branch)
    return repo


def repo_commit(repo, message):
    """ Add last changes and commit with commit message """
    repo.git.add(update=True)
    repo.git.commit('-m', message)
    print("> commit: \t" + message)
    return str(repo.head.commit)[:7]


def get_site_from_link(link, domains):
    """ Cut link with domain from hyperlink """
    newlink = link[link.find('://')+3:]    
    if newlink[:3] == 'www': 
        newlink = newlink[4:]

    # check if link has valid domain
    # and return site name in site.domain format
    for domain in domains:
        result = newlink.find(domain)
        if result != -1:
            location = result+len(domain)
            return newlink[:location]


def convert_to_md_link(link, notes, domains):
    """ Return hyperlink in .md format and site name with optional notes"""
    site = get_site_from_link(link, domains)
    if notes == "":
        return "[" + link + "]("+ site + ")\n", site
    else:
        return "[" + link + "]("+ site + " - " + notes + ")\n", site + " - " + notes
    

def add_commit_create_pull(sheet, repo):
    """ Check if key cells have valid content, 
        add filters to easylistpolish files,
        commit changes,
        create pull-request message for all commits """
    domains = domains_to_list(FILEREAD)
    pull = open_file_to_write()
    commit_msg = ""

    # Iterate through whole sheet
    for i in range(5): # sheet.index:
        CHECK = sheet['Check'][i]
        PUSH = sheet['Push'][i]
        LINK = sheet['Link'][i]
        
        # If filter is checked and wasn't pushed before
        if (CHECK=='yes' and PUSH=='no'):

            # Set rest of the params
            NUMBER = str(sheet['No'][i])[:-2]
            FILTER = sheet['Filter'][i]
            FILTERTYPE = sheet['Type'][i]

            # If link is not empty, add another hyperlink to pull-request file
            if LINK != "":
                MD_LINK = convert_to_md_link(LINK, sheet['Notes'][i], domains)

            # If number is empty, add next hyperlink (if no filter) or next filter
            if NUMBER is "":
                if FILTER is "":
                    pull.write(MD_LINK[0])
                else:
                    write_filter_to_file(FILTERTYPE, FILTER)

            # If number is NOT empty, commit previous changes and add next filter
            else:
                if commit_msg != "":
                    COMMIT = repo_commit(repo, commit_msg)
                    pull.write(COMMIT + "\n")

                write_filter_to_file(FILTERTYPE, FILTER)
                commit_msg = MD_LINK[1]

                # Compose pull-request message
                pull.write("\n")
                pull.write("__________________________\n")
                pull.write("**# " + NUMBER + "**\n")
                pull.write(MD_LINK[0])   

    # Commit last changes
    if commit_msg != "":
        COMMIT = repo_commit(repo, commit_msg)
        pull.write(COMMIT + "\n")


def main():
    """ Main """
    print("> script: commit-filters-from-xls.py is running")
    setup()
    sheet = open_sheet(FILEREAD, FILTERSHEET)
    repo = repo_open(REPOPATH, BRANCH)
    add_commit_create_pull(sheet, repo)
    print("> script: commit-filters-from-xls.py has finished all tasks")


if __name__== "__main__":
  main()

