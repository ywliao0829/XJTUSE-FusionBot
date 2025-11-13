"""
检索排序模块输出规范
必须符合比赛要求的result.json格式
"""

import json
from typing import List, Dict

def validate_result_format(result_file: str) -> bool:
    """
    验证result.json格式是否符合比赛要求（参考代码，我没具体看提交要求）
    1. 基础验证：顶层结构必须是 JSON 数组
    比赛要求 result.json 的最外层必须是[]（数组），不能是字典（{}）。
    比如示例里的result = [{"question_id": "...", ...}, ...]，就是符合要求的数组结构。
    2. 每个问题的必填字段验证
    每个数组元素（对应一个用户问题）必须满足两个核心要求：
    必须有question_id：且是字符串类型（比如"Q20231001001"），不能是数字或空值。
    必须有knowledge_points：是列表类型，且固定包含 3 个字符串（比赛强制要求知识点数量为 3）。
    3. 知识点细节验证
    每个知识点必须是字符串（不能是字典、数字等其他类型）。
    单个知识点长度不能超过 1500 字符（超过会触发警告，避免内容过长不符合赛事限制）。
    4. 异常处理
    如果读取文件失败、格式不符合要求，会直接打印具体错误（比如 “缺少 question_id”“知识点数量不是 3”），方便开发者快速修改。
    """
    try:
        with open(result_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # 检查顶层是否为数组
        if not isinstance(data, list):
            print("错误：顶层结构必须是JSON数组")
            return False
            
        # 检查每个对象
        for item in data:
            # 检查question_id
            if "question_id" not in item or not isinstance(item["question_id"], str):
                print(f"错误：缺少或格式错误的question_id: {item}")
                return False
                
            # 检查knowledge_points
            if "knowledge_points" not in item or not isinstance(item["knowledge_points"], list):
                print(f"错误：缺少或格式错误的knowledge_points: {item['question_id']}")
                return False
                
            if len(item["knowledge_points"]) != 3:
                print(f"错误：knowledge_points数量必须为3: {item['question_id']}")
                return False
                
            # 检查每个知识点
            for i, point in enumerate(item["knowledge_points"]):
                if not isinstance(point, str):
                    print(f"错误：知识点必须是字符串: {item['question_id']}, 索引{i}")
                    return False
                    
                if len(point) > 1500:
                    print(f"警告：知识点长度超过1500字符: {item['question_id']}, 索引{i}, 长度{len(point)}")
        
        print("result.json格式验证通过")
        return True
    except Exception as e:
        print(f"格式验证错误: {str(e)}")
        return False

# 示例用法
if __name__ == "__main__":
    # 检索排序模块输出示例
    result = [
        {
            "question_id": "Q20231001001",
            "knowledge_points": [
                "《商业银行个人住房贷款管理办法》规定，个人住房贷款申请需准备以下材料：1. 身份证明文件（身份证、户口簿等）；2. 收入证明（近6个月银行流水、工资单等）；3. 购房合同或意向书；4. 首付款证明；5. 信用报告。材料齐全后，提交至银行信贷部门，一般3-5个工作日完成初审。",
                "个人住房贷款审批流程如下：1. 客户提交申请材料；2. 银行进行初审（1-2个工作日）；3. 实地考察与评估（2-3个工作日）；4. 风险评估与审批（3-5个工作日）；5. 签订贷款合同；6. 办理抵押登记；7. 贷款发放。全流程通常需要10-15个工作日。",
                "个人住房贷款申请注意事项：1. 确保信用记录良好，无逾期记录；2. 收入证明需覆盖月供的2倍以上；3. 首付款比例不得低于30%；4. 贷款年限最长30年，且借款人年龄+贷款年限≤70岁；5. 需购买房贷保险。特殊情况可咨询银行客户经理。"
            ]
        },
        {
            "question_id": "Q20231001002",
            "knowledge_points": [
                "根据《个人住房贷款管理规定》第25条，贷款额度计算公式为：可贷额度 = 月收入 × 12 × 贷款年限 × 50% - 负债余额。本例中，客户月收入8000元，负债2000元，无其他负债，可贷额度 = 8000 × 12 × 30 × 50% - 2000 × 12 × 30 = 1,440,000 - 720,000 = 720,000元，大于50万元，因此符合贷款条件。",
                "客户资质评估：1. 收入负债比 = 月负债/月收入 = 2000/8000 = 25%，低于监管要求的50%上限；2. 月供收入比 = 月供/月收入 = (500,000/360)×4.5%/8000 ≈ 7.8%，远低于30%的警戒线；3. 名下房产价值100万元，可作为优质抵押物。综合评估，客户完全符合50万元信用贷款条件。",
                "贷款条件说明：根据我行《个人信用贷款管理办法》，申请50万元信用贷款需满足：1. 月收入≥5000元；2. 负债收入比≤50%；3. 信用记录良好；4. 工作稳定（入职≥1年）。本例客户月收入8000元，负债2000元，负债收入比25%，且有房产作为辅助担保，完全符合贷款条件，建议批准。"
            ]
        }
    ]
    
    # 保存为result.json
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # 验证格式
    validate_result_format("result.json")