import sqlite3
import csv
import networkx as nx
import pandas as pd
from itertools import count


# Create a SQL connection to our SQLite database
con = sqlite3.connect("./following_clean_b.db") # edges
#con = sqlite3.connect("./following_clean_copy.db") # followers


cur = con.cursor()

writers = set()
G = nx.Graph()
# custom dict
names = {}
scores = []


LIMIT = 75
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
    writer = row[1]
    twitter_name = row[2]
    num_followers = row[3]
    location = row[10]    
    polarity = row[11]
    num_journo_followers = row[12]

    following = row[9].split(':')

    for user in following:
        if (user in writers):
            print("{} - {} - {} - {}".format(writer, location, twitter_name, user))
            G.add_edge(twitter_name, user)

    if processed > LIMIT:
        break

con.close()


import matplotlib.pyplot as plt
from matplotlib import pylab


def save_graph(G,file_name):
    #initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    FOLLOWERS_LABEL = 100000

    labels = {}    
    for node in G.nodes():
        print(node)
    
        if node == 'twitter_name':
            continue

        if int(G.nodes[node]['num_followers']) >  FOLLOWERS_LABEL:
            labels[node] = G.nodes[node]['real_name']

    pos = nx.nx_pydot.graphviz_layout(G)
    d = dict(G.degree)

    groups = set(nx.get_node_attributes(G,'polarity').values())
    mapping = dict(zip(sorted(groups),count()))
    nodes = G.nodes()
    colors = [mapping[G.nodes[n]['polarity']] for n in nodes]
    
    # top 100
    nc = nx.draw(G, pos, alpha=0.5, node_size=[v * 13 for v in d.values()], width=0.001, font_size=12, 
            font_weight='bold', labels=names, node_color=colors, with_labels = True, cmap=plt.cm.jet, edge_color='#FFDEA2')


    # top 500
    #nc = nx.draw(G, pos, alpha=0.5, node_size=[v * 0.3 for v in d.values()], edgelist=[], width=0.001, font_size=3.5, 
    #    font_weight='bold', node_color=colors, labels=names, cmap=plt.cm.jet)

    # top 1000
    #nc = nx.draw(G, pos, alpha=0.5, node_size=[v * 0.02 for v in scores], edgelist=[], width=0.001, font_size=3, 
    #    font_weight='bold', node_color=colors, labels=names, cmap=plt.cm.jet)


    
    # fix colors later - https://stackoverflow.com/questions/14777066/matplotlib-discrete-colorbar
    # maybe draw nodes and edges seperately?
    
    # node size based on followers - use with_labels = fasle if needed
    #for node, (x, y) in pos.items():
    #    plt.text(x, y, node, fontsize=int(G.nodes[node]['num_journo_followers'])/500, ha='center', va='center')


    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    #plt.xlim(0, xmax)
    #plt.ylim(0, ymax)

    plt.savefig(file_name,bbox_inches="tight")
    pylab.close()
    del fig


#print(list(nx.isolates(G)))
#print("MT")
#remove = [node for node, degree in G.degree() if degree < 15]
#print(remove)
#G.remove_nodes_from(remove)
#G.remove_nodes_from(list(nx.isolates(G)))


save_graph(G,"t100b.pdf")
import sys
sys.exit()


pos = nx.spring_layout(G, k=0.1)
plt.rcParams.update({'figure.figsize': (15, 10)})

'''
nx.draw_networkx(
        G,
        pos=pos,
        node_size=0,
        edge_color="#444444",
        alpha=0.05,
        with_labels=False)

plt.savefig('full.pdf',bbox_inches="tight")
'''

#import networkx.algorithms.community as nxcom
#communities = sorted(nxcom.greedy_modularity_communities(G), key=len, reverse=True)

import networkx.algorithms.community as nx_comm
communities = nx_comm.louvain_communities(G, seed=2311)
print(len(communities))

i = 0
for c in communities:
    print("comminity")
    print("--------")

    if len(c) < 6:
        continue

    print(c)
    print(type(c))
    with open('comm_{}_{}.txt'.format(LIMIT, i), 'w') as f:
        for item in c:
            f.write(item)
            f.write('\n')

    i = i + 1




def set_node_community(G, communities):
    '''Add community to node attributes'''
    for c, v_c in enumerate(communities):
        for v in v_c:
            # Add 1 to save 0 for external edges
            G.nodes[v]['community'] = c + 1
            print('community')
            print(c+1)
    
def set_edge_community(G):
    '''Find internal edges and add their community to their attributes'''
    for v, w, in G.edges:
        if G.nodes[v]['community'] == G.nodes[w]['community']:
            # Internal edge, mark with community
            G.edges[v, w]['community'] = G.nodes[v]['community']
        else:
            # External edge, mark as 0
            G.edges[v, w]['community'] = 0
    
def get_color(i, r_off=1, g_off=1, b_off=1):
    '''Assign a color to a vertex.'''
    r0, g0, b0 = 0, 0, 0
    n = 16
    low, high = 0.1, 0.9
    span = high - low
    r = low + span * (((i + r_off) * 3) % n) / (n - 1)
    g = low + span * (((i + g_off) * 5) % n) / (n - 1)
    b = low + span * (((i + b_off) * 7) % n) / (n - 1)
    return (r, g, b)


def get_color(i, r_off=1, g_off=1, b_off=1):
    '''Assign a color to a vertex.'''
    if i == 0:
        (r,g,b) = (1,1,1) #  white
    elif i == 1:
        (r,g,b) = (1,0.6,1)    #pink
    elif i == 2:
        (r,g,b) = (0,0.4,0.1) #  green
    elif i == 3:
        (r,g,b) = (0,1,0.9) #  light blue
    elif i == 4:
        (r,g,b) = (0.4,0,0.7) #  purple
    elif i == 5:
        (r,g,b) = (1,0.6,1)    #pink
    elif i == 6:
        (r,g,b) = (0.9,0.1,0) #  red
    elif i == 7:
        (r,g,b) = (0.9,0.5,0) #  orange
    elif i == 8:
        (r,g,b) = (1,1,1) #  black

    return (r, g, b)




plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams.update({'figure.figsize': (15, 10)})
plt.style.use('dark_background')
    # Set node and edge communities
set_node_community(G, communities)
set_edge_community(G)
    # Set community color for internal edges
external = [(v, w) for v, w in G.edges if G.edges[v, w]['community'] == 0]
internal = [(v, w) for v, w in G.edges if G.edges[v, w]['community'] > 0]
internal_color = ["black" for e in internal]
node_color = [get_color(G.nodes[v]['community']) for v in G.nodes]


print("node_color")
print("----------")
print(get_color(0))
print(get_color(1))
print(get_color(2))
print(get_color(3))
print(get_color(4))
print(get_color(5))
print(get_color(6))
print(get_color(7))
print("---------")
    # external edges
nx.draw_networkx(
        G,
        pos=pos,
        node_size=0,
        edgelist=external,
        edge_color="silver",
        node_color=node_color,
        alpha=0.2,
        with_labels=False)
    # internal edges
nx.draw_networkx(
        G, pos=pos,
        edgelist=internal,
        edge_color=internal_color,
        node_color=node_color,
        alpha=0.05,
        with_labels=False)

plt.show()
plt.savefig('comms.pdf',bbox_inches="tight")
plt.show()


