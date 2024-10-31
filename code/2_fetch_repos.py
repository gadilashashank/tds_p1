from githubkit import GitHub
from githubkit.versions.latest.models import PublicUser, PrivateUser
import csv
import json
import pandas as pd
github = GitHub("<TOKEN>")

q = """
query ($cursor:String){
  user(login: "[]") {
    repositories(first: 100 ownerAffiliations:OWNER  after: $cursor orderBy:{field: PUSHED_AT, direction:DESC}) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes{
        owner {
          ... {
            login
          }
        }
        nameWithOwner
        createdAt
        stargazerCount
        watchers(first:1){...{totalCount}}
        primaryLanguage{...{name}}
        hasProjectsEnabled
        hasWikiEnabled
        licenseInfo{...{key}}
      }
    }
  }
}
"""

header = ['login', 'full_name', 'created_at', 'stargazers_count', 'watchers_count', 'language', 'has_projects', 'has_wiki', 'license_name']
with open("users.csv", mode='r') as file:
    reader = csv.reader(file)
    # Iterate through the rows
    for row in reader:
        login = row[0]
        if not login or login == "login" or login == "0" or login==0:
            continue

        query = q.replace("[]", login)
        repos = []
        counter = 0
        for result in github.graphql.paginate(query):
            if counter == 500:
                break
            for repo in result['user']['repositories']['nodes']:
                print(json.dumps(repo))
                repo['owner'] = repo['owner']['login']
                repo['watchers'] = 0 if not repo.get("watchers") else repo['watchers']['totalCount']
                repo['primaryLanguage'] = pd.NA if not repo.get("primaryLanguage") else repo['primaryLanguage']['name']
                repo['licenseInfo'] = pd.NA if not repo.get("licenseInfo") else repo['licenseInfo']['key']
                
                for k, v in repo.items():
                  if type(v) == str and not v:
                    repo[k] = pd.NA
                  if type(v) == bool:
                    repo[k] = str(v).lower()
                    
                repos.append(repo.values())
                counter += 1
        df = pd.DataFrame(repos)
        if not df.empty:
          df.columns = header
        df.to_csv("repositories.csv", mode="a", na_rep="''", index=False, header=False)

