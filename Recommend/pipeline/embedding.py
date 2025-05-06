from karateclub import NodeSketch,GLEE
def embedding(G):
    # 检查图的连通性


    # 使用 GLEE 模型计算嵌入
    model = GLEE(dimensions=512,seed=40)
    model.fit(G)

    # 获取嵌入
    embeddings = model.get_embedding()

    # 获取新节点的嵌入向量
    new_node_id = len(G.nodes()) - 1  # 假设新节点是最后一个节点
    if new_node_id >= len(embeddings):
        print("Error: New node embedding not found.")
        new_node_vector = None
    else:
        new_node_vector = embeddings[new_node_id]

    return embeddings, new_node_vector
# def embedding(G):
#     # model_NodeSketch = NodeSketch( iterations=1, decay=0.01 )
#     # model_NodeSketch.fit(G)
#     model_GLEE = GLEE(seed=100)
#     model_GLEE.fit(G)
#
#
#     embeddings = model_GLEE.get_embedding()
#
#     print(G.nodes[len(G.nodes())-1])
#     new_node_vector = embeddings[len(G.nodes())-1]
#     return embeddings, new_node_vector
