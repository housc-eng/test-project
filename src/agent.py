# src/agent.py
import re
from tools import get_current_week, calculate_gpa
from rag import vector_db, client, RAG_PROMPT

MAX_HISTORY = 10

# 修改：新增history入参，不再依赖文件内部全局变量
def rag_answer_with_memory(question, history):
    docs = vector_db.similarity_search(question, k=3)
    context = "\n\n".join([d.page_content for d in docs])
    system_prompt = f"""你是安徽交通职业技术学院校园百事通助手，只能依据下面校园知识库回答，禁止编造内容。
知识库参考内容：
{context}
"""
    messages = [{"role": "system", "content": system_prompt}]
    # 使用外部传入的历史对话
    messages.extend(history[-MAX_HISTORY:])
    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=0.3
    )
    return response.choices[0].message.content

# ReAct意图分发，接收外部history
def agent_chat(user_input, history):
    if "周" in user_input and ("几" in user_input or "校历" in user_input):
        return get_current_week()
    if "绩点" in user_input or "GPA" in user_input:
        scores = re.findall(r'\d+', user_input)
        if scores:
            return calculate_gpa(','.join(scores))
        else:
            return "请输入各科分数，格式示例：85,90,78"
    # 把网页session里的历史传给RAG
    return rag_answer_with_memory(user_input, history)

# 控制台单独运行时的全局历史（保留原来终端交互功能）
if __name__ == "__main__":
    conversation_history = []

    def chat_with_memory(user_input):
        # 全局变量声明，替换原来的 nonlocal
        global conversation_history
        conversation_history.append({"role": "user", "content": user_input})
        reply = agent_chat(user_input, conversation_history)
        conversation_history.append({"role": "assistant", "content": reply})
        return reply

    print("===== 安徽交职院校园百事通智能助手（带工具+多轮记忆）=====")
    print("支持功能：查询校历周数、绩点计算、校园规则问答\n输入quit退出对话\n")
    while True:
        user_msg = input("你：")
        if user_msg.strip().lower() == "quit":
            print("助手：感谢使用，再见！")
            break
        res = chat_with_memory(user_msg)
        print(f"助手：{res}\n")