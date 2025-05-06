# ——————————————————————————————————————cosine——————————————————————————————————————
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
def cosine_score(G, embeddings, new_node_vector, index_map,node_id,fplist, top_k=3, top_n=3000):
    """
    计算新节点与现有节点的余弦相似度，并筛选出前 top_k 个最相似的节点
    按照标签分类：['Sample', 'Disease', 'Genotype', 'FacePhenotype', 'Variation']

    Args:
        G: 图对象，包含节点及其属性。
        embeddings: 所有节点的嵌入向量。
        new_node_vector: 新节点的嵌入向量。
        index_map: 节点索引映射，键为 Neo4j 节点索引，值为实际索引。
        top_k: 每个标签类别筛选的最相似节点数。
        top_n: 在 top_n 个最相似节点中进行筛选。

    Returns:
        similar_sample: 筛选出的节点索引列表。
        similar_score: 相应节点的余弦相似度分数。
    """
    # 计算相似度
    similarities = cosine_similarity(new_node_vector.reshape(1, -1), embeddings)[0]

    # 按相似度排序，获取前 top_n 个节点的索引
    most_similar_idx = similarities.argsort()[::-1][:top_n]

    # 映射到 Neo4j 节点索引
    neo4j_index = [list(index_map.keys())[idx] for idx in most_similar_idx]
    user_index =list(index_map.keys())[list(index_map.values()).index(int(node_id))]
    fp_index = [list(index_map.keys())[idx] for idx in fplist]
    fp_index.append(user_index)
    # print(user_index)
    # 定义需要筛选的标签类别
    labels_to_check = ['Sample', 'Disease', 'Genotype', 'FacePhenotype', 'Variation']

    similar_sample = []
    similar_score = []

    # 针对每个标签筛选前 top_k 个节点
    for label in labels_to_check:
        count = 0
        for i, node_idx in enumerate(most_similar_idx):
            # (neo4j_index[i])
            if neo4j_index[i] in fp_index:
                continue
            # 检查节点是否属于当前标签
            if G.nodes[node_idx]['labels'] == [label]:
                similar_sample.append(neo4j_index[i])
                similar_score.append(similarities[node_idx])
                #print(f"  从零排序index：{node_idx}     neo4j_index：{neo4j_index[i]}          label：{label}   cos_sim_score：{similarities[node_idx]}")
                count += 1
                if count == top_k:
                    break

    return similar_sample, similar_score
# def cosine_score(G, embeddings, new_node_vector, index_map,nodeid):
#     # 初始化 KNN 模型
#     neigh = NearestNeighbors(n_neighbors=10, metric='cosine')
#     neigh.fit(embeddings)
#
#     # 查找与新节点最相似的 10 个节点
#     nearest_nodes = neigh.kneighbors([new_node_vector], 10, return_distance=False)
#     sim_scores = 1 / (neigh.kneighbors([new_node_vector], 10, return_distance=True)[0] + 1)
#
#     # 分别存储 Sample 节点和其他类型的节点
#     similar_sample = []
#     similar_score = []
#     other_nodes = []
#     other_scores = []
#
#     for i, node_idx in enumerate(nearest_nodes[0]):
#         neo4j_id = index_map[node_idx]
#         node_data = G.nodes[node_idx]
#
#         if neo4j_id ==int(nodeid):
#             continue
#
#         # 如果是 Sample 节点，加入 Sample 列表
#         if 'Sample' in node_data['labels']:
#             similar_sample.append(neo4j_id)
#             similar_score.append(sim_scores[0][i])
#             print(f"Sample node found: Index: {node_idx}, Neo4j ID: {neo4j_id}, Label: {node_data['labels']}, Score: {sim_scores[0][i]}")
#         else:
#             # 如果不是 Sample 节点，加入其他节点列表
#             other_nodes.append(neo4j_id)
#             other_scores.append(sim_scores[0][i])
#             print(f"Other node found: Index: {node_idx}, Neo4j ID: {neo4j_id}, Label: {node_data['labels']}, Score: {sim_scores[0][i]}")
#
#     # 如果没有找到任何 Sample 节点，返回其他节点
#     if not similar_sample:
#         print("Warning: No Sample nodes found in the top 10 similar nodes. Returning other types of nodes.")
#         similar_sample = other_nodes
#         similar_score = other_scores
#
#     return similar_sample, similar_score
# def cosine_score(G , embeddings , new_node_vector , index_map):
#
#
#
#
#     # 查找最近的10个节点
#     neigh = NearestNeighbors(n_neighbors=10,metric='cosine')
#     neigh.fit(embeddings)
#
#
#     # 查找与new_node最相似的10个节点
#     nearest_nodes = neigh.kneighbors([new_node_vector], 10, return_distance=False)
#
#     # nearest_nodes从0开始，需要转换为id
#     nearest_ids = [list(index_map.keys())[idx] for idx in nearest_nodes[0]]
#
#     # 计算相似度分数
#     sim_scores = (1 / (neigh.kneighbors([new_node_vector], 10, return_distance=True)[0] + 1))
#
#     similar_sample = []
#     similar_score = []
#     for i in range(1, 10):
#         # if (G.nodes[nearest_nodes[0][i]]['labels'] == ['Sample']):
#         similar_sample.append(nearest_ids[i])
#         similar_score.append(sim_scores[0][i])
#         print(f"  从零排序index：{nearest_nodes[0][i]}     neo4j_index：{nearest_ids[i]}          label：{G.nodes[nearest_nodes[0][i]]['labels']}   knn_score：{sim_scores[0][i]}".encode('utf-8', 'ignore').decode('utf-8'))
#
#
#     '''返回前 10 节点中的 sample'''
#     return similar_sample , similar_score
#
#
#     # # 计算相似度
#     # similarities = cosine_similarity(new_node_vector.reshape(1,-1), embeddings)
#     #
#     # # 排序
#     # most_similar_idx = similarities[0].argsort()[::-1]
#     # neo4j_index = [list(index_map.keys())[idx] for idx in most_similar_idx]
#     #
#     # # 取得最相似的节点
#     # top10_similar_nodes = most_similar_idx[0:10]
#     #
#     # # 筛选sample
#     # similar_sample = []
#     # similar_score = []
#     # for i in range(1, 10):
#     #     if (G.nodes[top10_similar_nodes[i]]['labels'] == ['Sample']):
#     #         similar_sample.append(neo4j_index[i])
#     #         similar_score.append(similarities[0][top10_similar_nodes[i]])
#     #         print(f"  从零排序index：{top10_similar_nodes[i]}     neo4j_index：{neo4j_index[i]}          label：{G.nodes[top10_similar_nodes[i]]['labels']}   cos_sim_score：{similarities[0][top10_similar_nodes[i]]}")
#     #
#     #
#     # '''返回前 10 节点中的 sample'''
#     # return similar_sample , similar_score
