
# coding: utf-8

# ## read edges from the file&the k-shortest

# In[317]:


import networkx as nx
from itertools import islice


#G=nx.Graph()
#create_using=nx.DiGraph(),
G = nx.read_edgelist('edges_new.txt', create_using=nx.DiGraph(), nodetype=int, data=(('mode',int), ('cap',float),('flow',float),('len',float),('disu',float)))
#print(G.edges.data())
#print(list(G.edges.data())[0])



# In[318]:


def k_shortest_paths(G, source, target, k, weight=None):
    return list(islice(nx.shortest_simple_paths(G, source, target, weight='disu'), k))
    
source = 274
target = 480
Paths = k_shortest_paths(G, source, target, 3)
_3weights=[]
for path in Paths:
    print (len(path))
    print (path)
    sum=float(0)
    for i in range(len(path)-1):
        weight=G.edges[path[i],path[i+1]]['disu']
        sum=sum+weight
    print (sum)
    _3weights.append(sum)
print (_3weights)
sum = 0
for i in range(len(_3weights)):
    sum+=_3weights[i]
ave1=sum / len(_3weights)
print (ave1)


# In[319]:


import math
def flow_allocation(Flow,weights):
    c =  [ 0 for _ in range(len(weights))]
    sum = 0
    for i in range(len(weights)):
        c[i] = math.exp(-0.2*weights[i])
        sum += c[i]
    flow = [ 0 for _ in range(len(weights))]
    for i in range(len(weights)):
        flow[i] = Flow * c[i] / sum
    return flow


weight_paths = []
for path in Paths:
    weight_path = []
    for i in range(len(path)-1):
        weight_path.append(G.edges[path[i],path[i+1]]['disu'])
    weight_paths.append(weight_path)


# ## Add node attributes

# In[320]:


import re
fh=open("expandnode2_forweight.txt", "r")
srs=fh.readlines()
for sr in srs:
    sr_1=re.split('\s', sr)
    #print(sr_1)
    a=int(sr_1[0])
    b=float(sr_1[1])
    c=float(sr_1[2])
    G.add_node(a, Loc=b, Tra=c)

# print(G.nodes[0]["Loc"])
# print(G.nodes.data())
#alst = list(G.edges.data())
#print(alst[0][2])


# ## Update the weight

# 两个不同的起点到同一个终点6条
# 58
# 两次循环之间，最短路权值平均值<0.1

# In[321]:


import math
def Update_path():
    for i in range(len(path)-1):
        if G.edges[path[i], path[i+1]]['mode'] ==1:
            veh=12
            t0=G.edges[path[i],path[i+1]]['len'] / veh
            weight= 10*t0+20*2/60+15*0.2*t0+0.1*math.pow(t0,2)
            G.add_edge(path[i], path[i+1], disu=weight)
            
        if G.edges[path[i], path[i+1]]['mode'] ==2:
            veh=48
            t0=G.edges[path[i],path[i+1]]['len'] / veh
            k = (G.edges[path[i],path[i+1]]['flow']/G.edges[path[i], path[i+1]]['cap'] 
                 +4*10/G.edges[path[i], path[i+1]]['cap'])
            weight = 10*t0+(10+20)*t0*0.15*math.pow(k, 4)+20*11/60
            G.add_edge(path[i], path[i+1], disu=weight)
            
        if G.edges[path[i], path[i+1]]['mode'] ==3:
            j=1
            for link in list(G.edges.data()):
                #print(link)
                #print(link[0])
                p=link[0]
                q=link[1]
                if (link[2]['mode']==2 and G.node[p]['Loc'] == G.node[path[i]]['Loc'] 
                    and G.node[q]['Loc']==G.node[path[i+1]]['Loc'] and 
                    G.node[q]['Tra'] == G.node[path[i+1]]['Tra']):
                    j += 1
                    print(j)
                    veh=25
                    t0=G.edges[path[i],path[i+1]]['len'] / veh
                    k = G.edges[p, q]['flow'] / G.edges[p, q]['cap']+4*10/G.edges[p, q]['cap']
                    weight = (10*t0+10*t0*0.15*math.pow(k, 4)+20*0.5/10+20*2/60+
                              20*G.edges[path[i],path[i+1]]['flow']/250+2)
                    G.add_edge(path[i], path[i+1], disu=weight)
                                                                                 
        if G.edges[path[i], path[i+1]]['mode'] ==4:
            t0 = 3 / 60                                                                    
            weight = 10 * t0 + 20*0.5/10+20*5/60+20*G.edges[path[i],path[i+1]]['flow']/30000+3
            G.add_edge(path[i], path[i+1], disu=weight)
                                                        
        if G.edges[path[i], path[i+1]]['mode'] ==0:
            if G.nodes[path[i]]['Tra'] != G.nodes[path[i+1]]['Tra']:
                weight = 20*5/60
                G.add_edge(path[i], path[i+1], disu=weight)
            else:
                weight = 0
                G.add_edge(path[i], path[i+1], disu=weight)
    return 


# In[322]:


