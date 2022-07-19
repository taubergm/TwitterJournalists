import sqlite3
import csv
import networkx as nx
import pandas as pd
from itertools import count


# Create a SQL connection to our SQLite database
con = sqlite3.connect("./following_clean_b.db")

cur = con.cursor()

writers = set()
G = nx.Graph()
# custom dict
names = {}
scores = []


LIMIT = 500
processed = 0
for row in cur.execute('select * from following'):
    processed = processed + 1
    writer = row[1]
    twitter_name = row[2]
    num_followers = row[3]
    location = row[10]
    polarity = row[11]
    num_journo_followers = row[12]
    writers.add(twitter_name)
    names[twitter_name] = writer
    score = int(num_journo_followers) * (1 + int(num_followers)/6000000)
    scores.append(score)
    
    G.add_node(twitter_name, num_followers=num_followers, polarity=polarity, num_journo_followers=num_journo_followers, real_name=writer, location=location)


    if processed > LIMIT:
        break
    
processed = 0
for row in cur.execute('SELECT * FROM Following;'):
    processed = processed + 1
    twitter_name = row[2]
    following = row[9].split(':')

    for user in following:
        if (user in writers):
            print(processed)
            #print("{} - {} - {} - {}".format(writer, location, twitter_name, user))
            G.add_edge(twitter_name, user)

    if processed > LIMIT:
        break

con.close()


'''
cliques = list(nx.find_cliques(G))
i = 0
for c in cliques:
    print("cliques")
    print("--------")

    print(c)
    print(type(c))
    with open('cliques_{}_{}.txt'.format(LIMIT, i), 'w') as f:
        for item in c:
            f.write(item)
            f.write('\n')

    i = i + 1



from networkx.algorithms.community import k_clique_communities
communities = list(k_clique_communities(G, 2))
i = 0
for c in communities:
    print("comminity")
    print("--------")

    print(c)
    print(type(c))
    with open('kclique_{}_{}.txt'.format(LIMIT, i), 'w') as f:
        for item in c:
            f.write(item)
            f.write('\n')

    i = i + 1
'''


import networkx.algorithms.community as nx_comm
communities = nx_comm.louvain_communities(G, seed=2311)


i = 0
for c in communities:
    print("comminity")
    print("--------")

    if len(c) < 6:
        continue

    print(c)
    print(type(c))
    with open('louvain_{}_{}.txt'.format(LIMIT, i), 'w') as f:
        for item in c:
            f.write(item)
            f.write('\n')

    i = i + 1

    #for node in c:
    #    print(G.nodes[node])
    #    user = G.nodes[node]['real_name']
    #    print(user)


'''
from networkx.algorithms.community.centrality import girvan_newman
communities = girvan_newman(G)
i = 0
for c in communities:
    print("comminity")
    print("--------")

    if len(c) < 6:
        continue

    print(c)
    print(type(c))
    with open('girvan_{}_{}.txt'.format(LIMIT, i), 'w') as f:
        for item in c:
            f.write(item)
            f.write('\n')

    i = i + 1
'''
