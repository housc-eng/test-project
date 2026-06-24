# src/build_vector_db.py
import pandas as pd
import os

# ========== 自动计算文件路径，解决相对路径找不到文件的核心问题 ==========
# 获取当前脚本 build_vector_db.py 所在文件夹 src
script_dir = os.path.dirname(os.path.abspath(__file__))
# 拼接csv完整路径：src上层ai_course_project下的data文件夹
csv_path = os.path.join(script_dir, "..", "data", "campus_data.csv")
# 向量库存放路径：ai_course_project/vector_db
vector_save_path = os.path.join(script_dir, "..", "vector_db")

# 导入依赖
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("开始加载校园问答CSV数据...")
# 加载CSV
df = pd.read_csv(csv_path)
print(f"成功读取 {len(df)} 条校园问答数据")

# 加载本地中文嵌入模型
print("正在加载BGE-small-zh嵌入模型...")
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh",
    model_kwargs={"trust_remote_code": True},
    # 国内hf镜像，解决连接超时
    cache_folder="./model_cache",
    encode_kwargs={"normalize_embeddings": True}
)

# 拆分文本与元数据
texts = df['answer'].tolist()
metadatas = df[['id', 'category', 'question']].to_dict('records')

print(f"开始向量化 {len(texts)} 条问答记录...")
# 构建并持久化向量库
vector_db = Chroma.from_texts(
    texts=texts,
    embedding=embeddings,
    metadatas=metadatas,
    persist_directory=vector_save_path
)
vector_db.persist()

print(f"✅ 向量库构建完成，共存入{len(texts)}条记录")
print(f"📁 向量库文件保存路径：{vector_save_path}")