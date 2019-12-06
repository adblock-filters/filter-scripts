#!/usr/bin/env python3
""" Filters Pull Request Script """


# Import key modules
import datetime, sys, os, subprocess, time, argparse
import pandas as pd
from git import Repo


# Set default parameters
REPOPATH =      "../easylistpolish"
DIRPATH =       "/easylistpolish/easylistpolish_"
PUSHTO =        'origin' 
FROMUSER =      'adblock-filters'
TOUSER =        'easylistpolish'
TOBRANCH =      'master'
IMAGES =        'https://raw.githubusercontent.com/adblock-filters/filter-scripts/master/screens/'
FILEREAD =      'filters-testing.xlsx'
FILTERSHEET =   'filters'


def parser():
    """ Parse arguments """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--from",   default=FROMUSER,   help="pull-request FROM this user")
    parser.add_argument("--to",     default=TOUSER,     help="pull-request TO this user")
    parser.add_argument("--branch", default=TOBRANCH,   help="pull-request to this branch")
    parser.add_argument("--repo",   default=REPOPATH,   help="path to easylist repository")
    parser.add_argument("--dir",    default=DIRPATH,    help="directory and filenames of filters lists")
    parser.add_argument("--images", default=IMAGES,     help="link to images")
    parser.add_argument("--pushto", default=PUSHTO,     help="origin / github / upstream etc.")
    parser.add_argument("--read",   default=FILEREAD,   help="read filters from specified .xlsx")
    parser.add_argument("--sheet",  default=FILTERSHEET,help="name of sheet with filters list")
    
    return parser.parse_args()


def getFilterfiles():
    """ Open particular file from easylist repo """
    path = f"{REPOPATH}{DIRPATH}"
    files = {
        'BLOCK':        (f"{path}specific_block.txt"),
        'HIDE':         (f"{path}specific_hide.txt"),
        'POPUP':        (f"{path}specific_block_popup.txt"),
        '3RD':          (f"{path}thirdparty.txt"),
        '3RDPOPUP':     (f"{path}thirdparty_popup.txt"),
        'AD':           (f"{path}adservers.txt"),
        'ADPOPUP':      (f"{path}adservers_popup.txt"),
        'WHITE':        (f"{path}whitelist.txt"),
        'WHITEDIM':     (f"{path}whitelist_dimensions.txt"),
        'WHITEPOPUP':   (f"{path}whitelist_popup.txt"),
        'GENBLOCK':     (f"{path}general_block.txt"),
        'GENHIDE':      (f"{path}general_hide.txt"),
        'GENPOPUP':     (f"{path}general_block_popup.txt"),
        }
    return files


def writeFilterToFile(filtertype, filter):
    """ Write filter to particular file """
    filename = getFilterfiles().get(filtertype)
    try:
        f = open(filename, 'a')
    except OSError:
        print (f"Could not open/read file: {filename}")
        sys.exit()
    with f:
        f.write(filter + "\n")
        f.close()
        print(f"> write:\t {filter}")


def openSheet(file_path, sheetname):
    """ Open and return .xls sheet """
    sheet = pd.read_excel(file_path, sheetname)
    sheet = sheet.fillna('')
    return sheet


def domainsToList(filepath):
    """ Open domains list from .xls sheet and put them in an array """
    domainsheet = openSheet(filepath, 'domains')
    domains = []
    for i in domainsheet.index:
        domains.append(domainsheet['Domain'][i])
    return domains


def openRepo(repo_path, branch):
    """ Open and return git repository on new branch """
    repo = Repo(repo_path)
    assert not repo.bare

    repo.git.checkout('master')
    repo.git.branch(branch)
    repo.git.checkout(branch)

    return repo


def commitAndPush(repo, message):
    """ Add last changes, commit and push to remote """
    try:
        repo.git.add(update=True)
        repo.git.commit('-m', message)
    except:
        print('An error occured while committing') 
# try:
    origin = repo.remote(name = PUSHTO)
    # origin.push('--set-upstream', 'origin')
    # repo.git.config('credential.helper', 'store')

    repo.git.push('--set-upstream', 'origin', str(repo.active_branch.name))
    print(f"> commit {str(repo.head.commit)[:7]} {message}")
# except:
    # print('An error occured while pushing the code, check if your credentials are stored')  



def getSiteFromLink(link, domains):
    """ Cut link with domain from hyperlink """
    newlink = link[link.find('://')+3:]

    if newlink[:3] == 'www': 
        newlink = newlink[4:]
    # check if link has a valid domain and return sitename in website.domain format
    for domain in domains:
        result = newlink.find(domain)
        if result != -1:
            location = result+len(domain)
            return newlink[:location]
        
    return newlink.replace("/","-")


