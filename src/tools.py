# src/tools.py
from datetime import datetime
import re

def get_current_week():
    """获取当前是第几周（校历，3月1日为开学第1周）"""
    today = datetime.now()
    start_day = datetime(2026, 3, 1)
    week_num = (today - start_day).days // 7 + 1
    return f"现在是校历第{week_num}周"

def calculate_gpa(scores_str):
    """
    计算平均绩点
    输入格式示例：'85,90,78'
    绩点规则：>=90=4.0 |80~89=3.0 |70~79=2.0 |60~69=1.0 |<60=0
    """
    scores = [int(x) for x in scores_str.split(',')]
    total = 0.0
    for s in scores:
        if s >= 90:
            total += 4.0
        elif s >= 80:
            total += 3.0
        elif s >= 70:
            total += 2.0
        elif s >= 60:
            total += 1.0
        else:
            total += 0.0
    gpa = total / len(scores)
    return f"您的平均绩点是：{gpa:.2f}"

# 新增：智能路由函数，识别用户输入并分发对应工具
def chat_tool(user_text):
    # 判断是否询问周数
    week_keywords = ["现在第几周", "第几周", "校历周", "现在是第几周"]
    for word in week_keywords:
        if word in user_text:
            return get_current_week()
    # 判断是否计算绩点（包含数字逗号）
    nums = re.findall(r"\d+", user_text)
    if len(nums) >= 2:
        score_str = ",".join(nums)
        return calculate_gpa(score_str)
    # 无匹配提示
    return "支持两种功能：1.输入「现在第几周」查询校历周；2.输入分数如85,100,100计算绩点"

# 交互入口：自主输入分数/文字计算
if __name__ == "__main__":
    print("===== 智能工具：周数查询与绩点计算器 =====")
    while True:
        user_input = input("\n请输入你的问题：")
        # 输入exit退出程序
        if user_input.lower() == "exit":
            print("程序退出")
            break
        res = chat_tool(user_input)
        print(res)