from pipeline.construct_nx import  construct_nx
from pipeline.add_new_node import  add_new_node
from pipeline.graph_sort import  graph_sort
from pipeline.embedding import  embedding
from pipeline.cosine_score import  cosine_score
from pipeline import change_neo4j
import argparse

'''
age = "6 y"
race = "Turkish"
region = "Turkey"
gender = "M"
fplist = [613,567,495,552,540,831,815,  825,401,453,351]
'''


# 运行
# python recommend.py --age "6 y" --race "Turkish" --region "Turkey" --gender "M" --HP "HP:0000343,HP:0012471,HP:0012810,HP:0011822,HP:0000325" --nodeid 8558904
# 重置
# python reset_neo4j.py --nodeid 8558904


'''java中运行'''
# Runtime rt = Runtime.getRuntime();
# command = "python recommend.py --age "6 y" --race "Turkish" --region "Turkey" --gender "M" --HP "HP:0000343,HP:0012471,HP:0012810,HP:0011822,HP:0000325""
# Process p = rt.exec(command);


def get_args():
    parser = argparse.ArgumentParser('recommend', add_help=False)

    parser.add_argument('--age', type=str)
    parser.add_argument('--race', type=str)
    parser.add_argument('--region', type=str)
    parser.add_argument("--gender", type=str)
    parser.add_argument("--HP", type=str)
    parser.add_argument("--nodeid", type=str)
    return parser.parse_args()


def main(args):

    sid = "user_" + args.nodeid

    # print(sid)



    print("————————construct_nx————————")
    G = construct_nx()
    print("————————————————————————————")


    fplist = []
    list = args.HP.split(",")
    for n in G.nodes():
        if 'pid' in G.nodes[n]["properties"] and G.nodes[n]["properties"]["pid"] in list:# 存在pid这个属性，并且是传入表型
            #print(G.nodes[n]["properties"]["pid"])
            fplist.append(n)



    print("————————add_new_node————————")
    #add_new_node(G, int(args.nodeid), sid , args.age , args.race , args.region , args.gender , fplist)
    add_new_node(G, int(args.nodeid), sid, args.age, args.race, args.region, args.gender, fplist)
    print("————————————————————————————")



    print("—————————graph_sort—————————")
    #G , index_map = graph_sort(G)
    G_filter , reverse_index_map,fplist_new = graph_sort(G,fplist)
    print("————————————————————————————")



    print("—————————embeddings—————————")
    #embeddings , new_node_vector = embedding(G)
    embeddings, new_node_vector = embedding(G_filter)
    print("————————————————————————————")


    print("———————————cos_sim——————————")
    #similar_sample , similar_score = cosine_score(G , embeddings , new_node_vector , index_map)
    similar_sample , similar_score = cosine_score(G_filter , embeddings , new_node_vector , reverse_index_map,args.nodeid,fplist_new)
    print("————————————————————————————")



    print("—————————change_neo4j———————")
    #change_neo4j.change_neo4j(sid, args.age, args.race, args.region, args.gender, fplist, similar_sample, similar_score)
    change_neo4j.change_neo4j(G_filter,sid, args.age, args.race, args.region, args.gender, fplist_new, similar_sample, similar_score)
    print("————————————————————————————")


if __name__ == '__main__':
    opts = get_args()
    main(opts)
