import requests
from typing import Dict

class DeepSeekClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1"
        
    def query_knowledge_graph(self, question: str, context: Dict) -> str:
        """查询知识图谱并通过DeepSeek生成回答"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个基于知识图谱的问答助手。"
                },
                {
                    "role": "user",
                    "content": f"基于以下知识图谱信息回答问题: {context}\n\n问题: {question}"
                }
            ]
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload
        )
        
        return response.json()["choices"][0]["message"]["content"]
