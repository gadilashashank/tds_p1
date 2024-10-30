from githubkit import GitHub
from githubkit.versions.latest.models import PublicUser, PrivateUser
import csv
import json
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

header = ['owner', 'nameWithOwner', 'createdAt', 'stargazerCount', 'watchers', 'primaryLanguage', 'hasProjectsEnabled', 'hasWikiEnabled', 'licenseInfo']
with open("repositories.csv", "a") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=header)
    writer.writeheader()

    with open("users.csv", mode='r') as file:
        reader = csv.reader(file)
        # Iterate through the rows
        for row in reader:
            login = row[0]
            if not login or login == "login":
                continue

            query = q.replace("[]", login)
            repos = []
            counter = 0
            for result in github.graphql.paginate(query):
                if counter == 500:
                    break
                for repo in result['user']['repositories']['nodes']:
                    repo['owner'] = repo['owner']['login']
                    repo['watchers'] = 0 if not repo.get("watchers") else repo['watchers']['totalCount']
                    repo['primaryLanguage'] = "" if not repo.get("primaryLanguage") else repo['primaryLanguage']['name']
                    repo['licenseInfo'] = "" if not repo.get("licenseInfo") else repo['licenseInfo']['key']
                    
                    print(json.dumps(repo))
                    repos.append(repo)
                    counter += 1
            
            writer.writerows(repos)
