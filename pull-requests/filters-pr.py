#!/usr/bin/env python3

""" Filters Pull Request Script 
    - create and checkout to the new dedicated branch for each filter from file,
    - add filter (or set of filters) to the proper easylist file(s),
    - commit change(s) and immediately push,
    - create pull-request message for those commits and perform pull-request using *hub* extension
"""


# Import key modules
import datetime, sys, os, time, argparse
import pandas as pd
from git import Repo
from subprocess import Popen, PIPE


# Set default parameters
REPOPATH =      "../../easylistpolish"
DIRPATH =       "/easylistpolish/easylistpolish_"
PUSHTO =        'origin' 
FROMUSER =      'adblock-filters'
TOUSER =        'easylistpolish'
TOBRANCH =      'master'
IMAGES =        'https://raw.githubusercontent.com/adblock-filters/filter-scripts/master/screens/'
FILEREAD =      'filters.xlsx'
FILTERSHEET =   'filters'


def parser():
    """ Parse arguments """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--from-user",  default=FROMUSER,   help="pull-request FROM USER repo")
    parser.add_argument("--to-user",    default=TOUSER,     help="pull-request TO USER repo")
    parser.add_argument("--branch",     default=TOBRANCH,   help="pull-request to selected branch")
    parser.add_argument("--repo",       default=REPOPATH,   help="path to filter lists repository (i.e. easylsit)")
    parser.add_argument("--dir",        default=DIRPATH,    help="directory and filenames of filters lists")
    parser.add_argument("--images",     default=IMAGES,     help="url to images web directory")
    parser.add_argument("--push-to",    default=PUSHTO,     help="origin / github / upstream etc.")
    parser.add_argument("--read-from",  default=FILEREAD,   help="read filters from specified .xlsx file")
    parser.add_argument("--sheet",      default=FILTERSHEET,help="name of sheet with filter list")
    
    return parser.parse_args()


def getFilterfiles(args):
    """ Open particular file from easylist repo """
    path = f"{args.repo}{args.dir}"
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


def writeFilterToFile(args, filtertype, filter):
    """ Write filter to particular file """
    filename = getFilterfiles(args).get(filtertype)
    try:
        f = open(filename, 'a')
    except OSError:
        print (f"Could not open/read file: {filename}")
        sys.exit()
    with f:
        f.write(filter + "\n")
        f.close()
        print(f" - - - - - ")
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


def commitAndPush(pushto, repo, message):
    """ Add last changes, commit and push to remote """
    try:
        repo.git.add(update=True)
        repo.git.commit('-m', message)
        # repo.git.push('origin', str(repo.active_branch.name))
    except:
        print('An error occured while committing') 

    # try:
    #     origin = repo.remote(name = pushto)
    #     repo.git.pull('https://github.com/adblock-filters/easylistpolish.git', str(repo.active_branch.name))
    #     repo.git.push('--set-upstream', pushto, str(repo.active_branch.name))
    #     print(f"> commit {str(repo.head.commit)[:7]} {message}")

    # except:
    #     print('An error occured while pushing the code, check if your credentials are stored')  



def getSiteFromLink(link, domains):
    """ Cut link with domain from hyperlink """
    newlink = link[link.find('://')+3:]

    if newlink[:3] == 'www': 
        newlink = newlink[4:]
    # check if link has a known domain and return sitename in website.domain format
    for domain in domains:
        result = newlink.find(domain)
        if result != -1:
            location = result+len(domain)
            return newlink[:location]
    # if domian is unknown    
    return newlink.replace("/","-")


def convertToMdLink(link, notes, domains):
    """ Create hyperlink in .md format and commit msg with optional notes"""
    site = getSiteFromLink(link, domains)
    if not notes:
        return f"[{site}]({link})", site
    else:
        notes = str(notes).replace(" ","-")
        return f"[{site}-{notes}]({link})", f"{site}-{notes}"


def runPowerShell(args, branch, link, title):
    """ Run PowerShell command  """
    base = f'{args.to_user}:{args.branch}'
    head = f'{args.from_user}:{branch}'
    image = (f'![image]({args.images}{title}.png)')
    ps_script = (f'hub pull-request --push --base {base} --head {head} --message \"{title}\" --message \"{link}\" --message \"{image}\"')
    print(ps_script)

    wd = os.getcwd()
    os.chdir(args.repo)

    # LINUX
    if sys.platform.startswith('linux'):
        p = Popen(ps_script, stdin=PIPE, shell=True)
        p.communicate()
        
    # WINDOWS
    elif sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
        p = Popen(["powershell.exe", ps_script], stdout=sys.stdout)
        p.communicate()

    os.chdir(wd)


def filtersPullRequest(args):
    """ Check if key cells have valid content, add filters to easylistpolish files,
        commit changes, create pull-request message for all commits """
    
    sheet = openSheet(args.read_from, args.sheet)
    domains = domainsToList(args.read_from)

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
                    writeFilterToFile(args, FILTERTYPE, FILTER)

            # If we have new number (= new set of filters), commit RECENT changes (previous filter) and add next filter
            else:
                # Commit recent changes and reset variables
                # if it's not first commit
                if branch != "filterpatch-init": 
                    commitAndPush(args.push_to, repo, commitmsg)
                    runPowerShell(args, branch, previouslink, commitmsg)
                    previouslink = ""

                # Add new filter on new branch
                previouslink = f"{previouslink}-{hyperlink}"
                branch = f"filterpatch-{NUMBER}"
                repo = openRepo(args.repo, branch)                                  
                writeFilterToFile(args, FILTERTYPE, FILTER) 
                commitmsg = newmsg

    # Commit last change - last filter(s) from list
    if commitmsg:
        commitAndPush(args.push_to, repo, commitmsg)
        runPowerShell(args, branch, previouslink, commitmsg)

    repo.git.checkout('master')


def measureTime(func, *arg):
    start = time.time()
    func(*arg)
    end = time.time()
    print(f"\n-> finished in {round(end-start,2)}s")
    return end - start


def listArguments(args):
    for name, value in args._get_kwargs():
        if value is not None:
            print('{0:10}  {1}'.format(name, value))


def main():
    print("### Filters Pull Request Script ###\n")
    print("> this script will modify filter files, create extra branches and pull-requests") 
    print("> selected options:\n")

    args = parser()
    listArguments(args)            
    input("\n> press Enter to start...")
    
    print("> script is running \n")
    measureTime(filtersPullRequest, args)
   

if __name__== "__main__":
  main()

