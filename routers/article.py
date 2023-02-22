import networkx as nx
from .db import get_db
from .models import SingleArticle
from fastapi import APIRouter

router = APIRouter(
    prefix='/article'
)


KEYWORDS_STR = [
    "Tesla", 
    "Microsoft", 
    "Apple",
    "Verizon",
    "Meta",
    "Coinbase",
    "Amazon",
    "Tencent"
]

@router.get("/recommend/{title}")
def recommend(title: str):
    db = get_db()
    document = SingleArticle.objects.search_text("\"{titl}\"".format(titl=title)).first() #Get the title of the document

    ####START CREATION OF GRAPH####
    G = nx.Graph()
    u = None #Graph node that will be used in algorithm
    count=1
    for i in SingleArticle.objects(): #Add nodes to graph
        tmp = i.toDict()
        G.add_node(count)
        G.nodes[count]['author']=tmp['author']
        G.nodes[count]['content']=tmp['content']
        G.nodes[count]['description']=tmp['description']
        G.nodes[count]['publishedAt']=tmp['publishedAt']
        G.nodes[count]['source']=tmp['source']
        G.nodes[count]['title']=tmp['title']
        G.nodes[count]['url']=tmp['url']
        G.nodes[count]['urlToImage']=tmp['urlToImage']

        if(document.toDict()['title']==tmp['title']):
            u = count
            print(u)

        count+=1
    from datetime import datetime
    from datetime import timezone

    for i in list(G.nodes.data()): #Add edges with criteria common 1) author, 2)source name or minimum timestamp difference
        tmp=i
        timestamp_node=None#Init node with minimum timestamp difference
        i[1]['publishedAt']
        dt = datetime.fromisoformat(i[1]['publishedAt'][:-1]).astimezone(timezone.utc)
        tp = int(round(datetime.timestamp(dt)))#Store timestamp of current node
        timestamp = abs( tp - 0)# Initialize minimum timestamp difference
        for j in list(G.nodes.data()):
            try:
                if i[1]['author'] == j[1]['author']:
                    G.add_edge(i[0], j[0])
                elif i[1]['source']['name'] == j[1]['source']['name']:
                    G.add_edge(i[0], j[0])

            except Exception as er:
                print(f'No SDN, author or timestamp')

            dt2 = datetime.fromisoformat(j[1]['publishedAt'][:-1]).astimezone(timezone.utc)
            tp2 = int(round(datetime.timestamp(dt2)))
            if abs( tp - tp2) < timestamp:#If timestamp difference is smaller keep that one
                timestamp =  abs( tp - tp2)
                timestamp_node = j
        G.add_edge(i[0], timestamp_node[0])#Add the node with the minimum timestamp difference

    ####END CREATION OF GRAPH####

    neighbors = G.neighbors(u) 
    max = 0 #max centality placeholder
    node_i =0 #neighbor node index that has max centality
    for i in neighbors:
        tmp = nx.closeness_centrality(G, u=i)
        #print(tmp)
        #print(i)
        if(max < tmp): #if new node is max
            node_i = i #change max neighbor node index
            max = tmp

    #print(max)
    #print(node_i)
    #print(G.nodes[node_i])
    #closeness_centrality = nx.closeness_centrality(G, u=list(neighbors))

    #return jsonify({'data': document.toDict()})
    return G.nodes[node_i] 