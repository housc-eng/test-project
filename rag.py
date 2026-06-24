# src/rag.py
from openai import OpenAI
import os
from dotenv import load_dotenv
# 1. 导入向量库、嵌入模型（复用test_retrieve.py路径逻辑）
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
# 2. 导入预设提示词模板
from prompt_templates import RAG_PROMPT

# ---------------------- 1. 加载环境变量、DeepSeek客户端 ----------------------
load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# ---------------------- 2. 加载向量库（和build_vector_db/test_retrieve完全统一路径） ----------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
vector_save_path = os.path.join(script_dir, "..", "vector_db")
model_cache = os.path.join(script_dir, "..", "model_cache")

# 初始化嵌入模型（和构建向量库参数保持一致）
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh",
    cache_folder=model_cache,
    model_kwargs={"trust_remote_code": True},
    encode_kwargs={"normalize_embeddings": True}
)

# 加载本地持久化向量库
vector_db = Chroma(
    persist_directory=vector_save_path,
    embedding_function=embeddings
)

# ---------------------- 3. 标准RAG问答函数（符合实训要求） ----------------------
def rag_answer(question):
    # 步骤1：向量库检索top3相关知识库片段
    docs = vector_db.similarity_search(question, k=3)
    # 拼接检索到的上下文
    context = "\n\n".join([d.page_content for d in docs])
    # 步骤2：填充预设提示词模板
    prompt = RAG_PROMPT.format(context=context, question=question)
    # 步骤3：调用DeepSeek大模型生成回答
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

# ---------------------- 4. 实训5条测试用例（对应步骤3测试要求） ----------------------
if __name__ == "__main__":
    test_questions = [
        "怎么请病假？",
        "奖学金要多少绩点？",
        "宿舍灯坏了找谁？",
        "一卡通丢了怎么办？",
        "选错了课能退吗？"
    ]
    print("===== 开始RAG实训测试 =====\n")
    for idx, q in enumerate(test_questions, 1):
        print(f"【测试问题{idx}】{q}")
        ans = rag_answer(q)
        print(f"【模型回答】{ans}\n" + "-"*60 + "\n")
        # ========== 新增导出语句，放在文件最末尾 ==========
__all__ = ["vector_db", "client", "RAG_PROMPT", "rag_answer"]