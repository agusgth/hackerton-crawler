# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:20:51 2026

@author: boson
"""
import asyncio
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    UndetectedAdapter,DefaultMarkdownGenerator,PruningContentFilter
)
from crawl4ai.async_crawler_strategy import AsyncPlaywrightCrawlerStrategy
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
import time
import os
import pandas as pd

crawler_max_pages=50
path=r"C:\Users\AVenti01\Downloads2"
os.chdir(path)

i=0
initial_runtime =time.time()
current_runtime=initial_runtime


list_allrawmakrdowns=[]
url_list=[]
markdown_list=[]


async def main():
    # Create browser config
    current_runtime=time.time()
    browser_config = BrowserConfig(
        headless=False, #this can help the qc
        verbose=True,
    )

    # Create the undetected adapter
    undetected_adapter = UndetectedAdapter()

    # Create the crawler strategy with the undetected adapter
    crawler_strategy = AsyncPlaywrightCrawlerStrategy(
        browser_config=browser_config,
        browser_adapter=undetected_adapter
    )

    # Create the crawler
    async with AsyncWebCrawler(
        crawler_strategy=crawler_strategy,
        config=browser_config
    ) as crawler:
        # Configure the crawl
        crawler_config = CrawlerRunConfig(
                markdown_generator=DefaultMarkdownGenerator(
                    content_filter=PruningContentFilter()
                ),
            
                capture_console_messages=True,  # Test adapter console capture
        
                deep_crawl_strategy=BFSDeepCrawlStrategy(
                    max_depth=2, 
                    max_pages=crawler_max_pages,
                    
                    include_external=False)
                )

        # Test on a news site
        
        results = await crawler.arun(
            url="https://www.cbc.ca/news", 
            config=crawler_config
        )
       
        for result in results:
            """     
            with open(r'Markdown '+str(i)+'.txt', 'w') as textfile:
                textfile.write(result.markdown.raw_markdown)
            i+1
            """    
            print(f"Status: {result.status_code}")
            print(f"Success: {result.success}")
            print(f"Console messages captured: {len(result.console_messages or [])}")
            print(results.index(result))
            print(result.url)
            url_list.insert(results.index(result),result.url)
            markdown_list.insert(results.index(result),result.markdown.raw_markdown)
            print(len(markdown_list))
            
           
            #with open(r'Markdown '+str(results.index(result))+'.txt', 'w', encoding="utf-8") as textfile:
               # textfile.write(result.markdown.raw_markdown)
           
        markdown_data={"URL":url_list, "Markdown":markdown_list}
        
        df_markdown_data=pd.DataFrame(data=markdown_data)
        df_markdown_data.to_excel(path+r"\df_markdown_data.xlsx")
        
        try:
            df_markdown_data.to_csv(path+r"\df_markdown_data.txt")
        
        except:
            print("Error exportring markdowns to .txt")
            raise  
            
            
    """for result in results:
       # print(str(i))
       # print(f"Markdown content (first 500 chars):\n{result.markdown.raw_markdown[:500]}")
        #try:
        with open(r'Markdown '+str(i)+'.txt', 'w', encoding="utf-8") as textfile:
                textfile.write(result.markdown.raw_markdown)
                
                i+1
        #except:
           # pass
    """
if __name__ == "__main__":
    
    asyncio.run(main())
  