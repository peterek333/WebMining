import networkx as nx
import matplotlib.pyplot as plt

def page_rank(pages, d_f = 0.85):
    pages_size = len(pages)
    # links_per_page_values = []
    # for page, links in pages.items():
    #     page_links_size = len(links)


    for page, links in pages.items():
        page_links_size = len(links)
        links_per_pages_value = 0
        for other_page, other_links in {i:pages[i] for i in pages if i != page}.items():
            links_per_pages_value += (1.0 / len(other_links))
        page_rank_for_site = (1 - d_f) / pages_size + d_f * links_per_pages_value

        print(page_rank_for_site)



pages = {
    "A.pl": ["B.com", "D.org"],
    "B.com": ["A.pl"],
    "C.net": ["B.com", "A.pl"],
    "D.org": ["C.net"],
}

# page_rank(pages)
digraph = nx.DiGraph()
digraph.add_nodes_from(pages.keys())
for page, links in pages.items():
    for link in links:
        digraph.add_edge(page, link)

pr = nx.pagerank(digraph)
print(pr)
# nx.draw(digraph, cmap = plt.get_cmap('jet'), with_labels=True)
# plt.show()
