from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

import os


class Agent:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.0, model="gpt-3.5-turbo")
    
    def _load_db(self):
        faiss_index_path = os.path.join(os.path.dirname(__file__), "faiss_index")
        # faiss_indexがなければエラー
        if not os.path.exists(faiss_index_path):
            raise Exception("faiss_index not found.")
        else:
            self.db = FAISS.load_local(faiss_index_path, OpenAIEmbeddings())
    
    def _search_neighborhood(self, question: str, k: int = 3):
        self._load_db()
        # faiss_indexからk近傍を探索
        neighbors = self.db.similarity_search_with_score(question, k=k)
        return neighbors
    
    def _generate_answer(self, question: str, neighbors: list):
        template = """Question: {question}
        質問に対して以下の記事を元に、400字程度で回答を作成してください。

        {article}
        
        Answer:"""

        prompt = PromptTemplate(template=template, input_variables=["question", "article"])
        llm_chain = LLMChain(llm=self.llm, prompt=prompt)

        articles = [neighbor[0].page_content for neighbor in neighbors]
        metadata = [neighbor[0].metadata for neighbor in neighbors]
        scores = [neighbor[1] for neighbor in neighbors]

        answer = llm_chain.run(question=question, article='\n\n'.join(articles))
        return answer, metadata
    
    def ask(self, question: str):
        neighbors = self._search_neighborhood(question)
        answer, metadata = self._generate_answer(question, neighbors)
        return answer, metadata

if __name__ == "__main__":
    agent = Agent()
    question = "サッカー日本代表について教えてください。"
    answer, metadata = agent.ask(question)
    print(answer)
    print(metadata)