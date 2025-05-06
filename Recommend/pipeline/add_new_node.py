def add_new_node(G, nodeid , sid , age , race , region , gender , fplist):

    G.add_node(int(nodeid), labels=['Sample'], properties={
        "race": race,
        "gender": gender,
        "year": age,
        "`sample number`": 1,
        "region": region,
        "sid": sid})


    # fplist = [613,567,495,552,540,831,815,  825,401,453,351]

    # sample与表型连接 nodeid——sampleid
    i=0
    for n in fplist:
        i+=1
        G.add_edge ( n, nodeid , type = "Mention_FP" , properties = {} , key = 30000 + i)
        #print(f" start--end : {nodeid}--{n}  edge: {G.edges.get((nodeid ,n))}".encode('utf-8', 'ignore').decode('utf-8'))

    # print(G.nodes)
    # print(G.nodes(data=True))
    # print(G.edges(data=True))
    # print(f" lenth: {len(G.nodes())}  last node:{ G.nodes[nodeid] }".encode('utf-8', 'ignore').decode('utf-8'))
