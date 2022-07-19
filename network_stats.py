import sqlite3
import csv
import networkx as nx
import pandas as pd
from itertools import count
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.pylab import plot

# Create a SQL connection to our SQLite database
con = sqlite3.connect("./following_clean_b.db")

cur = con.cursor()

writers = set()
G = nx.Graph()
#G = nx.DiGraph()
# custom dict
names = {}
scores = []


def map_polarity(pol):
    if pol == 'NA':
        return 0
    else:
        return int(pol)


LIMIT = 20000
processed = 0
for row in cur.execute('select * from following'):
    processed = processed + 1
    writer = row[1]
    twitter_name = row[2]
    num_followers = row[3]
    location = row[10]
    polarity = map_polarity(row[11])
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
    num_journo_followers = row[12]

    following = row[9].split(':')

    for user in following:
        if (user in writers):
            print("{} - {} - {} - {}".format(writer, location, twitter_name, user))
            G.add_edge(twitter_name, user)

    if processed > LIMIT:
        break

con.close()



def plot_degree_dist(G):
    degrees = [G.degree(n) for n in G.nodes()]
    plt.hist(degrees, bins=100)
    plt.title('Degree Distribution' )
    plt.xlabel('Degree')
    plt.ylabel('#Nodes')
    plt.show()

def AnalyzeGraphs(g1):
    
    """#Compares the quantitative properties of two graph. So I can check the coarse graining. """

    
    #Nodes and edges
    print('Graph1: #(Nodes, Edges) = (' + str(len(g1.nodes())) + ', ' + str(len(g1.edges())) + ')')

    #Connected Components
    
    plt.hist([len(i) for i in nx.connected_components(g1)])
    plt.title('Cluster Size')
    plt.xlabel('Cluster Size')
    plt.ylabel('#Cluster')
    plt.show()
    
    #Degree Distribution
    print(nx.degree_histogram(g1))
    plt.hist(nx.degree_histogram(g1), bins=80)
    plt.xticks(range(80), rotation=90)  # Set text labels and properties.
    plt.title('Degree Distribution' )
    plt.xlabel('Degree')
    plt.ylabel('#Nodes')
    plt.show()
    
    #Betweeness --- this is by far the most compuationally demanding.
    #plt.hist(nx.betweenness_centrality(g1, normalized = False).values(), bins=100))
    #plt.title('Distribution of Betweenness' )
    #plt.xlabel('Betweenness')
    #plt.ylabel('#Nodes')
    #plt.show()
       
def get_avg_clustering(G):
    return nx.average_clustering(G, trials=2000)


def get_transitivity(G):
    return nx.transitivity(G)


def get_correlation_coeff(G):
    r = nx.degree_pearson_correlation_coefficient(G)
    return r

def get_avg_shortest_path(G):
    l = nx.average_shortest_path_length(G)
    return l

def get_center_list(G):
    return list(nx.center(G))

def get_graph_radius(G):
    return nx.radius(G) 

def get_graph_diameter(G):
    return nx.diameter(G) 

def avg_redundancy(G):
    from networkx.algorithms import bipartite
    rc = bipartite.node_redundancy(G)
    return (sum(rc.values()) / len(G))

def get_average_betweeness(G):
    bet_centrality_dict = nx.betweenness_centrality(G, normalized = True, 
                                              endpoints = False)
    filtered_vals = [v for _, v in bet_centrality_dict.items()]
    average = sum(filtered_vals) / len(filtered_vals)
    return average

def get_average_trophic(G):
    return nx.trophic_incoherence_parameter(G)

def get_flow_hierarchy(G):
    return nx.flow_hierarchy(G) 


def get_small_world(G):
    sigma = nx.sigma(G)
    omega = nx.omega(G)

    return(sigma, omega)



####  cliques - slow compute
def get_cliques1(G):
    #return nx.enumerate_all_cliques(G)
    cliques = nx.find_cliques(g)
    cliques40 = [clq for clq in cliques if len(clq) >= 40]
    nodes = set(n for clq in cliques4 for n in clq)
    h = g.subgraph(nodes)
    deg = nx.degree(h)
    nodes = [n for n in nodes if deg[n] >= 4]
    k = h.subgraph(nodes)

def find_cliques(G):
    return list(nx.find_cliques(G)) 


print('nodes')
print('------')
print(G.number_of_nodes())
print()
print('edges')
print('------')
print(G.number_of_edges())
print()
print('density')
print('------')
print(nx.density(G))
print()
print('mean degree')
print('-----------')
print(1 * (G.number_of_edges()/G.number_of_nodes())) # 2* for undirected
print()
print('num components')
print('---------')
#print(nx.number_connected_components(G))
print()
print('mean shortest path')
print('-----------')
#print(get_avg_shortest_path(G))
print()



