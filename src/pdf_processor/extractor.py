import pdfplumber
import spacy
from typing import Dict, List, Tuple

class PDFExtractor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        # 加载中文NLP模型
        self.nlp = spacy.load("zh_core_web_sm")
        
    def extract_text(self) -> str:
        """提取PDF中的文本内容"""
        text = ""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text
    
    def extract_entities(self, text: str) -> List[Dict]:
        """提取命名实体"""
        doc = self.nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            })
        return entities
    
    def extract_relationships(self, text: str) -> List[Tuple]:
        """提取实体关系"""
        doc = self.nlp(text)
        relationships = []
        for token in doc:
            if token.dep_ in ["nsubj", "dobj"]:
                relationships.append((
                    token.head.text,
                    token.dep_,
                    token.text
                ))
        return relationships