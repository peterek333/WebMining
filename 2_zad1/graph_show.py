import requests
from bs4 import BeautifulSoup
import re
from enum import Enum
import networkx as nx
import matplotlib.pyplot as plt

DEGREE_MAX = 2
LINKS_WITHOUT_HASH = True   #without javascript links like "#profile"

site = 'pduch.kis.p.lodz.pl'
homeUrl = 'http://' + site
internalRegex = '(' + site.replace('.', '\.') + '|^(?!http).*\.html)'
externalRegex = '^http.*'
print(internalRegex)

class LinkType(Enum):
    HOME = 0,
    INTERNAL = 1,
    EXTERNAL = 2,
    ANOTHER = 3

def getColor(linkType):
    linkTypes = {
        LinkType.HOME: 'g',
        LinkType.INTERNAL: 'g',
        LinkType.EXTERNAL: 'r',
        LinkType.ANOTHER: 'b'
    }
    return linkTypes.get(linkType)

class LinkPoint:
    def __init__(self, linkType, degree, edge):
        self.linkType = linkType
        self.degree = degree
        self.edge = edge

def getUniqueLinksFromSite(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')
    links = soup.find_all('a', href=True)
    if LINKS_WITHOUT_HASH:
        return set([link['href'] for link in links if not link['href'].startswith("#") ])
    else:
        return set([link['href'] for link in links])

def isHome(url):
    return url == "index.html" or url == homeUrl

def isExternalLink(url):
    return re.match(externalRegex, url)

def isInternalLink(url):
    return re.match(internalRegex, url)


def buildLinksMap(actualUrl, maxDegree, actualDegree):
    linksMap = []
    if actualDegree < maxDegree:
        uniqueLinks = getUniqueLinksFromSite(actualUrl)
        print("Degree " + str(actualDegree))
        for link in uniqueLinks:
            linkType = LinkType.INTERNAL
            if isHome(link):
                linkType = LinkType.HOME
                print("Home: " + link)
            elif isInternalLink(link):
                print("Internal: " + link)
            elif isExternalLink(link):
                linkType = LinkType.EXTERNAL
                print("External: " + link)
            else:
                linkType = LinkType.ANOTHER
                print("Other: " + link)
            linksMap.append(LinkPoint(linkType, actualDegree, (actualUrl, link)))
            if linkType is LinkType.INTERNAL:
                linksFromDeeperDegree = buildLinksMap(actualUrl + '/' + link, maxDegree, actualDegree + 1)
                linksMap += linksFromDeeperDegree
            # elif linkType == LinkType.EXTERNAL:
        print("\n\n\n")

    return linksMap

s = getUniqueLinksFromSite(homeUrl)
print(s)
linksMap = buildLinksMap(homeUrl, DEGREE_MAX, 0)
for linkPoint in linksMap:
    print(linkPoint.linkType.name + " | " + str(linkPoint.degree) + " | ")
    print(linkPoint.edge)

links = []
edges = []
for linkPoint in linksMap:
    startNode = str(linkPoint.degree) + " " + linkPoint.edge[0]
    nextNode = str(linkPoint.degree + 1) + " " + linkPoint.edge[1]
    links.append(startNode)
    links.append(nextNode)
    edges.append((startNode, nextNode))

colorMap = []
links = set(links)
digraph = nx.DiGraph()
for link in links:
    link = link.split(" ")[1]
    linkType = LinkType.INTERNAL
    if isHome(link):
        linkType = LinkType.HOME
    elif isInternalLink(link):
        linkType = LinkType.INTERNAL
    elif isExternalLink(link):
        linkType = LinkType.EXTERNAL
    else:
        linkType = LinkType.ANOTHER
    print(link + " -> " + str(linkType))
    colorMap.append(getColor(linkType))
    # digraph.add_node(link)

digraph.add_nodes_from(links)
digraph.add_edges_from(edges)
for k, v in zip(links, colorMap):
    print(k, v)
# print(colorMap)
nx.draw(digraph, cmap = plt.get_cmap('jet'), with_labels=True, node_color=colorMap)
# nx.draw(digraph, cmap = plt.get_cmap('jet'), with_labels=True)
plt.show()