def convertToMdLink(link, notes, domains):
    """ Create hyperlink in .md format and commit msg with optional notes"""
    site = getSiteFromLink(link, domains)
    if not notes:
        return f"[{site}]({link})", site
    else:
        notes = str(notes).replace(" ","-")
        return f"[{site}-{notes}]({link})", f"{site}-{notes}"


def runPowerShell(branch, link, title):
    """ Run PowerShell command
    EXAMPLE: 
    cd ..\easylistpolish\ ; 
    hub pull-request --base adblock-filters:master --head adblock-filters:filterpatch-133 
    --message "dziennikpolski24.pl-xmlhttprequest" 
    --message "-[dziennikpolski24.pl-xmlhttprequest](https://dziennikpolski24.pl/)" 
    --message "![image](https://raw.githubusercontent.com/adblock-filters/foo/master/screens/dziennikpolski24.pl-xmlhttprequest.png)"; 
    cd ..\filter-scripts\;          
    """
    goto_dir = f"cd {REPOPATH}"
    returnto_dir = 'cd ../filter-scripts/' #TODO my dir
    hubcommand = 'hub pull-request'
    base = f"{TOUSER}:{TOBRANCH}"
    head = f"{FROMUSER}:{branch}"
    pulltitle = f"\"{title}\""
    hyperlink = f"\"{link}\""
    image = (f'\"![image]({IMAGES}{title}.png)\"')
    
    # IF WINDOWS
    # ps_script = (f'{goto_dir} ; {hubcommand} --base {base} --head {head} --message {pulltitle} --message {hyperlink} --message {image}; {returnto_dir};')
    # print(ps_script)
    # p = subprocess.Popen(["powershell.exe", ps_script], stdout=sys.stdout)
    # p.communicate()

    # IF LINUX
    ps_script = (f'{hubcommand} --base {base} --head {head} --message {pulltitle} --message {hyperlink} --message {image}')
    print(ps_script)
    wd = os.getcwd()
    os.chdir("../easylistpolish/")
    subprocess.Popen(ps_script, shell=True)
    os.chdir(wd)


def filtersPullRequest():
    """ Check if key cells have valid content, 
        add filters to easylistpolish files,
        commit changes,
        create pull-request message for all commits """
    
    sheet = openSheet(FILEREAD, FILTERSHEET)
    domains = domainsToList(FILEREAD)

    commitmsg = ""
    previouslink = ""
    branch = "filterpatch-init"

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
            if LINK:
                hyperlink, newmsg = convertToMdLink(LINK, sheet['Notes'][i], domains)

            # If number is empty (so we continue in same commit)
            if not NUMBER:
                if not FILTER:  # add hyperlink
                    previouslink = f"{previouslink}-{hyperlink}"
                else:           # add filter
                    writeFilterToFile(FILTERTYPE, FILTER)

            # If we have new number (= new set of filters), commit RECENT changes (previous filter) and add next filter
            else:
                # Commit recent changes and reset variables
                if branch != "filterpatch-init": # if it's not first commit
                    commitAndPush(repo, commitmsg)
                    runPowerShell(branch, previouslink, commitmsg)
                    previouslink = ""

                # Add new filter on new branch
                previouslink = f"{previouslink}-{hyperlink}"
                branch = f"filterpatch-{NUMBER}"
                repo = openRepo(REPOPATH, branch)                                  
                writeFilterToFile(FILTERTYPE, FILTER) 
                commitmsg = newmsg

    # Commit last change - last filter(s) from list
    if commitmsg:
        commitAndPush(repo, commitmsg)
        runPowerShell(branch, previouslink, commitmsg)

    repo.git.checkout('master')



def main():
    
    args = parser()

    print(
    """\n##### Filters Pull Request Script ##### 

    Attention, script will: 
    - create and checkout to the new dedicated branch for each filter from file,
    - add filter (or set of filters) to the proper easylist file(s),
    - commit change(s) and immediately push,
    - create pull-request message for those commits and perform pull-request using *hub* extension
    Abort if you don't want to create unnecessary branches and pull-requests.
    """ )
    print("##### Selected options ##### \n")
    print(args)

    input("> Press Enter to start...")
    print("\n##### Script is running ##### \n")
    start = time.time()
    
    filtersPullRequest()

    end = time.time()
    print(f"##### Finished in {round(end-start,2)}s ##### \n")


if __name__== "__main__":
  main()

