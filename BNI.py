#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 23:16:58 2022

@author: batdora
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx



"""This Project aims to maximize network "effective" connectivity by modeling
an already established successful business model: BNI"""




#VARIABLES

#constant variables

    #people joining per month
newcomers= 3

    #hpeople leaving per mont
leave=2

    #rate of weekly edge increase
weekly_edge= 2

    #rate of increase in wage per node
weekly_wage_increase= 0.05

    #rate of success per signal (currently %70)
def success_rate(x):
    
    "this function takes the output of the function increase_success() as an arguement"
    
    if np.random.rand() * x >= 0.3:
        return 1
    else:
        return 0
    
#dependent variables

    #monthyl most redound (the one who made others more rich)
redound_edges= 10

    #increase in success per node
def increase_success(x):
    
    "this function takes the #of previous successfull jobs as an arguement"
    
    if x > 20:
        return 2.5
    
    if x > 10:
        return 2
    
    if x > 5:
        return 1.5
    else:
        return 1
    
    
#independent variables
    
    #new edge per node (currently at %50)
def new_connection():
    if np.random.rand() >= 0.5:
        return 1
    else:
        return 0
    
    #income per node
def income():
    return np.random.randint(20,100)

    #redound rate per node
def redound_rate(k):
    
   "this function takes in k as an arguement and divides it by 5"
    
   if np.random.rand() * k/5 >= 0.7:
       return 3
   elif np.random.rand() * k/5 >= 0.5:  
       return 2
   else:
       return 1
    
    
#GROUPS & MEETINGS

#Güç Takımları
groups= {1:"IT",2:"Advertising",3:"Health",4:"Finance and Law",5:"Estate",6:"Etc"}
jobs=np.zeros([50,6])


#Meetings per month
guc_meeting= 1
main_meeting= 4


#THE NETWORK

"""currently the network starts with 50 people"""

BNI=np.identity(50)

"""the second arguement for np.zeros defines the #of attributes per member"""
attributes=["job","income","success","k","rich club"]

BNI_members=np.zeros([50,5])

#Members
def new_member():
    job= np.random.randint(1,7)
    inc= income()
    suc= np.random.randint(1,4)
    k= 3
    rich=0
    
    return [job,inc,suc,k,rich]
    

    #First Members

for i in range(50):
    BNI_members[i]=new_member()
    jobs[i][int(BNI_members[i,0])-1] = i+1
    
    
    
    # j1-j6 represents the people in job groups with their index
    
    

j1= list(jobs[:,0])
j1[:] = (int(value)-1 for value in j1 if value != 0)
for i in j1:
    for j in j1:
        BNI[i,j]= 1
        BNI_members[i,3]=BNI_members[i,3]+1

j2= list(jobs[:,1])
j2[:] = (int(value)-1 for value in j2 if value != 0)
for i in j2:
    for j in j2:
        BNI[i,j]= 1
        BNI_members[i,3]=BNI_members[i,3]+1

j3= list(jobs[:,2])
j3[:] = (int(value)-1 for value in j3 if value != 0)
for i in j3:
    for j in j3:
        BNI[i,j]= 1
        BNI_members[i,3]=BNI_members[i,3]+1

j4= list(jobs[:,3])
j4[:] = (int(value)-1 for value in j4 if value != 0)
for i in j4:
    for j in j4:
        BNI[i,j]= 1
        BNI_members[i,3]=BNI_members[i,3]+1

j5= list(jobs[:,4])
j5[:] = (int(value)-1 for value in j5 if value != 0)
for i in j5:
    for j in j5:
        BNI[i,j]= 1
        BNI_members[i,3]=BNI_members[i,3]+1

j6= list(jobs[:,5])
j6[:] = (int(value)-1 for value in j6 if value != 0)
for i in j6:
    for j in j6:
        BNI[i,j]= 1
        BNI_members[i,3]=BNI_members[i,3]+1
        
#Making every person non-connected to themselves

for i in range(len(BNI[:,1])):
    for j in range(len(BNI[:,1])):
        if j == i:
            BNI[i,j]= 0



#The Hubs and the Rich CLub

rich_club_lead= [j1[0],j2[0],j3[0],j4[0],j5[0],j6[0]]
rich_club_secondary= [j1[1],j2[1],j3[1],j4[1],j5[1],j6[1]]

for i in rich_club_lead:
    BNI_members[i,4] = 2
    BNI_members[i,3]=BNI_members[i,3]+len(rich_club_lead)-1
    for j in rich_club_lead:
        BNI[i,j]= 1

for i in rich_club_secondary:
    BNI_members[i,4] = 1

for i in range(len(BNI[:,1])):
    for j in range(len(BNI[:,1])):
        if j == i:
            BNI[i,j]= 0
    

plt.figure(0)
sns.heatmap(BNI,center=1)


plt.figure(1)
graph=nx.from_pandas_adjacency(pd.DataFrame(BNI))
#nx.draw(graph, node_size= 10, width= 0.5)
nx.draw(graph, node_size=70, width= 0.8)

    
#TIME & GROWTH

time= list(range(0,30))
average_k=[]

for i in range(len(time)):
    average_k.append(BNI_members[:,3].mean())
    if i%7 == 0:
        for j in range(0,len(BNI[1])):
            if np.random.rand()>0.5:
                a= np.random.randint(0,len(BNI[1]))
                while a == j:
                    a= np.random.randint(0,len(BNI[1]))
                if BNI[j,a]== 0:
                    BNI[j,a]=1
                    BNI[a,j]=1
                    BNI_members[j,3] = BNI_members[j,3] +1
                    BNI_members[a,3] = BNI_members[a,3] +1
                    
plt.figure(2)
plt.plot(time,average_k)
plt.title("Average K over Time")
plt.xlabel("Time")
plt.ylabel("<k>")

plt.figure(3)
sns.heatmap(BNI,center=1)


#NETWORK GRAPH DRAWER

plt.figure(4)
graph=nx.from_pandas_adjacency(pd.DataFrame(BNI))
#nx.draw(graph, node_size= 10, width= 0.5)
nx.draw(graph, node_size=70, width= 0.8)






