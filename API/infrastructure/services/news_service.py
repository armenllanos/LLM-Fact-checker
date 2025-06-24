import time
import aiohttp
import asyncio
from typing import List, Dict, Any

from googlesearch import search
from infrastructure.services.embedding_service import EmbeddingService
import yake
import urllib.parse
import requests
from bs4 import BeautifulSoup
from config.settings import Settings
from core.entities.knowledge_source import KnowledgeSource
from core.entities.retrieved_news import RetrievedNews
from core.interfaces.i_news_service import INewsService
from sklearn.metrics.pairwise import cosine_similarity


class NewsService(INewsService):


    embedding_system:str
    search_engine:str = "www.bing.com"

    def __init__(self,settings:Settings):
        self.settings = settings
        self.embedding_model = EmbeddingService(settings)

    def get_news(self, source: KnowledgeSource,query:str,number_of_news:int,min_cos_dist:float = 0) -> list[RetrievedNews]:
        if source.international:
            keywords = self.get_keywords(query,'en')
        else:
            keywords = self.get_keywords(query)
        urls = self.massive_search(keywords,source)
        results = {}
        for url in urls:
            results[url] = self.get_articles(url,source)
        
        
        query_embeddings = self.embedding_model.get_embeddings(query)
        mejores_noticias = {}
        for r in results.values():
            r:RetrievedNews
            title_embedding =  self.embedding_model.get_embeddings(r.title)
            subtitle_embedding = self.embedding_model.get_embeddings(r.subtitle)
            title_score = cosine_similarity([query_embeddings], [title_embedding])[0][0]
            subtitle_score = cosine_similarity([query_embeddings], [subtitle_embedding])[0][0]
            mean_score = title_score+subtitle_score/2
            mejores_noticias[mean_score] = r.url
            
        valoraciones_resumen = sorted(mejores_noticias.keys(),reverse=True)
        return_list = []
        for value  in valoraciones_resumen:
            if (len(return_list) > number_of_news and value >= min_cos_dist):
                return_list.append(results[mejores_noticias[value]])
        return return_list()    
        
    
    def get_articles(self,url:str,source:KnowledgeSource)->RetrievedNews:
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Estos selectores dependen de la estructura del sitio
            title = soup.find(class_=source.title_class)
            title = title.get_text(strip=True) if title else 'No encontrado'
            resume = soup.find(class_=source.resume_class)
            resume = resume.get_text(strip=True) if resume else 'No encontrado'
            content = soup.find_all(class_=source.body_class,limit=10)
            contenido = " ".join([element.get_text(strip=True) for element in content])
            if len(contenido) == 0:
                contenido = 'No encontrado'
            return RetrievedNews(title=title,subtitle=resume,url=url,corpus=contenido,source=source)
        except Exception as e:
            return
        
    def get_keywords(text, language="es",max_keywords=10):
        extractor = yake.KeywordExtractor(lan=language, n=1, top=max_keywords)
        keywords = extractor.extract_keywords(text)
        return [kw for kw, score in keywords]
    
    def search(self,keywords,source:KnowledgeSource,lang):
        urls =[]
        query = "site:" + source.url + " " + " ".join(keywords)
        for url in search(query, lang=lang):
            if len(urls > self.settings.number_news_per_source-1):
                break
            urls.append(url)
            time.sleep(self.settings.wait_time_between_calls)
        return urls

    def massive_search(self,keywords,source:KnowledgeSource):
        try:    
            lang = 'es'
            if source.international:
                lang = 'en'
            return self.search(keywords,source,lang)
        except urllib.error.HTTPError as e:
            time.sleep(self.settings.wait_time_cortesy)
            return self.search(keywords,source,lang)
        except Exception as e:
            print(f"Error en búsqueda de {source.name}")
            print(f"Error:  {e}")


        query = "site: "+source.url+ + " ".join(keywords)
        query_encoded = urllib.parse.quote_plus(query)
        url = f"https://"+self.search_engine+"/search?q={query_encoded}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

    
        resp = requests.get(url, headers=headers)
        resp.raise_for_status() 
        soup = BeautifulSoup(resp.text, "html.parser")
        resultados = []
        
        titulos = soup.find_all('h2')
        resumenes = soup.find_all(class_='b_caption')
        urls = []
        for i in range(0,len(titulos)):
            url = titulos[i].find('a')['href']
            urls.append(url)
        return urls
    

        
