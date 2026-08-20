# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 11:47:01 2026

@author: agustin
"""

import asyncio
import itertools
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    DefaultMarkdownGenerator,PruningContentFilter,
    #BM25ContentFilter
)
#from crawl4ai.async_crawler_strategy import AsyncPlaywrightCrawlerStrategy
#from crawl4ai.deep_crawling.filters import (ContentTypeFilter,FilterChain)
from crawl4ai.deep_crawling import BestFirstCrawlingStrategy
from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer
import pandas as pd
import utilityfunctions as util
import os


list_allrawmakrdowns=[]
url_list=[]
markdown_list=[]
fit_markdown_list=[]
cleaned_html=[]
metadata=[]
score=[]
urls=["https://www.axios.com","https://www.usatoday.com/news","https://apnews.com/us-news",
      "https://edition.cnn.com","https://www.businessinsider.com","https://finance.yahoo.com/topic/latest-news/",
      "https://ohiocapitaljournal.com","https://penncapital-star.com/news","https://floridaphoenix.com",
      "https://ncnewsline.com","https://wisconsinexaminer.com","https://michiganadvance.com"]

async def MainCrawler(path:str,switch1,switch2,keywords1:list,brandname:str):

    # Scorer Config
    scorer = KeywordRelevanceScorer(keywords=keywords1,weight=0.6)
    # Create browser config
    browser_config = BrowserConfig(
        #browser_type="webkit",
         #browser_type="chromium",
       # channel="chrome",
        headless=switch2, #this can help the qcing 
        verbose=switch1,
)
    
    #filter_chain =  FilterChain([ContentTypeFilter(allowed_types=[r"text/html"])])

    # Create the crawler
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Configure the crawl
        crawler_config = CrawlerRunConfig( 
                remove_overlay_elements=True,
                exclude_social_media_links=True,
                exclude_external_images=True,
                remove_forms=True,
                excluded_tags=["aside","nav", "footer", "header", "form",
                               "head","ul","img","li","img","button",
                               "script", "style"], #,"list","button","li"
                deep_crawl_strategy=BestFirstCrawlingStrategy(max_depth=2,url_scorer=scorer,
                                                              max_pages=5000, 
                                                              #filter_chain=filter_chain,
                                                              include_external=False),
                
                markdown_generator=DefaultMarkdownGenerator(content_filter=PruningContentFilter(),options={"ignore_links": True}),
                capture_console_messages=True, 
                )

        # Test on a news site
        async with asyncio.TaskGroup() as tg:
            results_tasks=[tg.create_task(crawler.arun( url=urls[i], config=crawler_config)) 
                           for i in range(len(urls))]
        
        results_list = [t.result() for t in results_tasks]
        results=list(itertools.chain.from_iterable(results_list))
        
        #results = await asyncio.gather(*results_tasks)   
            

        for result in results:

            if result.success:
                if((len(result.markdown.raw_markdown)>200) and 
                   (sum(util.score_keywords_count(result.markdown.raw_markdown,keywords1,brandname))>=2)):
                    
                    #print("Fit Markdown (BM25 query-based):")
                    #print(result.markdown.fit_markdown)
                    url_list.insert(results.index(result),result.url)
                    markdown_list.insert(results.index(result),result.markdown.raw_markdown)
                    fit_markdown_list.insert(results.index(result),result.markdown.fit_markdown)
                    cleaned_html.insert(results.index(result),result.cleaned_html)
                    metadata.insert(results.index(result),result.metadata)
                    score.append(sum(util.score_keywords_count(result.markdown.raw_markdown,keywords1,brandname)))
                    
                    
            else:
                print("Error:", result.error_message)
            
        
        fit_markdown_data={"URL":url_list,"Score":score, "Fit Markdown":fit_markdown_list}
        cleaned_html_data={"URL":url_list, "Fit Markdown":cleaned_html}
        metadata_data={"URL":url_list, "Fit Markdown":metadata}
        
       
        df_fitmarkdown_data=pd.DataFrame(data=fit_markdown_data).sort_values(by="Score", ascending=False)
        df_cleaned_html=pd.DataFrame(data=cleaned_html_data)
        df_metadata=pd.DataFrame(data=metadata_data)
        
        os.makedirs(path+"\\Raw Outputs", exist_ok=True)
        df_fitmarkdown_data.to_csv(path+"\\Raw Outputs" + "\\Fitmarkdown_data.txt")
        df_cleaned_html.to_csv(path+"\\Raw Outputs"+ "\\Cleaned_html.txt")
        df_metadata.to_csv(path+r"\\Raw Outputs"+ "\\Metadata.txt")
        
           
        

        
