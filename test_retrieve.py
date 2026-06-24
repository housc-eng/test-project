# src/test_retrieve.py
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# ========== 1. 自动匹配路径，和build_vector_db保持一致 ==========
script_dir = os.path.dirname(os.path.abspath(__file__))
# 向量库存放路径，和构建脚本完全对应
vector_save_path = os.path.join(script_dir, "..", "vector_db")
# 模型缓存路径
model_cache = os.path.join(script_dir, "..", "model_cache")

# ========== 2. 加载和构建时完全相同的嵌入模型 ==========
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh",
    cache_folder=model_cache,
    model_kwargs={"trust_remote_code": True},
    encode_kwargs={"normalize_embeddings": True}
)

# ========== 3. 读取本地持久化的向量库 ==========
vector_db = Chroma(
    persist_directory=vector_save_path,
    embedding_function=embeddings
)

# ========== 4. 检索函数（实训指导书原版逻辑） ==========
def search_knowledge(query):
    results = vector_db.similarity_search(query, k=3)
    for r in results:
        print(f"相关元数据: {r.metadata}")
        print(f"知识库内容: {r.page_content}\n")
    return results

# ========== 5. 测试入口，仅直接运行本文件时执行 ==========
if __name__ == "__main__":
    print("===== ✅开始检索“请假相关手续？”=====")
    search_knowledge("请假相关手续")
    print("===== ✅开始检索“校园WiFi怎么连接？”=====")
    search_knowledge("校园WiFi怎么连接？")
    print("===== ✅开始检索“宿舍东西坏了怎么办？”=====")
    search_knowledge("宿舍东西坏了怎么办？")
    print("===== ✅开始检索“国家助学金发放时间？”=====")
    search_knowledge("国家助学金发放时间")