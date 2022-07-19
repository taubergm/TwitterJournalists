import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('all_journos.csv')

print(df['url'])

freq = df['url'].value_counts()
print(freq)

s = df['url'].value_counts()
df = df[df.isin(s.index[s >= 40]).values]

df['url'].value_counts().sort_values().plot(kind = 'barh', figsize=(30, 30))

#plt.rcParams["figure.figsize"] = [200, 200]
#plt.rcParams["figure.figsize"] = (400,400)

plt.yticks(fontsize=20)
plt.xticks(fontsize=30)


#plt.show()
plt.savefig("urls.png")


df = pd.read_csv('all_journos.csv')

print(df['broad_location'])

freq = df['broad_location'].value_counts()
print(freq)

s = df['broad_location'].value_counts()
df = df[df.isin(s.index[s >= 50]).values]

df['broad_location'].value_counts().sort_values().plot(kind = 'barh')

#plt.show()
