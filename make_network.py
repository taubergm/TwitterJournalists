import csv
import time
import sys
import re
import subprocess
import networkx as nx
import matplotlib.pyplot as plt

csv.field_size_limit(sys.maxsize)



#infile = "writers_plus_twitter_network_final.csv"
infile = "journalists_2019.csv"
writer_data = open(infile)
csv_reader = csv.reader(writer_data)
writers = set()
for row in csv_reader:
    twitter_name = row[1]
    num_followers = row[2]

    if (row[0] == "writer"):
        continue

    if (int(num_followers) < 300):
        continue

    writers.add(twitter_name)

G = nx.Graph()


infile = "journalists_2019.csv"
writer_data = open(infile)
node_color = []
polarities = []
csv_reader = csv.reader(writer_data)
next(csv_reader) # skip header


# AVG number of edges per node? = avg number of journalists they follow

for row in csv_reader:
    writer = row[0]
    twitter_name = row[1]
    num_followers = row[2]
    num_articles = row[3]
    gender = row[4]
    last_url = row[5]
    following = row[6].split(':')

    num_following = len(following)
  
    if (writer == "writer"):
        continue

    #print writer, twitter_name, num_followers, num_articles

    if (int(num_followers) < 300):
        continue

    try:
        polarity = int(row[7])
        print(polarity)
        #polarities.append(polarity)
    except:
        polarity = -99

    num_following = len(following)

    
    if polarity == '-2':
        node_color.append('#00008B') # dark blue
    elif polarity == '-1':
        node_color.append('#ADD8E6') # light blue
    elif polarity == '0':
        node_color.append("#D3D3D3") # grey
    elif polarity == '1':
        node_color.append("#ffcccb") # light red
    else:
        node_color.append("#8B0000") # dark red


    G.add_node(twitter_name, polarity=polarity, name=writer)
    polarities.append(polarity)
    for user in following:
        if (user in writers):
            #print "%s - %s - %s - %s" % (writer, num_following, twitter_name, user)
            G.add_edge(twitter_name, user)


writer_degrees =  dict(G.degree)
fieldnames = ['writer', 'degrees', 'polarity']
#print writer_degrees

with open('mycsvfile.csv', 'w') as f:  
    w = csv.DictWriter(f, writer_degrees.keys())
    w.writeheader()
    w.writerow(writer_degrees)



#to get degrees 
for key, value in writer_degrees.items():
    print(key + ',' + str(value))



deg_cen = nx.degree_centrality(G)
print "degree centrality"
print deg_cen


largest = max(nx.strongly_connected_components(G), key=len)
print(largest)

#nx.draw_networkx_nodes(graph = G, pos = pos, node_list = graph.nodes(), node_color = ['r','b'], alpha = 0.8, node_size = [counts['edges'][s] for s in G.nodes()])
#plt.savefig("./map_0.png", format = "png", dpi = 300)
#plt.show()

#nx.draw(G, with_labels=False, node_size=25, node_color=node_color)
#plt.savefig("./map_2019.png", format = "png", dpi = 300)
#plt.show()

from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.transform import linear_cmap

colors = ["#00008B", "#ADD8E6", "#D3D3D3", "#ffcccb", "#8B0000"]

fill_color=linear_cmap(field_name='polarity', palette=colors, low=-2, high=2)


# Show with Bokeh
plot = figure(title="Graph Layout Demonstration", x_range=(-1.1,1.1), y_range=(-1.1,1.1),
              tools="", toolbar_location=None)



network_graph = from_networkx(G, nx.spring_layout, scale=10, center=(0, 0))
network_graph.node_renderer.glyph = Circle(size=15, fill_color=fill_color)
network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)

# add name to node data
network_graph.node_renderer.data_source.data['polarity'] = polarities
# add name, media name attributes too
#network_graph.node_renderer.data_source.data['name'] = names


plot.renderers.append(network_graph)
show(plot)


#betweeness_centrality = nx.betweenness_centrality(G)
#fieldnames = ['writer', 'betweeness_centrality']
#with open('betweeness_centrality.csv', 'wb') as f:  
#    w = csv.DictWriter(f, betweeness_centrality.keys())
#    w.writeheader()
#    w.writerow(betweeness_centrality)


#eigenvector_centrality = nx.eigenvector_centrality(G)
#fieldnames = ['writer', 'eigenvector_centrality']
#with open('eigenvector_centrality.csv', 'wb') as f:  
#    w = csv.DictWriter(f, eigenvector_centrality.keys())
#    w.writeheader()
#    w.writerow(eigenvector_centrality)

#closeness_centrality = nx.closeness_centrality(G)
#fieldnames = ['writer', 'closeness_centrality']
#with open('eigenvector_centrality.csv', 'wb') as f:  
#    w = csv.DictWriter(f, closeness_centrality.keys())
#    w.writeheader()
#    w.writerow(closeness_centrality)


