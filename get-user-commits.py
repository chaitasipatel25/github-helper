!/usr/bin/python

# python3 ./get-user-commits.py -t <github token> -o <github owner> -r <repo> -g <github user> -d <directory> -s <since date> -u <until date>
#
# Script to inspect Github and pull all commits for the given user.

import requests
import os
import json
import getopt
import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def Usage():
  print("Usage: %s -t <github token> -o <github owner> -r <repo> -g <github user> -d <directory> -s <since date> -u <until date>" % sys.argv[0])
  print("  -t <github token>  github token")
  print("  -o <github owner>  github owner/org")
  print("  -r <repo>          specific repo")
  print("  -g <github user>   github user name")
  print("  -d <directory>     (optional) local directory to put file for commits")
  print("  -s <since date>    (optional) since date isoformat")
  print("  -u <until date>    (optional) until date isoformat")

def main():
    githubToken = ''
    githubOwner = ''
    currentRepo = ''
    githubUser = ''
    destDirectory = os.getcwd()
    sinceDate = (datetime.now()-relativedelta(years=1)).isoformat()
    untilDate = datetime.now().isoformat()

    try:
    # process command arguments
        ouropts, args = getopt.getopt(sys.argv[1:],"t:o:r:g:d:s:u:h")
        for o, a in ouropts:
          if   o == '-t':
            githubToken = a
          if   o == '-o':
            githubOwner = a
          if   o == '-r':
            currentRepo = a
          if   o == '-g':
            githubUser = a
          if   o == '-d':
            destDirectory = a
          if   o == '-s':
            sinceDate = a
          if   o == '-u':
            untilDate = a
          elif o == '-h':
            Usage()
            sys.exit(0)
    except getopt.GetoptError as e:
        print(str(e))
        Usage()
        sys.exit(2)

    if type(githubToken) != str or len(githubToken) <= 0:
          print("please use -t for github token")
          Usage()
          sys.exit(0)
    if type(githubOwner) != str or len(githubOwner) <= 0:
          print("please use -o for github owner")
          Usage()
          sys.exit(0)
    if type(currentRepo) != str or len(currentRepo) <= 0:
          print("please use -r for repo")
          Usage()
          sys.exit(0)
    if type(githubUser) != str or len(githubUser) <= 0:
          print("please use -g for github user")
          Usage()
          sys.exit(0)      

    query_url = f"https://api.github.com/repos/{githubOwner}/{currentRepo}/commits"
    if sinceDate or untilDate:
        params = {
            "since": sinceDate,
            "until": untilDate,
            "per_page": "100",
            }
    else:
        params = {
                "per_page": "100",
                }      
    headers = {'Authorization': f'token {githubToken}'}
    r = requests.get(query_url, headers=headers, params=params)
    commits = r.json()

    file = sinceDate+'-to-'+untilDate+'-'+githubUser+'-'+currentRepo+'-commits.txt'
          
    # Creating a file at specified location
    with open(os.path.join(destDirectory, file), 'w') as fp:
        count = 0
        for commit in commits:
            name = commit['commit']['author']['name']
            if(name==githubUser):
                d = commit['commit']['committer']['date']
                message = commit['commit']['message']
                sha = commit['sha']
                subdir = "{0}-{1}-{2}-{3}-{4}".format(currentRepo, d, name, sha, message)
                fp.write(subdir)
                fp.write("\n")

                count += 1
                if (count >= 10000):
                    break
        print(str(count) +' commits found')


if __name__ == "__main__":
  main()