print("power law alpha")
import powerlaw
import collections
degree_sequence = sorted([d for n, d in G.degree()], reverse=False) # used for degree distribution and powerlaw test

# the wrong way to calculate alpha - loses histogram bins
#counter=collections.Counter(degree_sequence) # get histogram from list
#print(counter)
#print(counter.values())
#vals = sorted(list(counter.values()))
#print(vals)
#fit2 = powerlaw.Fit(vals)
#print("alpha")
#print(fit2.power_law.alpha)
#print(fit2.power_law.xmin)


# the right way using CDFs and bins 
count, bins_count = np.histogram(degree_sequence, bins=50)
print(count)
print(bins_count)
pdf = count / sum(count)
cdf = np.cumsum(pdf)
print(pdf)
fit3 = powerlaw.Fit(pdf)
print("alpha")
print(fit3.power_law.alpha) # alpha is one more for CDF
print(fit3.power_law.xmin)
# plotting PDF and CDF
#plt.plot(bins_count[1:], pdf, color="red", label="PDF")
#plt.plot(bins_count[1:], cdf, label="CDF")
#plt.legend()
#plt.show()

# fit powerlaw random variates with scipy.stats
import scipy.stats as sps
fit_simulated_data = sps.powerlaw.fit(pdf, loc=0, scale=1)
print('alpha:', fit_simulated_data[0])



print("clustering")
print('---------')
print('avg cluster C2')
print('-----------')
#print(get_avg_clustering(G))
print()
print('transitivity (triangles) C1')
print('-------------')
#print(get_transitivity(G))
print()
print("correlation_coefficient")
print('----------------')
#print(get_correlation_coeff(G))
print()


print("radius")
print('---------')
#print(get_graph_radius(G))
print()


print("diameter")
print('---------')
#print(get_graph_diameter(G))
print()



print("average_neighbor_degree")
print('---------')
#print(nx.average_neighbor_degree(G))
print()


print("average betweenness")
print('---------')
#print(get_average_betweeness(G))
print()


print("coherenece")
print('---------')
#print(get_average_trophic(G))
print()

#print("find_cliques")
#print('---------')
#print(find_cliques(G))
#print()



#print("center")
#print('---------')
#print(get_center_list(G))
#print()


#print("get_small_world")
#print('---------')
#(sigma, omega) = get_small_world(G)
#print(sigma, omega)


# associativity based on polarity
#print("polarity associativity")
#print(nx.numeric_assortativity_coefficient(G, "polarity"))

def plot_stats(G):
    # degre histogram
    degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
    dmax = max(degree_sequence)

    fig = plt.figure("Degree of a random graph", figsize=(8, 8))
    # Create a gridspec for adding subplots of different sizes
    axgrid = fig.add_gridspec(5, 4)

    ax0 = fig.add_subplot(axgrid[0:3, :])
    Gcc = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
    pos = nx.spring_layout(Gcc, seed=10396953)
    nx.draw_networkx_nodes(Gcc, pos, ax=ax0, node_size=20)
    nx.draw_networkx_edges(Gcc, pos, ax=ax0, alpha=0.4)
    ax0.set_title("Connected components of G")
    ax0.set_axis_off()

    ax1 = fig.add_subplot(axgrid[3:, :2])
    ax1.plot(degree_sequence, "b-", marker="o")
    ax1.set_title("Degree Rank Plot")
    ax1.set_ylabel("Degree")
    ax1.set_xlabel("Rank")

    ax2 = fig.add_subplot(axgrid[3:, 2:])
    ax2.bar(*np.unique(degree_sequence, return_counts=True))
    ax2.set_title("Degree histogram")
    ax2.set_xlabel("Degree")
    ax2.set_ylabel("# of Nodes")

    fig.tight_layout()
    plt.show()


#plot_stats(G)

#Fun Neighbors
a = nx.common_neighbors(G, 'maddow', 'TuckerCarlson')
print(len(sorted(a)))
b = nx.common_neighbors(G, 'maddow', 'andersoncooper')
print(len(sorted(b)))
c = nx.common_neighbors(G, 'andersoncooper', 'TuckerCarlson')
print(len(sorted(c)))
d = nx.common_neighbors(G, 'ezraklein', 'seanhannity')
print(len(sorted(d)))
e = nx.common_neighbors(G, 'ezraklein', 'dbongino')
print(len(sorted(e)))


# plot leaders of each community
