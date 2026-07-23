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
import pandas as pd

crawler_max_pages=100
#path=r"E:\Python\Hackerton"
#os.chdir(path)

i=0


list_allrawmakrdowns=[]
url_list=[]
markdown_list=[]


async def main(path:str,switch1,switch2):
    # Create browser config
    
  
    
    browser_config = BrowserConfig(
        headless=switch2, #this can help the qc
        verbose=switch1,
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

            print(f"Status: {result.status_code}")
            print(f"Success: {result.success}")
            print(f"Console messages captured: {len(result.console_messages or [])}")
            print(results.index(result))
            print(result.url)
            url_list.insert(results.index(result),result.url)
            markdown_list.insert(results.index(result),result.markdown.raw_markdown)
            print(len(markdown_list))
             
        markdown_data={"URL":url_list, "Markdown":markdown_list}
        
        df_markdown_data=pd.DataFrame(data=markdown_data)
        df_markdown_data.to_csv(path+r"\df_markdown_data.csv")
        df_markdown_data.to_csv(path+r"\df_markdown_data.txt")
        
"""
if __name__ == "__main__":
    
    asyncio.run(main())
"""