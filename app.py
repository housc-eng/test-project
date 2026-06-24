# src/app.py
import streamlit as st
import random
import json
from datetime import datetime
import pandas as pd

# 导入 agent
try:
    from agent import agent_chat
except ImportError:
    def agent_chat(query, history):
        return f"🤖 收到你的问题：{query}\n\n💡 提示：请确保 agent.py 文件存在并正确配置。"

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="校园生活百事通",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定义CSS ====================
st.markdown("""
<style>
    /* ===== 全局 ===== */
    * { font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif; }
    .stApp { background: #f0f2f6; }
    
    /* ===== 标题 ===== */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.35);
    }
    .main-header h1 {
        color: #fff !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }
    .main-header p {
        color: rgba(255,255,255,0.9) !important;
        font-size: 1rem !important;
        margin: 0.2rem 0 0 0 !important;
    }
    .main-header .badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 0.15rem 1rem;
        border-radius: 20px;
        font-size: 0.7rem;
        color: #fff;
        margin-top: 0.3rem;
    }
    
    /* ===== 欢迎卡片 ===== */
    .welcome-card {
        background: #fff;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    .welcome-card .big-emoji { font-size: 3.5rem; }
    .welcome-card h3 { color: #333; font-size: 1.4rem; }
    .welcome-card p { color: #888; font-size: 0.95rem; }
    .welcome-card .tags {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.5rem;
        margin: 0.8rem 0;
    }
    .welcome-card .tag {
        background: #f0f2f6;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        color: #555;
    }
    
    /* ===== 消息样式 ===== */
    .stChatMessage {
        animation: fadeIn 0.3s ease-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    [data-testid="stChatMessage"][role="user"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #fff !important;
        border-radius: 18px 18px 4px 18px !important;
        padding: 0.7rem 1.2rem !important;
        margin: 0.3rem 0 0.6rem auto !important;
        max-width: 80% !important;
        box-shadow: 0 4px 15px rgba(102,126,234,0.25);
    }
    [data-testid="stChatMessage"][role="user"] p { color: #fff !important; }
    [data-testid="stChatMessage"][role="assistant"] {
        background: #fff;
        border-radius: 18px 18px 18px 4px !important;
        padding: 0.7rem 1.2rem !important;
        margin: 0.3rem 0 0.6rem 0 !important;
        max-width: 85% !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid rgba(102,126,234,0.08);
    }
    
    /* ===== 输入框 ===== */
    .stChatInput input {
        border-radius: 30px !important;
        border: 2px solid #e8ecf4 !important;
        padding: 12px 24px !important;
        font-size: 1rem !important;
        background: #fff !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    }
    .stChatInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102,126,234,0.12) !important;
    }
    
    /* ===== 侧边栏 ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fe 0%, #eef1f9 100%);
        border-right: 1px solid rgba(102,126,234,0.1);
    }
    [data-testid="stSidebar"] .stMarkdown h3 { color: #4a4a6a; font-weight: 600; }
    
    /* ===== 统计卡片 ===== */
    .stat-cards {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.5rem;
        margin: 0.5rem 0;
    }
    .stat-card {
        background: #fff;
        border-radius: 12px;
        padding: 0.6rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .stat-card .num { font-size: 1.2rem; font-weight: 700; color: #667eea; }
    .stat-card .label { font-size: 0.65rem; color: #999; }
    
    /* ===== 按钮 ===== */
    .stButton button {
        border-radius: 30px !important;
        transition: all 0.2s ease !important;
        font-weight: 500 !important;
    }
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102,126,234,0.25) !important;
    }
    
    /* ===== 功能卡片 ===== */
    .func-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.5rem;
        margin: 0.5rem 0;
    }
    .func-item {
        background: #fff;
        border-radius: 12px;
        padding: 0.5rem 0.8rem;
        text-align: center;
        border: 1px solid #e8ecf4;
        transition: all 0.2s ease;
        cursor: pointer;
        font-size: 0.85rem;
    }
    .func-item:hover {
        border-color: #667eea;
        box-shadow: 0 2px 12px rgba(102,126,234,0.12);
        transform: translateY(-1px);
    }
    .func-item .icon { font-size: 1.2rem; display: block; }
    
    /* ===== 页脚 ===== */
    .footer {
        text-align: center;
        padding: 1rem 0 0.3rem;
        color: #bbb;
        font-size: 0.75rem;
        border-top: 1px solid rgba(0,0,0,0.04);
        margin-top: 1rem;
    }
    .footer .heart { color: #e74c6f; }
</style>
""", unsafe_allow_html=True)

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("### 🏫 校园百事通")
    st.caption(f"📅 {datetime.now().strftime('%Y年%m月%d日')}")
    st.divider()
    
    # === 快速工具 ===
    with st.expander("🛠️ 快速工具", expanded=True):
        tool_col1, tool_col2 = st.columns(2)
        with tool_col1:
            if st.button("📊 绩点计算器", use_container_width=True):
                st.session_state.show_tool = "gpa"
        with tool_col2:
            if st.button("📅 校历查询", use_container_width=True):
                st.session_state.show_tool = "calendar"
    
    st.divider()
    
    # === 热门问题 ===
    with st.expander("⭐ 热门问题", expanded=True):
        quick_questions = [
            ("📋 怎么请假？", "怎么请假？"),
            ("🏆 奖学金条件？", "奖学金需要什么条件？"),
            ("🔧 宿舍报修？", "宿舍怎么报修？"),
            ("💳 一卡通丢了？", "一卡通丢了怎么办？"),
            ("📚 选课时间？", "选课什么时候开始？"),
        ]
        for label, q in quick_questions:
            if st.button(label, key=f"q_{q[:10]}", use_container_width=True):
                st.session_state.quick_question = q
    
    st.divider()
    
    # === 对话统计 ===
    if "messages" in st.session_state:
        total = len(st.session_state.messages)
        user_msgs = sum(1 for m in st.session_state.messages if m["role"] == "user")
        st.markdown(f"""
        <div class="stat-cards">
            <div class="stat-card"><div class="num">{total}</div><div class="label">总消息</div></div>
            <div class="stat-card"><div class="num">{user_msgs}</div><div class="label">已提问</div></div>
            <div class="stat-card"><div class="num">{total - user_msgs}</div><div class="label">回复数</div></div>
        </div>
        """, unsafe_allow_html=True)
    
    # === 控制按钮 ===
    col_clear, col_export = st.columns(2)
    with col_clear:
        if st.button("🗑️ 清空", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col_export:
        if st.button("📥 导出", use_container_width=True):
            if "messages" in st.session_state and st.session_state.messages:
                st.session_state.export_dialog = True
    
    st.divider()
    st.caption("⚡ v3.0 · RAG + DeepSeek")

# ==================== 导出对话 ====================
if st.session_state.get("export_dialog", False):
    with st.expander("📥 导出对话记录", expanded=True):
        msgs = st.session_state.messages
        text = f"校园百事通对话记录\n{datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        text += "=" * 40 + "\n"
        for m in msgs:
            role = "👤 用户" if m["role"] == "user" else "🤖 助手"
            text += f"{role}: {m['content']}\n\n"
        st.download_button(
            label="📥 下载对话记录",
            data=text,
            file_name=f"对话记录_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )
        if st.button("关闭", use_container_width=True):
            st.session_state.export_dialog = False
            st.rerun()

# ==================== 主内容 ====================
st.markdown("""
<div class="main-header">
    <h1>🏫 校园生活百事通</h1>
    <p>🤖 AI 智能助手 · 校园问题一站式解答</p>
    <span class="badge">✨ 支持 RAG 检索 · 多轮对话</span>
</div>
""", unsafe_allow_html=True)

# ==================== 初始化 ====================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "quick_question" not in st.session_state:
    st.session_state.quick_question = None
if "show_tool" not in st.session_state:
    st.session_state.show_tool = None

# ==================== 工具功能 ====================
if st.session_state.show_tool == "gpa":
    st.session_state.show_tool = None
    with st.chat_message("assistant"):
        st.markdown("### 📊 绩点计算器")
        col1, col2 = st.columns([2, 1])
        with col1:
            scores_input = st.text_input("请输入各科成绩（英文逗号分隔）", placeholder="85,90,78")
        with col2:
            if st.button("计算绩点"):
                if scores_input:
                    try:
                        from tools import calculate_gpa
                        result = calculate_gpa(scores_input)
                        st.success(result)
                    except Exception as e:
                        st.error(f"计算失败：{e}")
                else:
                    st.warning("请输入成绩")

if st.session_state.show_tool == "calendar":
    st.session_state.show_tool = None
    with st.chat_message("assistant"):
        st.markdown("### 📅 校历查询")
        from tools import get_current_week
        st.info(get_current_week())
        st.caption("校历起始日：2026年3月1日（第1周）")

# ==================== 快捷问题处理 ====================
if st.session_state.quick_question:
    q = st.session_state.quick_question
    st.session_state.quick_question = None
    st.session_state.messages.append({"role": "user", "content": q})
    with st.chat_message("user"):
        st.markdown(q)
    with st.chat_message("assistant"):
        with st.spinner("🤔 思考中..."):
            response = agent_chat(q, st.session_state.messages)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# ==================== 消息显示 ====================
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <div class="big-emoji">👋</div>
        <h3>欢迎来到校园生活百事通！</h3>
        <p>我是你的 AI 校园助手，可以帮你解答各类校园生活问题</p>
        <div class="tags">
            <span class="tag">📋 请假</span>
            <span class="tag">🎓 奖学金</span>
            <span class="tag">🔧 报修</span>
            <span class="tag">💳 一卡通</span>
            <span class="tag">📚 选课</span>
            <span class="tag">📊 绩点</span>
            <span class="tag">📅 校历</span>
        </div>
        <p style="font-size:0.8rem; color:#bbb; margin-top:0.5rem;">
            💡 在下方输入问题 · 侧边栏有快捷入口
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ==================== 输入区域 ====================
if prompt := st.chat_input("💬 输入你的校园问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("🤔 AI 正在思考..."):
            try:
                response = agent_chat(prompt, st.session_state.messages)
            except Exception as e:
                response = f"❌ 出错了：{str(e)}"
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# ==================== 页脚 ====================
st.markdown("""
<div class="footer">
    🏫 安徽交通职业技术学院 · 人工智能应用技术开发<br>
    <span class="heart">❤</span> 基于 LangChain + DeepSeek RAG <span class="heart">❤</span>
</div>
""", unsafe_allow_html=True)