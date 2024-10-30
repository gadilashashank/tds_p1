from githubkit import GitHub
from githubkit.versions.latest.models import PublicUser, PrivateUser
import json
import csv

github = GitHub("<token>")

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
        location
        company
        location
        email
        isHireable
        bio
        repositories{
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

header = ['login', 'name', 'company', 'location', 'email', 'isHireable', 'bio', 'repositories', 'followers', 'following', 'createdAt']
with open("users.csv", "a") as file:
  writer = csv.DictWriter(file, fieldnames=header)
  writer.writeheader()  # Write the header        

  for result in github.graphql.paginate(q):
      rows = []
      for user in result['search']['nodes']:
          user['followers'] = 0 if not user.get('followers') else user['followers']['totalCount']
          user['following'] = 0 if not user.get('following') else user['following']['totalCount']
          user['bio'] = "" if not user.get("bio") else repr(user['bio'])
          user['repositories'] = 0 if not user.get("repositories") else user['repositories']['totalCount']
          rows.append(user)
      
      writer.writerows(rows)
