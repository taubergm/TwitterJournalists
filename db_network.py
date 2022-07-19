import sqlite3
import csv
import networkx as nx
import pandas as pd


# Create a SQL connection to our SQLite database
con = sqlite3.connect("following_final.sqlite")

cur = con.cursor()

writers = set()
G = nx.Graph()
journo_followers = {}
names = {}
followers = {}
locations = {}
urls = {}


for row in cur.execute('SELECT * FROM Following;'):
    writer = row[1]
    twitter_name = row[2]
    num_followers = row[3]
    gender = row[4]
    url = row[5]
    location = row[6]
    num_following = row[7]
    writers.add(twitter_name)
    #print(twitter_name)

    journo_followers[twitter_name] = 0
    names[twitter_name] = writer
    followers[twitter_name] = num_followers
    locations[twitter_name] = location
    urls[twitter_name] = url

    G.add_node(twitter_name, real_name=writer)
    

for row in cur.execute('SELECT * FROM Following;'):
    writer = row[1]
    twitter_name = row[2]
    num_followers = row[3]
    gender = row[4]
    url = row[5]
    location = row[6]
    num_following = row[7]
    following = row[8].split(':')

    #print(twitter_name)

    for user in following:
        if (user in writers):
            #print "%s - %s - %s - %s" % (writer, num_following, twitter_name, user)
            G.add_edge(twitter_name, user)
            journo_followers[user] = journo_followers[user] + 1


# Be sure to close the connection
con.close()


# USER EDGES AS REAL MEASURE - degrees is fauly since it counts your own following - eg 
# @funder follows 89k people 
degrees =  dict(G.degree)

journo_followers = pd.DataFrame.from_dict(dict(journo_followers), orient='index').reset_index()
journo_followers.columns = ['user', 'journo_followers']

names = pd.DataFrame.from_dict(dict(names), orient='index').reset_index()
names.columns = ['user', 'name']
followers = pd.DataFrame.from_dict(dict(followers), orient='index').reset_index()
followers.columns = ['user', 'num_followers']
locations = pd.DataFrame.from_dict(dict(locations), orient='index').reset_index()
locations.columns = ['user', 'location']
urls = pd.DataFrame.from_dict(dict(urls), orient='index').reset_index()
urls.columns = ['user', 'url']

prs = nx.pagerank(G, alpha=0.9)
prs = pd.DataFrame.from_dict(dict(prs), orient='index').reset_index()
prs.columns = ['user', 'page_rank']


#betweenness = nx.betweenness_centrality(G)
#betweenness = pd.DataFrame.from_dict(dict(betweenness), orient='index').reset_index()
#betweenness.columns = ['user', 'betweenness']

#closeness = nx.closeness_centrality(G)
#closeness = pd.DataFrame.from_dict(dict(closeness), orient='index').reset_index()
#closeness.columns = ['user', 'closeness']


df = pd.DataFrame.from_dict(dict(G.degree()), orient='index').reset_index()
#df = pd.DataFrame.from_dict(dict(journo_followers), orient='index').reset_index()

df.columns = ['user', 'degrees']
print(df)
df = df.sort_values(by=['degrees'])

df = df.merge(journo_followers, left_on='user', right_on='user')
df = df.merge(names, left_on='user', right_on='user')
df = df.merge(followers, left_on='user', right_on='user')
df = df.merge(locations, left_on='user', right_on='user')
df = df.merge(urls, left_on='user', right_on='user')
df = df.merge(prs, left_on='user', right_on='user')
#df = df.merge(betweenness, left_on='user', right_on='user')
#df = df.merge(closeness, left_on='user', right_on='user')


# normalize out of 100

# remove noninteger rows
df = df[pd.to_numeric(df['num_followers'], errors='coerce').notnull()]
df = df[pd.to_numeric(df['journo_followers'], errors='coerce').notnull()]


df['score'] = df['journo_followers'].astype(int) * (1 + df['num_followers'].astype(int)/3000000) 
#* df['prs'].astype(int) * 1   # add NYT multiplier soon

print(df)
df.to_csv('journo_followers6.csv')



# this is cool - find the communities
# eg sports journos, Right wing, some left, canadians, brits, NYT/CNN etc
import networkx.algorithms.community as nx_comm
communities = nx_comm.louvain_communities(G, seed=123)

#import pandas as pd
#df = pd.read_csv('combined_journos_2022b.csv')

for c in communities:
    
    #print("comminity")
    print("--------")

    if len(c) > 6:
        continue

    for node in c:
        print(G.nodes[node])
        user = G.nodes[node]['real_name']
        print(user)
        
        #user_row = df[df['writer'] == user]
        #if len(user_row) > 1:
        #    continue
        
        #followers = df[df['writer'] == user]['num_followers'].item()
        #print(followers)

        #if followers < 1000:
        #    print("DROPPING")
        #    df.drop(df[df['writer'] == user].index, inplace=True)


#df.to_csv('combined_journos_2022c.csv')
        


    #print("\n")







#largest = max(nx.strongly_connected_components(G), key=len)
#print(largest)


#from networkx.algorithms.community import k_clique_communities
#communities = list(k_clique_communities(G, 5))
#print(communities)

#to get degrees 
#for key, value in writer_degrees.items():
#    print(key + ',' + str(value))


#deg_cen = nx.degree_centrality(G)
#print("degree centrality")
#print(deg_cen)



