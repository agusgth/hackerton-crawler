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
