# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 11:47:01 2026

@author: boson
"""

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
    UndetectedAdapter,DefaultMarkdownGenerator,PruningContentFilter,BM25ContentFilter
)
from crawl4ai.async_crawler_strategy import AsyncPlaywrightCrawlerStrategy
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy,DFSDeepCrawlStrategy,BestFirstCrawlingStrategy
from crawl4ai.deep_crawling.filters import (FilterChain,URLPatternFilter,DomainFilter,ContentTypeFilter)
from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer
import pandas as pd
import utilityfunctions as util

crawler_max_pages=500
#path=r"E:\Python\Hackerton"
#os.chdir(path)

i=0


list_allrawmakrdowns=[]
url_list=[]
markdown_list=[]
fit_markdown_list=[]
cleaned_html=[]
metadata=[]
score=[]
urls=["https://www.axios.com","https://www.usatoday.com/news","https://apnews.com/us-news","https://www.reuters.com/world/us/"]

async def main(path:str,switch1,switch2,keywords1:list,brandname:str):

    # Scorer Config
    scorer = KeywordRelevanceScorer(
    #keywords=["health", "care","medicare"],
    keywords=keywords1,
    weight=0.6
    )
    # Create browser config
    browser_config = BrowserConfig(
        headless=switch2, #this can help the qc
        verbose=switch1,
    )
    
    filter_chain =  FilterChain([
                    ContentTypeFilter(allowed_types=[r"text/html"])
                    ])

    # Create the crawler
    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Configure the crawl
        crawler_config = CrawlerRunConfig( 
                
                exclude_social_media_links=True,
                exclude_external_images=True,
                excluded_tags=["aside","nav", "footer", "header", "form","head","ul","img","li"], #,"list","button","li"
                deep_crawl_strategy=BestFirstCrawlingStrategy(max_depth=2,url_scorer=scorer,
                                                              max_pages=5000, 
                                                              #filter_chain=filter_chain,
                                                              include_external=False),
                
                markdown_generator=DefaultMarkdownGenerator(content_filter=PruningContentFilter(),options={"ignore_links": True}),
                capture_console_messages=True, 
                )

        # Test on a news site
        
        results0 = asyncio.create_task(crawler.arun( url=urls[0], config=crawler_config)) 
        results1= asyncio.create_task(crawler.arun( url=urls[1], config=crawler_config))
        results2= asyncio.create_task(crawler.arun( url=urls[2], config=crawler_config))
        results3= asyncio.create_task(crawler.arun( url=urls[3], config=crawler_config))
        await results0
        await results1
        await results2
        await results3
        
        
        #print(str(len(results0.result()))+" - "+str(len(results1.result()))+" - "+str(len(results2.result())))
        results=results0.result()+results1.result()+results2.result()+results3.result()
        print(str(len(results)))
        
        for result in results:

            print(f"Status: {result.status_code}")
            print(f"Success: {result.success}")
            print(f"Console messages captured: {len(result.console_messages or [])}")
            #print(results.index(result))
            print(result.url)
            if result.success:
                if((len(result.markdown.raw_markdown)>200) and 
                   (sum(util.score_keywords_count(result.markdown.raw_markdown,keywords1,brandname))>=2)):
                    
                    print("Fit Markdown (BM25 query-based):")
                    print(result.markdown.raw_markdown)
                    url_list.insert(results.index(result),result.url)
                    markdown_list.insert(results.index(result),result.markdown.raw_markdown)
                    fit_markdown_list.insert(results.index(result),result.markdown.fit_markdown)
                    cleaned_html.insert(results.index(result),result.cleaned_html)
                    metadata.insert(results.index(result),result.metadata)
                    score.append(sum(util.score_keywords_count(result.markdown.raw_markdown,keywords1,brandname)))
                    
                    
            else:
                print("Error:", result.error_message)
            
        #markdown_data={"URL":url_list, "Markdown":markdown_list}
        fit_markdown_data={"URL":url_list,"Score":score, "Fit Markdown":fit_markdown_list}
        cleaned_html_data={"URL":url_list, "Fit Markdown":cleaned_html}
        metadata_data={"URL":url_list, "Fit Markdown":metadata}
        
        #df_markdown_data=pd.DataFrame(data=markdown_data)
        df_fitmarkdown_data=pd.DataFrame(data=fit_markdown_data)
        df_cleaned_html=pd.DataFrame(data=cleaned_html_data)
        df_metadata=pd.DataFrame(data=metadata_data)
        
        #df_markdown_data.to_csv(path+r"\df_markdown_data.csv")
        #df_markdown_data.to_csv(path+r"\df_markdown_data.txt")
        df_fitmarkdown_data.to_csv(path+r"\df_fitmarkdown_data.txt")
        df_cleaned_html.to_csv(path+r"\df_cleaned_html.txt")
        df_metadata.to_csv(path+r"\df_metadata.txt")

    
        
"""
if __name__ == "__main__":
    
    asyncio.run(main())
"""