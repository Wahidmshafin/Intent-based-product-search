from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

class KeywordExtractor:

    def __init__(self):
        self.llm = ChatOllama(
            model="qwen2.5:3b-instruct",
            temperature=0,
            base_url="http://ollama:11434" #http://localhost:11435
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system","You are a helpful assistant that extract keywords from given query."),
                ("human","{input}")
            ]
        )
    
    def extract_keywords(self, input:str)->str:
        chain = self.prompt | self.llm
        response = chain.invoke({"input":input}).content
        return {"response": response}