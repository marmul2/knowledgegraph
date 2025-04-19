from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional

from src.pdf_processor.extractor import PDFExtractor
from src.knowledge_graph.builder import KnowledgeGraphBuilder
from src.llm_integration.deepseek import DeepSeekClient

app = FastAPI()

# 配置
PDF_PATH = "关于建立碳足迹管理体系的实施方案.pdf"
DEEPSEEK_API_KEY = "your_api_key"

# 初始化组件
pdf_extractor = PDFExtractor(PDF_PATH)
kg_builder = KnowledgeGraphBuilder()
deepseek_client = DeepSeekClient(DEEPSEEK_API_KEY)

class Question(BaseModel):
    text: str
    context: Optional[Dict] = None

@app.post("/query")
async def query(question: Question):
    try:
        # 如果没有提供上下文,则查询知识图谱
        if not question.context:
            # 这里需要实现从Neo4j查询相关知识的逻辑
            question.context = {}
            
        # 调用DeepSeek生成回答
        answer = deepseek_client.query_knowledge_graph(
            question.text,
            question.context
        )
        
        return {"answer": answer}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rebuild-kg")
async def rebuild_knowledge_graph():
    try:
        # 提取文本
        text = pdf_extractor.extract_text()
        
        # 提取实体和关系
        entities = pdf_extractor.extract_entities(text)
        relationships = pdf_extractor.extract_relationships(text)
        
        # 重建知识图谱
        kg_builder.build_graph(entities, relationships)
        
        return {"message": "Knowledge graph rebuilt successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))