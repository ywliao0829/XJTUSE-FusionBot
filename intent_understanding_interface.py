"""
意图理解模块输出规范
"""

from typing import List, Dict, Optional

class Intent:
    """
    问题意图表示
    """
    question_id: str  # 问题ID
    question_type: str  # 问题类型：多意图/推理/多跳/细节/长文本/总结
    confidence: float  # 问题分类置信度
    main_intents: List[str]  # 主要意图列表（多意图问题）
    entities: List[Dict]  # 识别出的实体
    core_requirements: List[str]  # 核心需求描述，用户想要的核心答案（比如 “流程步骤”“当前利率”“是否符合条件”）
    reasoning_rules: Optional[List[str]]  # 推理所需的规则（推理问题）（比如 “贷款额度 = 月收入 ×12×50%”）
    multi_hop_steps: Optional[List[str]]  # 多跳步骤（多跳问题）找答案需要的步骤（比如 “先查贷款条件→再算负债率→最后判断额度”）
    summary_keywords: Optional[List[str]]  # 总结关键词（总结问题）

    def __init__(self, question_id, question_type, confidence, 
                 main_intents=None, entities=None, core_requirements=None,
                 reasoning_rules=None, multi_hop_steps=None, summary_keywords=None):
        self.question_id = question_id
        self.question_type = question_type
        self.confidence = confidence
        self.main_intents = main_intents or []
        self.entities = entities or []
        self.core_requirements = core_requirements or []
        self.reasoning_rules = reasoning_rules
        self.multi_hop_steps = multi_hop_steps
        self.summary_keywords = summary_keywords

    def to_dict(self):
        return {
            "question_id": self.question_id,
            "question_type": self.question_type,
            "confidence": self.confidence,
            "main_intents": self.main_intents,
            "entities": self.entities,
            "core_requirements": self.core_requirements,
            "reasoning_rules": self.reasoning_rules,
            "multi_hop_steps": self.multi_hop_steps,
            "summary_keywords": self.summary_keywords
        }

# 示例用法
if __name__ == "__main__":
    # 意图理解模块输出示例 - 多意图问题
    multi_intent_example = Intent(
        question_id="Q20231001001",
        question_type="multi_intent",
        confidence=0.92,
        main_intents=["申请流程", "利率政策"],
        entities=[
            {"text": "个人住房贷款", "type": "product", "start": 3, "end": 9},
            {"text": "最新", "type": "time", "start": 18, "end": 20}
        ],
        core_requirements=["流程步骤", "当前利率"],
        reasoning_rules=None,
        multi_hop_steps=None,
        summary_keywords=None
    )
    
    # 意图理解模块输出示例 - 推理问题
    reasoning_example = Intent(
        question_id="Q20231001002",
        question_type="reasoning",
        confidence=0.88,
        main_intents=["贷款条件判断"],
        entities=[
            {"text": "8000元", "type": "income", "start": 15, "end": 20},
            {"text": "2000元", "type": "debt", "start": 28, "end": 33},
            {"text": "100万元", "type": "asset", "start": 44, "end": 50},
            {"text": "50万元", "type": "loan_amount", "start": 65, "end": 71}
        ],
        core_requirements=["是否符合条件"],
        reasoning_rules=["贷款额度=月收入×12×50%", "负债率=负债/收入"],
        multi_hop_steps=None,
        summary_keywords=None
    )
    
    # 检索排序模块接收示例
    import json
    # 转字典
    output = {
        "Q20231001001": multi_intent_example.to_dict(),
        "Q20231001002": reasoning_example.to_dict()
    }
    
    with open("intents.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)