import pandas as pd
from scipy.stats import linregress

repos = pd.read_csv("repositories.csv", header=0)
users = pd.read_csv("users.csv", header=0)

# Q1
sorted_users = users.sort_values(by='followers', ascending=False).login.head()
print("1: ", ",".join(sorted_users))

# Q2
sorted_users = users.sort_values(by='created_at', ascending=True).login.head()
print("2: ", ",".join(sorted_users))

# Q3
lc = repos.groupby('license_name').license_name.value_counts().nlargest(3)
print("-"*20)
print(lc)
print("-"*20)
# Q4
print("4: ", users.groupby('company').company.value_counts().idxmax())

# Q5
print("5: ", repos.groupby('language').language.value_counts().idxmax())

# Q6
lg = {}
after_2020 = users[users['created_at'] >= '2021-01-01']
print("6: ", end="")
print(repos[repos['login'].isin(after_2020.login)].language.value_counts().index[1])

# Q7
average_stars_per_language = repos.groupby('language')['stargazers_count'].mean()
highest_average_language = average_stars_per_language.idxmax()
print("7: ", highest_average_language)

# Q8
users['leader_strength'] = users['followers'] / (1 + users['following'])

# Sort by leader_strength in descending order and get the top 5
top_leaders = users.sort_values(by='leader_strength', ascending=False).head(5)

# Get the logins in order and join them as a comma-separated string
top_logins = ', '.join(top_leaders['login'])
print("8: ", top_logins)

# Q9
print("9: ", round(users['followers'].corr(users['public_repos']), 3))

# Q10
result = linregress(users['public_repos'], users['followers'])
print("10: ", round(result.slope, 3))

# Q11
print("11: ", round(repos['has_projects'].corr(repos['has_wiki']), 3))

# Q12
avg_following_hireable = users[users['hireable'] == True]['following'].mean()
avg_following_not_hireable = users[users['hireable'] == False]['following'].mean()
difference = avg_following_hireable - avg_following_not_hireable
print("12: ", round(difference, 3))


# Q13
users['bio_len'] = users['bio'].str.split().str.len()
result = linregress(users['bio_len'], users['followers'])
print("13: ", round(result.slope, 3))

# Q14
repos['created_at_dtime'] = pd.to_datetime(repos['created_at'], utc=True)
weekend_repos = repos[repos['created_at_dtime'].dt.dayofweek >= 5].login.value_counts().index[:5]
print("14: ", ",".join(weekend_repos))
# Q15
hireable_with_email = users[users['hireable'] == 'true']['email'].notna().mean()
not_hireable_with_email = users[users['hireable'] == 'false']['email'].notna().mean()
difference = hireable_with_email - not_hireable_with_email
print("15: ", round(difference, 3))

# Q16
non_missing_names = users['name'].dropna()
surnames = non_missing_names.str.split().str[-1].str.strip()
most_common_surname = surnames.value_counts().head(6)
print("-"*20)
print(most_common_surname)
print("-"*20)