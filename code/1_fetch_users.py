from githubkit import GitHub
from githubkit.versions.latest.models import PublicUser, PrivateUser
import json
import csv
import pandas as pd

github = GitHub("<TOKEN>")

def clean_company(company):
   if not company:
      return ''
   return company.strip().lstrip("@").upper()

q = """
query ($cursor:String){
  search(type: USER, query: "location:Dublin followers:>50", first: 100 after:$cursor) {
    pageInfo {
      hasNextPage
      endCursor
    }
    userCount
    nodes {
      ... on User{
        login
        name
        company
        location
        email
        isHireable
        bio
        repositories(ownerAffiliations:OWNER){
          totalCount
        }
        followers {
          totalCount
        }
        following {
          totalCount
        }
        createdAt

      }
    }
  }
}
"""

header = ['login', 'name', 'company', 'location', 'email', 'is_hireable', 'bio', 'public_repos', 'followers', 'following', 'created_at']
for result in github.graphql.paginate(q):
  rows = []
  for user in result['search']['nodes']:
      user['followers'] = 0 if not user.get('followers') else user['followers']['totalCount']
      user['following'] = 0 if not user.get('following') else user['following']['totalCount']
      user['bio'] = '' if not user.get("bio") else repr(user['bio'])
      user['repositories'] = 0 if not user.get("repositories") else user['repositories']['totalCount']
      user['company'] = clean_company(user.get("company"))

      for k, v in user.items():
        if type(v) == str and not v:
          user[k] = pd.NA
        if type(v) == bool:
           user[k] = str(v).lower()
      rows.append(user.values())
  
  df = pd.DataFrame(rows)
  df.columns = header
  df.to_csv("users.csv", mode="a", na_rep="''", index=False)




