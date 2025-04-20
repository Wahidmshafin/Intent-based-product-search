from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

class KeywordExtractor:

    def __init__(self):
        self.llm = ChatOllama(
            model="qwen2.5:3b-instruct",
            temperature=0
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system","You are a helpful assistant that extract keywords from given query."),
                ("human","{input}")
            ]
        )
    
    async def extract_keywords(self, input:str)->str:
        chain = self.prompt | self.llm
        return await chain.invoke({"input":input}).content