# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 19:04:27 2026

@author: boson
"""

import itertools
import pandas as pd

path_text="E:\Python\Hackerton\BM25ContentFilter\df_markdown_data.csv"

def trim_markdown_list(path_text):
    df_text=pd.read_csv(path_text)
    list_df_text=[]
    listoflists=[]
    newlistoflists=[]
    
    
    for i in range(len(df_text.index)):
        list_df_text.append(df_text.iloc[i,2])
        
    lists = list_df_text
    
    for i in range(len(lists)):
        listoflists.append(lists[i].split("\n"))
        
    for i in range(len(listoflists)-1):
        
        newlistoflists.append([elem for elem in listoflists[i] if elem not in listoflists[i+1]])
        
    return newlistoflists.append(listoflists[len(listoflists)-1])



"""   
setn=[(sorted(set(listoflists[i]), key=listoflists[i].index)) for i in range(len(listoflists))]

#setn=[(set(listoflists[i])) for i in range(len(listoflists))]


#setn0=sorted(set(listoflists[0]), key=listoflists[0].index) 

setn2=[(set(listoflists[i])-set(listoflists[i+1])) for i in range(0,len(listoflists)-1)]

print(setn[45])

setn2.append(setn[len(setn)-1])

z=[str("\n".join(str(y))) for x in setn2 for y in x]
print("---------------")

print(setn2[44])
for x in range(len(setn2)):
    print(x)
    print(setn2[x])
    
    #z.append("\n".join((str(y) for y in x)))
    
    
#xx=[("\n".join((str(y) for y in x))) x in setn2]

#newlist="\n".join(str(x) for x in setn2[0])

"""