#print(_3weights)
Flow_paths_sum = flow_allocation(1200, _3weights)       #3条最短路各自对应流量

#print(Flow_paths_sum)
Flow_paths=[]              #把每条路每部分的流量计算出来，三条路都存在列表中
for i in range(len(Paths)):
    Flow_paths.append(flow_allocation(Flow_paths_sum[i], weight_paths[i]))
j=0
for path in Paths:
    for i in range(len(path)-1):
        #G.add_edge(path[i],path[i+1],flow = Flow_paths[j][i])
        G.add_edge(path[i],path[i+1],flow = Flow_paths_sum[j])   #按照一条路的流量
    j+=1

#print (weight_paths)
# s1 = []
# for path in Paths:
#     for i in range(len(path)-1):
#         s1.append(G.edges[path[i],path[i+1]]['disu'])

# s2 = []
# for path in Paths:
#     Update_path()
#     for i in range(len(path)-1):
#         s2.append(G.edges[path[i],path[i+1]]['disu'])


# In[323]:


for path in Paths:
    Update_path()
    #更新每一条路的权值

# for path in Paths:
#     for i in range(len(path)-1):
#         weight=G.edges[path[i],path[i+1]]['disu']
#         sum=sum+weight
#     _3weights.append(sum)
#     #更新3条路的总权值
# Flow_paths_sum = flow_allocation(1200, _3weights)       #3条最短路各自对应权值
Paths_new = k_shortest_paths(G, source, target, 3)
_3weights=[]
for path in Paths_new:
    print (len(path))
    print (path)
    sum=float(0)
    for i in range(len(path)-1):
        weight=G.edges[path[i],path[i+1]]['disu']
        sum=sum+weight
    print (sum)
    _3weights.append(sum)
print (_3weights)
sum = 0
for i in range(len(_3weights)):
    sum+=_3weights[i]
ave2=sum / len(_3weights)
print (ave2)
print(ave2-ave1)


# In[324]:


while math.fabs(ave2-ave1) >= 0.5:
    #重新分配流量
    Flow_paths_sum = flow_allocation(1200, _3weights) 
    
    Flow_paths=[]              #把每条路每部分的流量计算出来，三条路都存在列表中
#     weight_paths_new= []
#     for path in Paths_new:
#         weight_path_new= []
#         for i in range(len(path)-1):
#             weight_path_new.append(G.edges[path[i],path[i+1]]['disu'])
#         weight_paths_new.append(weight_path_new)
#     for i in range(len(Paths_new)):
#         Flow_paths.append(flow_allocation(Flow_paths_sum[i], weight_paths_new[i]))
    j=0
    for path in Paths_new:
        for i in range(len(path)-1):
            #G.add_edge(path[i],path[i+1],flow = Flow_paths[j][i])
            G.add_edge(path[i],path[i+1],flow = Flow_paths_sum[j])
        j+=1
    #根据新的流量，计算新的权值并更新
    for path in Paths_new:
        Update_path()
    #比较差值
    ave1=ave2
    Paths_new = k_shortest_paths(G, source, target, 3)
    _3weights=[]
    for path in Paths_new:
        print (len(path))
        print (path)
        sum=float(0)
        for i in range(len(path)-1):
            weight=G.edges[path[i],path[i+1]]['disu']
            sum=sum+weight
        print (sum)
        _3weights.append(sum)
    print (_3weights)
    sum = 0
    for i in range(len(_3weights)):
        sum+=_3weights[i]
    ave2=sum / len(_3weights)
    
print(ave2-ave1)

#转换flow数据类型
for edge in list(G.edges.data()):
    tem = edge[2]['flow']
    tem1=int(tem)
    G.add_edge(edge[0], edge[1], flow=tem1)

j=0
m0 = 0
m1 = 0
m2 = 0
m3 = 0
m4 = 0
for path in Paths_new:
    for i in range(len(path)-1):
        if G.edges[path[i], path[i+1]]['mode'] == 0:
            m0 += G.edges[path[i], path[i+1]]['flow']
        elif G.edges[path[i], path[i+1]]['mode'] == 1:
            m1 += G.edges[path[i], path[i+1]]['flow']
        elif G.edges[path[i], path[i+1]]['mode'] == 2:
            m2 += G.edges[path[i], path[i+1]]['flow']
        elif G.edges[path[i], path[i+1]]['mode'] == 3:
            m3 += G.edges[path[i], path[i+1]]['flow']
        elif G.edges[path[i], path[i+1]]['mode'] == 4:
            m4 += G.edges[path[i], path[i+1]]['flow']
print(m0, m1,m2,m3,m4)

j=0
for path in Paths_new:
    print ('最短路路长度',len(path))
    print ('最短路路径',path)
    print ('该路总权重',_3weights[j])
    print ('该路总流量', Flow_paths_sum[j])
    w = []
    f = []
    for i in range(len(path)-1):
        w.append(G.edges[path[i],path[i+1]]['disu'])
        f.append(G.edges[path[i],path[i+1]]['flow'])
    print('每条边权重',w)
    print('每条边流量',f)
    
    


# In[ ]:




