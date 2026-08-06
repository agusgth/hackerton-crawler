# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 12:36:50 2026

@author: boson
"""





def trim_path(export_path:str) -> str:
    
    if (export_path.rfind("\\")==(len(export_path)-1)):
        return export_path.replace("\"","")[:-1]
    else: 
        return export_path.replace("\"","")


key=["health","medicare"]
raw_markdown=["asdsdsd"," is medicare ","medicare","asdasddsds","/health/ health medicare","healthy"]




def comma_del_str_tolist(comma_sep_string:str)-> list:
    
    return [item.strip() for item in (comma_sep_string.strip().split(","))]




def score_keywords_count(raw_markdown:str,key:list,brandname:str) -> list:
    score1=[0]*len(key)
    if raw_markdown.upper().count(brandname.upper())>0:
        score_brand=10
    else:
        score_brand=0
    
    
    for y in range(len(key)):
            print(raw_markdown.upper().count(key[y].upper()))
            score1[y] = raw_markdown.upper().count(key[y].upper())
    if 0 not in score1:             
        return(sum(score1),sum(score1)*2,score_brand)      
    else:
        return(sum(score1),0,score_brand)
            


