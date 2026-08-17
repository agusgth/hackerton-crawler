# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 15:55:37 2026

@author: agustin
"""

import tkinter as tk
from ttkbootstrap import Style
import ttkbootstrap as ttk
from tkinter import messagebox
import utilityfunctions as util
import pandas as pd
import crawler_main_BM25 as cm5
import asyncio
import ttkbootstrap
from ttkbootstrap.constants import *
import GrogAiParses as grog


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.style = Style(theme='darkly')
        self.root.title("Hackerton Crawler")
        self.root.geometry("450x400")

        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(expand=True, fill='both')

        self.title_label = ttk.Label( self.main_frame, text="Hackerton Crawler", font=('Helvetica', 18))
        self.title_label.pack(pady=5)

        ####################################################################################################

        self.path_frame = ttk.Frame(self.main_frame)
        self.path_frame.pack(fill='x', pady=5)

        self.path_label = ttk.Label( self.path_frame, text="Export Path:", font=('Helvetica', 11, "bold"))
        self.path_label.pack(anchor='w')

        self.path_entry = ttk.Entry( self.path_frame, font=('Helvetica', 11))
        self.path_entry.pack(fill='x', pady=(5, 0))
       
        ####################################################################################################
        self.brand_frame = ttk.Frame(self.main_frame)
        self.brand_frame.pack(fill='x', pady=5)

        self.brand_label = ttk.Label( self.brand_frame, text="Brand Name:", font=('Helvetica', 11, "bold"))
        self.brand_label.pack(anchor='w')

        self.brand_entry = ttk.Entry( self.brand_frame, font=('Helvetica', 11))
        self.brand_entry.pack(fill='x', pady=(5, 0))
        ####################################################################################################
        
        self.keywords_frame = ttk.Frame(self.main_frame)
        self.keywords_frame.pack(fill='x', pady=5)

        self.keywords_label = ttk.Label( self.keywords_frame, text="Keywords:", font=('Helvetica', 11, "bold"))
        self.keywords_label.pack(anchor='w')

        self.keywords_entry = ttk.Entry( self.keywords_frame, font=('Helvetica', 11))
        self.keywords_entry.pack(fill='x', pady=(5, 0))

        ####################################################################################################

        self.rb_group = ttk.Labelframe(self.root, text="Configuration", padding=10)
        self.rb_group.pack(pady=5, side=RIGHT)#fill=X,
    
        #################### Switch 1  #####################################################################
        self.switch1_state= tk.IntVar()
        self.switch2_state= tk.IntVar()
        
        self.check1 = ttk.Checkbutton(self.rb_group, text="Verbose Mode",variable=self.switch1_state  
                                      ,bootstyle="success-round-toggle",
                                      command=self.evaluar_estado)
        
        self.check1.pack(side=RIGHT, expand=YES, padx=5)
        self.check1.invoke()
        
        ## Switch 2 
        self.switch2_state= tk.IntVar()
        self.check2 = ttk.Checkbutton(self.rb_group, text="Headless Mode",variable=self.switch2_state  
                                      ,bootstyle="success-round-toggle",
                                      command=self.evaluar_estado)
        
        self.check2.pack(side=RIGHT, expand=YES, padx=5)
        self.check2.invoke()
         
        ####################################################################################################
         
        self.login_button = ttk.Button( self.main_frame, text="Run", command=self.verify_login, bootstyle="success", width=20)
        self.login_button.pack(pady=20)

        self.root.bind('<Return>', lambda event: self.verify_login())
        
        self.brand_entry.focus()
        
        ###################################################################################################
     

    def evaluar_estado(self):
        # Obtiene el valor booleano del interruptor
        if self.switch1_state.get()==1:
            print("Verbose Mode ON")
        if self.switch1_state.get()==0: 
            print("Verbose Mode OFF")
        if self.switch2_state.get()==1:
            print("Headless Mode ON")
        if self.switch2_state.get()==0: 
            print("Headless Mode OFF")    
        
        
            
    def verify_login(self):
        
        path=util.trim_path(self.path_entry.get())
        brandname = self.brand_entry.get()
        keywords = util.comma_del_str_tolist(self.keywords_entry.get())
        
        if self.switch1_state.get() ==1:
            switch1=True
        if self.switch1_state.get() ==0:
            switch1=False
            
        if self.switch2_state.get() ==1:
            switch2=True
        if self.switch2_state.get() ==0:
            switch2=False    
      
        print(str(switch1)+" Switch1") 
        print(str(switch2)+" Switch2")
        
        ########################################################################
        # Main Crawler function from the crawler_main_BM25
        asyncio.run(cm5.MainCrawler(path,switch1,switch2,keywords,brandname))
        print("Status: Async Crawler Finished ")
        ########################################################################
        # Grog Ai Parser
        df_fitmarkdown=pd.read_csv(path+"\\Raw Outputs" + "\\Fitmarkdown_data.txt")
        grog.grog_parse(df_fitmarkdown, path)
        ########################################################################
        
        messagebox.showinfo("Success", "Files exported to "+path, icon='info')
        self.clear_fields()


    def clear_fields(self):
        self.brand_entry.delete(0, tk.END)
        self.keywords_entry.delete(0, tk.END)
        self.brand_entry.focus()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()