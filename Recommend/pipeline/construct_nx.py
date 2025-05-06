import networkx as nx
import json
def construct_nx():
    #with open('/recommend/pipeline/all.json', encoding='utf-8-sig') as f:
    #with open('E:/other/code/fpgkb for Springboot/src/main/resources/recommend/pipeline/all.json', encoding='utf-8-sig') as f:
    #with open('C:/Users/15085/Desktop/Backup_2024.08.16/projects/05-FPGDKG/codes/fpgkb_website/fpgkb for Springboot/src/main/resources/recommend/pipeline/all.json', encoding='utf-8-sig') as f:
    # + GMDB
    with open('C:/Users/15085/Desktop/Backup_2024.08.16/projects/05-FPGDKG/codes/fpgkb_website/fpgkb for Springboot/src/main/resources/recommend/pipeline/records_146155.json', encoding='utf-8-sig') as f:
        data = json.load(f)

    G = nx.Graph()
    edges = []
    for item in data:
        info = item['p']
        start_node = info['start']
        end_node = info['end']

        # 添加节点
        G.add_node(start_node['identity'], labels=start_node['labels'], properties=start_node['properties'])
        G.add_node(end_node['identity'], labels=end_node['labels'], properties=end_node['properties'])

        # 添加关系
        relation = info['segments'][0]['relationship']
        edges.append((relation['start'], relation['end'], {
            'type': relation['type'], 'properties': relation['properties'], 'key': relation['identity']
        }))

    G.add_edges_from(edges)
    return G
# def construct_nx():
#     # 加载JSONE:\fpgkb for Springboot\src\main\resources\recommend\pipeline\all.json
#     with open('E:/other/code/fpgkb for Springboot/src/main/resources/recommend/pipeline/all.json', encoding='utf-8-sig') as f:
#     # with open('/recommend/pipeline/all.json', encoding='utf-8-sig') as f:
#         data = json.load(f)
#
#     G = nx.Graph()
#     for i in range(0, len(data)):
#         info = data[i]['p']
#
#         start_node = info['start']
#         end_node = info['end']
#
#         # 添加节点
#         G.add_node(start_node['identity'], labels=start_node['labels'], properties=start_node['properties'])
#         G.add_node(end_node['identity'], labels=end_node['labels'], properties=end_node['properties'])
#
#         # 添加关系
#         relation = info['segments'][0]['relationship']
#         # G.add_edge (relation['start'], relation['end'], type = relation['type'] , properties = relation['properties'] ,)
#         G.add_edge(relation['start'], relation['end'], type=relation['type'], properties=relation['properties'],
#                    key=relation['identity'])
#
#     return G

    # '''
    # for start, end, data in G.edges(data=True):
    #     print(f"Edge ({start}, {end})  ID: {data['key']}")
    # '''
