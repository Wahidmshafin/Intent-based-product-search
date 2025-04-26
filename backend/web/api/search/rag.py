from langchain_ollama import ChatOllama, OllamaEmbeddings, OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable
from backend.web.api.search.schema import Keywords, QueryExpension
from backend.db.dao.history_dao import HistoryDAO

class SearchPipeline:

    def __init__(self):
        
        self.embedding = OllamaEmbeddings(
            model = "nomic-embed-text",            
            keep_alive= -1,
            base_url="http://ollama:11434" #http://localhost:11435
        )

        

        # self.llm = ChatOllama(
        #     model="qwen2.5:3b-instruct",
        #     temperature=0,
        #     keep_alive= -1,
        #     base_url="http://ollama:11434" #http://localhost:11435
        # )
        self.fune_tuned_llm = ChatOllama(
            model="ecommerce-ner-model",
            temperature=0,
            keep_alive= -1,
            base_url="http://ollama:11434" #http://localhost:11435
        )
        self.fine_promt =ChatPromptTemplate.from_messages(
            [
                ("system","""
                [NER] Extract entities:\n
                 """),
                
                ("human","{input}")
            ]
        )

    def generate_embedding(self, input:str)->str:
        return self.embedding.embed_query(input)
        

    def generate_test_rag(self, input:str)->str:
        chain = self.fine_promt | self.fune_tuned_llm
        response = chain.invoke({"input":input})
        return response.model_dump()
    
    
        # self.keyword_prompt = ChatPromptTemplate.from_messages(
        #     [
        #         ("system","""
        #         You are a highly accurate keyword-extraction assistant.
        #         Your sole task is to read the provided text and output only the most relevant keywords, separated by commas—nothing else.
                

        #         ### Instruction:
        #         Extract the keywords present in the input text.
        #         • Return only the keywords, separated by commas.
        #         • Do not add any extra words, explanations, or formatting.
        #         • Do not return any empty list.

        #         ### Examples:

        #         #### Example 1
        #         **Input:**
        #         "The UltraSound 2000 Wireless Noise-Cancelling Headphones deliver up to 30 hours of battery life, a comfortable over-ear design, and Bluetooth 5.2 connectivity."
        #         **Output:**
        #         UltraSound 2000, wireless, noise-cancelling, 30 hours battery life, over-ear design, Bluetooth 5.2

        #         #### Example 2
        #         **Input:**
        #         "The FreshBrew 12-Cup Programmable Coffee Maker features a digital touchscreen, auto brew timer, and a stainless-steel carafe for optimal brewing."
        #         **Output:**
        #         FreshBrew 12-Cup Programmable Coffee Maker, digital touchscreen, auto brew timer, stainless-steel carafe, optimal brewing

        #         #### Example 3
        #         **Input:**
        #         "The AeroBoost Running Shoes offer a breathable mesh upper, responsive cushioning, and a durable rubber outsole ideal for marathon training."
        #         **Output:**
        #         AeroBoost Running Shoes, breathable mesh upper, responsive cushioning, durable rubber outsole, marathon training
        #          """),
                
        #         ("human","{input}")
        #     ]
        # )

        # self.query_expension_prompt = ChatPromptTemplate.from_messages(
        #     [
        #         ("system","""
        #         You are an AI assistant specialized in e-commerce query expansion and product information generation.

        #         Given an input search query from a user, follow these steps precisely:
        #         1. **Reformulate the Query**  
        #         - Identify key terms and generate relevant synonyms or related category keywords.  
        #         - Extract potential product attributes (e.g., color, size, material, use case).

        #         2. **Generate Structured Output**  
        #         - Produce a JSON object with the following schema:  
        #             ```json
        #             {{
        #             "expanded_query": "<the enriched query including synonyms and attributes>",
        #             "product_title": "<a concise, SEO-friendly title for the top matching product>",
        #             "product_details": "<a detailed description including key features, specifications, and use cases>"
        #             }}
        #             ```

        #         3. **Adhere to E-Commerce Best Practices**  
        #         - Ensure the `product_title` is no longer than 70 characters and includes the primary keyword.  
        #         - In `product_details`, cover at least three bullet-point features, material or composition, and intended use case.  
        #         - Maintain clarity, relevancy, and user intent alignment.

        #         4. **Respond Only with the JSON object.**  

        #          """),
                
        #         ("human","{input}")
        #     ]
        # )
        

    # def extract_keywords(self, input:str)->str:
    #     model = self.llm.with_structured_output(Keywords)
    #     chain = self.keyword_prompt | model
    #     response = chain.invoke({"input":input}).response
    #     return response

    # def query_expension(self, input:str)->str:
    #     model = self.llm.with_structured_output(QueryExpension)
    #     chain = self.query_expension_prompt | model
    #     response = chain.invoke({"input":input})
    #     return response.to_string()
    
        
# Blue color Samsung smartphone with 8GB RAM and 256GB ROM and it should have a big screen and should be waterproof.