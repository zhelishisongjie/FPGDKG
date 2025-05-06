import networkx as nx
import sys
import io

def graph_sort(G,fplist):
    if not nx.is_connected(G):
        # print("Warning: The graph is not connected. Using the largest connected component.")
        largest_cc = max(nx.connected_components(G), key=len)  # 获取最大连通子图
        G= G.subgraph(largest_cc).copy()
    fplist_new = []
    # 重新映射节点索引为连续整数
    original_index_map = {node: i for i, node in enumerate(G.nodes())}
    reverse_index_map = {i: node for node, i in original_index_map.items()}  # 反向映射
    for fp in fplist:
        fplist_new.append(original_index_map[fp])
    G = nx.relabel_nodes(G ,original_index_map)

    # index_map = {}
    # index = 0
    # for node in G.nodes():
    #     index_map[str(node)] = index
    #     index += 1
    # print("index_map {'351': 0 , '3303': 1 , '3302': 2 , '3309': 3}")
    #
    #
    #
    # mapping = {node: i for i, node in enumerate( G. nodes())}
    # G = nx. relabel_nodes( G, mapping)

    # print(G.nodes)
    # print(f" length: {len(G.nodes())}  last node:{ G.nodes[len(G.nodes())-1] }".encode('utf-8', 'ignore').decode('utf-8'))

    return G , reverse_index_map,fplist_new
# def graph_sort(G):
#     index_map = {}
#     index = 0
#     for node in G.nodes():
#         index_map[str(node)] = index
#         index += 1
#     print("index_map {'351': 0 , '3303': 1 , '3302': 2 , '3309': 3}")
#
#
#
#     mapping = {node: i for i, node in enumerate( G. nodes())}
#     G = nx. relabel_nodes( G, mapping)
#
#     # print(G.nodes)
#     print(f" lenth: {len(G.nodes())}  last node:{ G.nodes[len(G.nodes())-1] }".encode('utf-8', 'ignore').decode('utf-8'))
#
#     return G , index_map


