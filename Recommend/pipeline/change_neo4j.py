from neo4j import GraphDatabase, Transaction

# 创建病人节点
def create_node(tx: Transaction, race: str, gender: str, age: int, region: str, sid: str):
    tx.run(
        """
        CREATE (n:Sample {race: $race, gender: $gender, year: $age, region: $region, sid: $sid})
        """,
        race=race, gender=gender, age=age, region=region, sid=sid
    )

# 创建连接 FP 边
def create_edge(tx: Transaction, sid: str, FPid: str):
    tx.run(
        """
        MATCH (a:Sample {sid: $sid})
        WITH a
        MATCH (b:FacePhenotype {pid: $FPid})
        CREATE (b)-[r:Mention_FP]->(a)
        """,
        sid=sid, FPid=FPid
    )

# 创建连接 sample 边，避免笛卡尔积
def create_similar_edge(tx: Transaction,G, sid: str, b_type: str, b_id: str, score: float):
    type_to_property = {
        "Disease": "did",
        "Article": "pmid",
        "FacePhenotype": "pid",
        "Genotype": "geneId",
        "Sample": "sid",
        "Variation": "details"
    }

    if b_type not in type_to_property:
        raise ValueError(f"Unsupported node type: {b_type}")

    b_property = type_to_property[b_type]
    id_juti = G.nodes[b_id]['properties'][b_property]

    query = f"""
        MATCH (a:Sample {{sid: $sid}})
        WITH a
        MATCH (b:{b_type} {{{b_property}: $b_id}})
        CREATE (a)-[r:SIMILAR {{score: $score}}]->(b)
    """
    tx.run(query, sid=sid, b_id=id_juti, score=score)

# 主函数：更改 Neo4j 数据
def change_neo4j(
        G_filter,sid: str, age: int, race: str, region: str, gender: str,
        fplist: list, similar_sample: list, similar_score: list
):
    # 配置 Neo4j 数据库连接
    #URI = "bolt://neo4j:7687/test"
    URI = "bolt://localhost:7687/test"
    #AUTH = ("neo4j", "hmqww123")
    AUTH = ("neo4j", "aA1508525874!")

    # 创建数据库连接
    driver = GraphDatabase.driver(URI, auth=AUTH)

    try:
        # 开启会话
        with driver.session(database="test") as session:
            # 创建节点
            print(f"Creating node for sample with sid: {sid}")
            session.execute_write(create_node, race, gender, age, region, sid)
            #print("Nodes created", flush=True)

            # 创建表型连接
            for FPid in fplist:
                # print(type(G_filter.nodes[FPid]['properties']['pid']))
                # print(G_filter.nodes[FPid]['properties']['pid'])
                # print(f"Creating edge between sample {sid} and phenotype {G_filter.nodes[FPid]['properties']['pid']}")
                session.execute_write(create_edge, sid, G_filter.nodes[FPid]['properties']['pid'])
                #print("edges created", flush=True)

            # 创建推荐 sample 的相似性边
            for id, score in zip(similar_sample, similar_score):
                # print(f"Creating SIMILAR edge between sample {sid} and {G_filter.nodes[id]['labels'][0]}:{id} with score {score}")
                session.execute_write(create_similar_edge,G_filter, sid,G_filter.nodes[id]['labels'][0], id, score)
                #print("similar created", flush=True)

    # create_similar_edge(tx: Transaction, sid: str, b_type: str, b_id: str, score: float):
    except Exception as e:
        # 捕获并打印错误
        print(f"An error occurred: {e}")

    # finally:
    #     # 关闭数据库连接
    #     driver.close()
    #     print("Database connection closed.")
# from neo4j import GraphDatabase
# from neo4j import Transaction
#
#
# # 创建病人节点
# def create_node(tx , race , gender , age , region , sid ):
#     tx.run("CREATE (n:Sample { race: $race, gender: $gender,  year: $age , region: $region, sid:$sid })", race=race, gender=gender , age=age , region=region, sid=sid)
#
# # 创建连接 FP 边
# def create_edge(tx , sid, FPid):
#     tx.run("MATCH (a), (b) WHERE a.sid = $sid AND b.pid = $FPid CREATE (b)-[r:Mention_FP]->(a)",
#             sid=sid, FPid=FPid)
#
# # 创建连接 sample 边
# def create_similar_edge(tx , sid, id , score):
#     tx.run("MATCH (a), (b) WHERE a.sid = $sid AND b.pid = $id CREATE (a)-[r:SIMILAR {score: $score}]->(b)",
#             sid=sid, id=id , score=score)
#
#
#
#
# def change_neo4j(sid , age , race , region , gender , fplist , similar_sample , similar_score):
#     #URI = "bolt://neo4j:7687/test"
#     URI = "bolt://localhost:7687/test"
#     driver = GraphDatabase.driver(URI, auth=("neo4j", "hmqww123"))
#
#
#     with driver.session(database="test") as session:
#         # 创建节点
#         session.execute_write(create_node, race, gender, age, region, sid)
#
#         # 连接表型
#         for FPid in fplist:
#             session.execute_write(create_edge, sid, FPid)
#
#         # 连接推荐sample
#         for id, score in zip(similar_sample, similar_score):
#             session.execute_write(create_similar_edge, sid, id, score)



    # with GraphDatabase.driver(URI, auth=("neo4j", "hmqww123")) as driver:
    #     driver.verify_connectivity()
    #     print(driver.execute_query("MATCH (n) WHERE n.sid="+'"'+"user_849113365"+'"'+" RETURN n"))


