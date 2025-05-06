from neo4j import GraphDatabase
import argparse
URI = "bolt://localhost:7687/test"
#URI = "bolt://neo4j:7687/test"
#driver = GraphDatabase.driver(URI, auth=("neo4j" , "hmqww123"))
driver = GraphDatabase.driver(URI, auth=("neo4j" , "aA1508525874!"))

def get_args():
    parser = argparse.ArgumentParser('reset', add_help=False)
    parser.add_argument("--nodeid", type=str)
    return parser.parse_args()


# 删除病人节点
def delete_node(tx , sid):
    tx.run("MATCH (n:Sample {sid: $sid}) DELETE n", sid=sid)

# 删除所有边
def delete_edge(tx , sid):
    tx.run("MATCH (a)-[r]-(b) WHERE a.sid = $sid DELETE r", sid=sid)


def reset_neo4j(args):

    sid = "user_" + args.nodeid

    # 删除新边, 删除节点
    with driver.session(database="test") as session:

        # 删除所有边
        session.execute_write(delete_edge, sid)

        # 删除节点
        session.execute_write(delete_node, sid)


if __name__ == '__main__':
    opts = get_args()
    reset_neo4j(opts)
