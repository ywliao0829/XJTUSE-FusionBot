"""
知识构建模块输出规范
"""

from typing import List, Dict, Optional

class KnowledgeItem:
    """
    单个知识点
    """
    item_id: str  # 知识点ID，格式：KI_{文档ID}_{序号}
    content: str  # 知识点文本内容
    source: Dict  # 来源信息
    entities: List[Dict]  # 识别出的实体
    keywords: List[str]  # 关键词
    type: str  # 知识点类型：规则/数据/流程/政策等
    relevance_score: float  # 权威性评分（0-1.0）比如法律条款评 1.0，普通说明书评 0.9

    def __init__(self, item_id, content, source, entities=None, 
                 keywords=None, type="general", relevance_score=0.8):
        self.item_id = item_id
        self.content = content
        self.source = source
        self.entities = entities or []
        self.keywords = keywords or []
        self.type = type
        self.relevance_score = relevance_score

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "content": self.content,
            "source": self.source,
            "entities": self.entities,
            "keywords": self.keywords,
            "type": self.type,
            "relevance_score": self.relevance_score
        }

class KnowledgeGraph:
    """
    知识图谱表示
    相当于上面单个零散的知识点，用关系连起来
    """
    nodes: List[Dict]  # 节点列表
    edges: List[Dict]  # 边列表

    def __init__(self, nodes=None, edges=None):
        self.nodes = nodes or []
        self.edges = edges or []

    def to_dict(self):
        return {
            "nodes": self.nodes,
            "edges": self.edges
        }

# 示例用法
if __name__ == "__main__":
    # 知识构建模块输出示例
    knowledge_items = [
        KnowledgeItem(
            item_id="KI_DOC_001_01",
            content="个人住房贷款年利率为4.5%",
            source={
                "doc_id": "DOC_001",
                "doc_type": "pdf",
                "path": "/data/docs/政策法规/商业银行法.pdf",
                "page": "第35条"
            },
            entities=[
                {"text": "个人住房贷款", "type": "product", "start": 0, "end": 6},
                {"text": "4.5%", "type": "rate", "start": 11, "end": 14}
            ],
            keywords=["个人住房贷款", "年利率", "4.5%"],
            type="rate",
            relevance_score=1.0
        ),
        KnowledgeItem(
            item_id="KI_DOC_002_01",
            content="贷款申请需提供身份证、收入证明和房产证明",
            source={
                "doc_id": "DOC_002",
                "doc_type": "word",
                "path": "/data/docs/产品说明书/个人住房贷款说明书.docx",
                "section": "申请材料"
            },
            entities=[
                {"text": "身份证", "type": "document", "start": 9, "end": 12},
                {"text": "收入证明", "type": "document", "start": 13, "end": 16},
                {"text": "房产证明", "type": "document", "start": 17, "end": 20}
            ],
            keywords=["贷款申请", "身份证", "收入证明", "房产证明"],
            type="requirement",
            relevance_score=0.9
        )
    ]
    
    # 知识图谱示例
    knowledge_graph = KnowledgeGraph(
        nodes=[
            {"id": "个人住房贷款", "type": "product", "label": "个人住房贷款"},
            {"id": "年利率", "type": "attribute", "label": "年利率"},
            {"id": "4.5%", "type": "value", "label": "4.5%"},
            {"id": "申请材料", "type": "requirement", "label": "申请材料"},
            {"id": "身份证", "type": "document", "label": "身份证"}
        ],
        edges=[
            {"source": "个人住房贷款", "target": "年利率", "relation": "has"},
            {"source": "年利率", "target": "4.5%", "relation": "value"},
            {"source": "个人住房贷款", "target": "申请材料", "relation": "requires"},
            {"source": "申请材料", "target": "身份证", "relation": "includes"}
        ]
    )
    
    # 意图理解模块接收示例
    # 写入 JSON 文件
    import json
    # 把所有知识点转成字典，知识图谱也转成字典，整合到一个大字典里
    output = {
        "knowledge_items": [item.to_dict() for item in knowledge_items],
        "knowledge_graph": knowledge_graph.to_dict()
    }
    
    with open("knowledge_base.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)