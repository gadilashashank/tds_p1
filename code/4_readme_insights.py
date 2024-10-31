import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt

repos = pd.read_csv("../repositories.csv", header=0)
users = pd.read_csv("../users.csv", header=0)


repos['created_at'] = pd.to_datetime(repos['created_at'], utc=True)
users['created_at'] = pd.to_datetime(users['created_at'], utc=True)

users['ls'] = users['following'] / (1 + users['followers'])

plt.figure(figsize=(8, 6))
users['ls'].plot.kde()
plt.xlabel("Leader Strength")
plt.title("KDE of Leader strength metric")
plt.xlim(0, 10)
plt.savefig("leader_strength_kde.jpg")
plt.clf()

users['ls'].plot.box()
plt.title("Box plot of Leader strength metric")
plt.xlabel("Leader Strength")
plt.savefig("leader_strength_box.jpg")
plt.clf()

df = pd.merge(repos, users, on='login')
df['insight'] = df['created_at_x'] - df['created_at_y']

print(df.groupby("login").insight.min().mean())
print(df.groupby("login").insight.max().mean())