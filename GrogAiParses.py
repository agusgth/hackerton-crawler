# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 09:39:02 2026

@author: agustin
"""

#import pandas as pd
import os
from openai import OpenAI

def grog_parse(df_fitmarkdown,path:str):

    os.makedirs(path+"\\Top Articles", exist_ok=True)

    api_key1=[r"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",r"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"
              ,r"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",r"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"]
    #modelo=r"llama-3.3-70b-versatile"
    
    def grog_ai_titlerequest(text:str,key:str,modelo:str)->str:
        # 1.
        # 
        client = OpenAI(
            base_url=r"https://api.groq.com/openai/v1",
            api_key=key
        )
        
    
        #"llama-3.3-70b-versatile"
        # 
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {
                    "role": "system", 
                    "content": "Your only taks is to produce a short title,no more than nine words, direct for the text given, without semicollons or spacial characters, spaces are permited. Without intructions, explanations."
                },
                {
                    "role": "user", 
                    "content": f"Generate the title for the text: \n\n{text}"
                }
            ],
            temperature=0.5,
            max_tokens=30
        )
    
        return response.choices[0].message.content.strip().replace("''", "")
    
    
    
    for i in range(0,30):
        
        try:
            title=grog_ai_titlerequest(df_fitmarkdown["Fit Markdown"].iloc[i],api_key1[0],"llama-3.3-70b-versatile")
            
        except:    
            try:
                title=grog_ai_titlerequest(df_fitmarkdown["Fit Markdown"].iloc[i],api_key1[1],"llama-3.3-70b-versatile")
            except:
                try:
                    title=grog_ai_titlerequest(df_fitmarkdown["Fit Markdown"].iloc[i],api_key1[2],"llama-3.3-70b-versatile")
                except:
                    try:
                        title=grog_ai_titlerequest(df_fitmarkdown["Fit Markdown"].iloc[i],api_key1[3],"llama-3.3-70b-versatile")
                    except:
                        title=str(i)
        
                
        with open(path+"\\Top Articles"+"\\" + title + r".txt", "w", encoding="utf-8") as file:
            file.write(df_fitmarkdown["Fit Markdown"].iloc[i])
        
        
    

