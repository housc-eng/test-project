# src/app.py
import streamlit as st
import random
import json
from datetime import datetime
import pandas as pd
import hashlib
import time


# ==================== 用户数据（模拟数据库） ====================
USERS = {
    "admin": {
        "password": "e10adc3949ba59abbe56e057f20f883e",  # md5: 123456
        "name": "管理员",
        "role": "管理员",
        "avatar": "👤"
    },
    "student": {
        "password": "e10adc3949ba59abbe56e057f20f883e",
        "name": "张同学",
        "role": "学生端",
        "avatar": "🎓"
    },
    "teacher": {
        "password": "e10adc3949ba59abbe56e057f20f883e",
        "name": "李老师",
        "role": "教师端",
        "avatar": "👨‍🏫"
    }
}

def md5_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def check_login(username, password):
    if username in USERS:
        if USERS[username]["password"] == md5_hash(password):
            return True, USERS[username]
    return False, None

# ==================== 导入 agent ====================
try:
    from agent import agent_chat
except ImportError:
    def agent_chat(query, history):
        return f"🤖 收到你的问题：{query}\n\n💡 提示：请确保 agent.py 文件存在并正确配置。"

# ==================== 登录页面 ====================
def login_page():
    # ===== 登录页面CSS - 完全重构 =====
    st.markdown("""
    <style>
        /* ===== 全局重置 ===== */
        .stApp {
            background: linear-gradient(145deg, #eef1f5 0%, #dce1ea 100%) !important;
        }
        
        /* ===== 隐藏所有默认元素 ===== */
        .stApp > header { display: none !important; }
        #MainMenu { display: none !important; }
        .stAppDeployButton { display: none !important; }
        footer { display: none !important; }
        .st-emotion-cache-1r6slb0 { display: none !important; }
        .st-emotion-cache-1wivap2 { display: none !important; }
        .st-emotion-cache-1v3ca8y { display: none !important; }
        .st-emotion-cache-16txtl3 { display: none !important; }
        .stChatInput { display: none !important; }
        
        /* ===== 主容器 - 完全居中且无空白 ===== */
        .main .block-container {
            padding: 0px !important;
            max-width: 480px !important;
            margin-left: auto !important;
            margin-right: auto !important;
            display: flex !important;
            align-items: center !important;
            min-height: 100vh !important;
        } 
        /* ===== Logo ===== */
        .login-logo {
            text-align: center;
            margin-bottom: 4px;
        }
        .login-logo .icon-box {
            display: inline-block;
            background: linear-gradient(135deg, #4A6CF7, #6A3DE8);
            border-radius: 14px;
            padding: 6px 10px;
            margin-bottom: 4px;
            box-shadow: 0 4px 16px rgba(74, 108, 247, 0.18);
        }
        .login-logo .icon-box span { font-size: 22px; }
        .login-logo .title {
            font-size: 20px;
            font-weight: 700;
            color: #1a1a2e;
            margin: 0;
            letter-spacing: -0.5px;
        }
        .login-logo .title .hl { color: #1a1a2e; }
        
        /* ===== Slogan ===== */
        .slogan {
            text-align: center;
            margin-bottom: 10px;
            padding: 6px 8px;
            background: linear-gradient(135deg, rgba(74, 108, 247, 0.04), rgba(106, 61, 232, 0.04));
            border-radius: 10px;
            border: 1px solid rgba(74, 108, 247, 0.06);
        }
        .slogan .main-text {
            font-size: 13px;
            font-weight: 600;
            color: #1a1a2e;
        }
        .slogan .sub-text {
            font-size: 10px;
            color: #9a9aaa;
            margin-top: 1px;
        }
        
        /* ===== 欢迎文字 ===== */
        .welcome-text {
            text-align: center;
            margin: 8px 0 12px;
        }
        .welcome-text h2 {
            font-size: 16px;
            font-weight: 600;
            color: #1a1a2e;
            margin: 0;
        }
        .welcome-text p {
            font-size: 12px;
            color: #9a9aaa;
            margin: 2px 0 0;
        }
        
        /* ===== 快速选择角色 ===== */
        .role-section {
            margin-bottom: 12px;
        }
        .role-section .label {
            font-size: 10px;
            color: #b0b0c0;
            text-align: center;
            margin-bottom: 6px;
            letter-spacing: 0.5px;
        }
        .role-grid {
            display: flex;
            gap: 8px;
        }
        .role-item {
            flex: 1;
            background: #f5f6fa;
            border: 2px solid transparent;
            border-radius: 10px;
            padding: 8px 4px;
            text-align: center;
            transition: all 0.3s ease;
        }
        .role-item:hover {
            background: #eef0f7;
            border-color: #4A6CF7;
            transform: translateY(-2px);
        }
        .role-item .emoji { font-size: 20px; display: block; }
        .role-item .name {
            font-size: 11px;
            color: #4a4a5a;
            font-weight: 500;
        }
        .role-item .code {
            font-size: 9px;
            color: #aaa;
            background: rgba(0,0,0,0.03);
            padding: 1px 8px;
            border-radius: 4px;
            display: inline-block;
            margin-top: 1px;
        }
        
        /* ===== 隐藏输入框标签 ===== */
        .stTextInput label { display: none !important; }
        .stTextInput .st-emotion-cache-1y4p8pa { display: none !important; }
        .stTextInput .st-emotion-cache-1x8cf4d { display: none !important; }
        .stTextInput > div { padding: 0 !important; margin: 0 !important; }
        .stTextInput > div > div { padding: 0 !important; margin: 0 !important; }
        
        /* ===== 输入框样式 ===== */
        .stTextInput input {
            margin: 0 !important;
            padding: 10px 14px !important;
            font-size: 14px !important;
            border-radius: 10px !important;
            border: 2px solid #e8ecf4 !important;
            background: #f8f9fc !important;
            transition: border-color 0.3s ease;
            width: 100% !important;
            box-sizing: border-box !important;
        }
        .stTextInput input:focus {
            border-color: #4A6CF7 !important;
            box-shadow: 0 0 0 3px rgba(74, 108, 247, 0.08) !important;
            outline: none !important;
            background: #ffffff !important;
        }
        .stTextInput input::placeholder {
            color: #b8b8c8;
        }
        
        /* ===== 登录按钮 ===== */
        .stButton button {
            width: 100% !important;
            padding: 12px !important;
            border: none !important;
            border-radius: 10px !important;
            background: linear-gradient(135deg, #4A6CF7, #6A3DE8) !important;
            color: #fff !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 16px rgba(74, 108, 247, 0.2) !important;
            transition: all 0.3s ease !important;
            margin-top: 6px !important;
            letter-spacing: 0.5px;
        }
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 30px rgba(74, 108, 247, 0.3) !important;
        }
        
        /* ===== 错误信息 ===== */
        .error-msg {
            background: rgba(239, 68, 68, 0.05);
            border: 1px solid rgba(239, 68, 68, 0.1);
            color: #dc2626;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 12px;
            margin-bottom: 10px;
            text-align: center;
        }
        
        /* ===== 功能列表 ===== */
        .features {
            display: flex;
            gap: 6px;
            margin: 12px 0 6px;
        }
        .features .item {
            flex: 1;
            font-size: 10px;
            color: #8a8a9a;
            text-align: center;
            padding: 6px 4px;
            background: #f8f9fc;
            border-radius: 8px;
            border: 1px solid #f0f2f6;
        }
        .features .item .icon { margin-right: 2px; }
        
        /* ===== 注册链接 ===== */
        .register-link {
            text-align: center;
            font-size: 12px;
            color: #8a8a9a;
            margin-top: 8px;
            padding-top: 8px;
            border-top: 1px solid #f0f0f5;
        }
        .register-link a {
            color: #4A6CF7;
            text-decoration: none;
            font-weight: 500;
        }
        
        /* ===== 底部提示 ===== */
        .demo-tip {
            text-align: center;
            font-size: 10px;
            color: #b8b8c8;
            margin-top: 6px;
            line-height: 1.8;
        }
        .demo-tip code {
            background: rgba(74, 108, 247, 0.06);
            padding: 1px 6px;
            border-radius: 4px;
            font-size: 10px;
            color: #4A6CF7;
        }
        .demo-tip .sep {
            color: #d0d0d8;
            margin: 0 3px;
        }
        
        /* ===== 响应式 ===== */
        @media (max-width: 480px) {
            .login-card { padding: 20px 14px 16px; }
            .login-logo .title { font-size: 17px; }
            .login-logo .icon-box span { font-size: 18px; }
            .slogan .main-text { font-size: 12px; }
            .welcome-text h2 { font-size: 15px; }
            .welcome-text p { font-size: 11px; }
            .role-item .emoji { font-size: 17px; }
            .role-item .name { font-size: 10px; }
            .stTextInput input { padding: 8px 12px !important; font-size: 13px !important; }
            .features .item { font-size: 9px; }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # ===== 单个白色卡片 - 包含所有内容 =====
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # Slogan
    st.markdown("""
    <div class="slogan">
        <div class="main-header">
            <h1>🏫 <span class="highlight">校园生活百事通</span></h1>
        </div>
        <div class="main-text">✨ 智慧校园 · AI赋能 · 便捷生活</div>
        <div class="sub-text">AI 智能校园助手 · 一站式解答</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 欢迎文字
    st.markdown("""
    <div class="welcome-text">
        <h2>欢迎登录</h2>
        <p>请输入您的账号和密码</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 快速选择角色
    st.markdown('<div class="role-section"><div class="label">— 快速选择角色 —</div><div class="role-grid">', unsafe_allow_html=True)
    
    cols = st.columns(3)
    quick_users = [
        ("👤", "管理员", "admin"),
        ("🎓", "学生端", "student"),
        ("👨‍🏫", "教师端", "teacher"),
    ]
    for idx, (emoji, name, username) in enumerate(quick_users):
        with cols[idx]:
            if st.button(f"{emoji}\n{name}", key=f"role_{username}", use_container_width=True):
                st.session_state.login_username = username
                st.session_state.login_password = "123456"
                st.rerun()
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # 错误信息
    if st.session_state.get("login_error"):
        st.markdown(f'<div class="error-msg">❌ {st.session_state.login_error}</div>', unsafe_allow_html=True)
        st.session_state.login_error = None
    
    # ✅ 修复：使用 label 参数，而不是 label_visibility
    username = st.text_input(
        "用户名",
        value=st.session_state.get("login_username", ""),
        placeholder="请输入用户名",
        key="login_username_input"
    )
    
    # ✅ 修复：使用 label 参数，而不是 label_visibility
    password = st.text_input(
        "密码",
        value=st.session_state.get("login_password", ""),
        placeholder="请输入密码 (默认: 123456)",
        type="password",
        key="login_password_input"
    )
    
    # 登录按钮
    if st.button("🚀 登 录", key="login_btn", use_container_width=True):
        if username and password:
            success, user_info = check_login(username, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_info = user_info
                st.session_state.login_error = None
                st.rerun()
            else:
                st.session_state.login_error = "用户名或密码错误，请重新输入"
                st.rerun()
        else:
            st.session_state.login_error = "请输入用户名和密码"
            st.rerun()
    
    # 功能列表
    st.markdown("""
    <div class="features">
        <div class="item"><span class="icon">💬</span>AI智能问答</div>
        <div class="item"><span class="icon">🔄</span>多轮对话</div>
        <div class="item"><span class="icon">📚</span>知识库检索</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 注册链接
    st.markdown("""
    <div class="register-link">
        还没有账号？<a href="#">立即注册</a>
    </div>
    """, unsafe_allow_html=True)
    
    # 底部提示
    st.markdown("""
    <div class="demo-tip">
        💡 演示账号：<code>admin</code> <span class="sep">·</span> <code>123456</code>
        <span class="sep">｜</span>
        <code>student</code> <span class="sep">·</span> <code>123456</code>
        <span class="sep">｜</span>
        <code>teacher</code> <span class="sep">·</span> <code>123456</code>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


# ==================== 主应用 ====================
def main_app():
    # ===== 主应用CSS =====
    st.markdown("""
    <style>
        * { font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif; }
        .stApp { background: #f0f2f6; }
        
        .main .block-container {
            max-width: 100% !important;
            padding: 0.5rem 2rem 120px 2rem !important;
            transition: all 0.3s ease !important;
        }
        
        /* ===== 侧边栏 ===== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8f9fe 0%, #eef1f9 100%);
            border-right: 1px solid rgba(102,126,234,0.08);
            padding: 0 !important;
            width: 280px !important;
            min-width: 280px !important;
            transition: all 0.3s ease !important;
        }
        [data-testid="stSidebar"] > div { padding: 0.5rem 0.6rem !important; }
        [data-testid="stSidebar"][aria-expanded="true"] {
            width: 280px !important;
            min-width: 280px !important;
        }
        [data-testid="stSidebar"][aria-expanded="false"] {
            width: 0px !important;
            min-width: 0px !important;
            overflow: hidden !important;
            border-right: none !important;
            padding: 0 !important;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div { display: none !important; }
        
        /* ===== 侧边栏标题样式 ===== */
        .sidebar-title {
            font-size: 0.85rem;
            font-weight: 700;
            padding: 0.3rem 0.3rem 0.5rem;
            border-bottom: 1px solid rgba(102,126,234,0.08);
            margin-bottom: 0.5rem;
        }
        .sidebar-title span {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* ===== 添加新对话按钮 ===== */
        .new-conversation-btn {
            width: 100% !important;
            margin-bottom: 0.5rem !important;
        }
        .new-conversation-btn button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: #fff !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.6rem 0.8rem !important;
            font-weight: 600 !important;
            font-size: 0.8rem !important;
            width: 100% !important;
            transition: all 0.3s ease !important;
            cursor: pointer !important;
            box-shadow: 0 2px 12px rgba(102,126,234,0.15) !important;
        }
        .new-conversation-btn button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 24px rgba(102,126,234,0.25) !important;
        }
        
        /* ===== 用户信息双列按钮 ===== */
        .user-info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px;
            margin-bottom: 0.5rem;
        }
        .user-info-grid .stButton {
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
        }
        .user-info-grid .stButton button {
            border-radius: 10px !important;
            padding: 0.5rem 0.3rem !important;
            font-size: 0.7rem !important;
            font-weight: 500 !important;
            width: 100% !important;
            height: auto !important;
            min-height: 44px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 4px !important;
            transition: all 0.25s ease !important;
            box-shadow: none !important;
            border: 1px solid rgba(102,126,234,0.08) !important;
        }
        .user-info-grid .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 16px rgba(102,126,234,0.10) !important;
        }
        .user-info-grid .stButton:first-child button {
            background: rgba(102,126,234,0.08) !important;
            color: #4a4a6a !important;
            border-color: rgba(102,126,234,0.12) !important;
        }
        .user-info-grid .stButton:last-child button {
            background: rgba(239, 68, 68, 0.06) !important;
            color: #b91c1c !important;
            border-color: rgba(239, 68, 68, 0.1) !important;
        }
        .user-info-grid .stButton:last-child button:hover {
            background: rgba(239, 68, 68, 0.12) !important;
            border-color: rgba(239, 68, 68, 0.2) !important;
        }
        
        /* ===== 用户信息提示框 ===== */
        .user-info-toast {
            background: rgba(255,255,255,0.95) !important;
            border-radius: 12px !important;
            padding: 0.8rem 1rem !important;
            margin-bottom: 0.5rem !important;
            border: 1px solid rgba(102,126,234,0.15) !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06) !important;
            animation: fadeInUp 0.3s ease-out !important;
        }
        .user-info-toast .label {
            font-size: 0.65rem !important;
            color: #999 !important;
            font-weight: 500 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }
        .user-info-toast .value {
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            color: #2d3436 !important;
            margin-top: 2px !important;
        }
        .user-info-toast .value .highlight {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* ===== 历史对话列表 ===== */
        .history-item {
            padding: 0.4rem 0.6rem;
            margin: 0.2rem 0;
            border-radius: 8px;
            background: rgba(255,255,255,0.5);
            border: 1px solid rgba(102,126,234,0.06);
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 0.7rem;
            color: #4a4a6a;
        }
        .history-item:hover {
            background: rgba(102,126,234,0.08);
            border-color: rgba(102,126,234,0.15);
        }
        .history-item .time {
            font-size: 0.55rem;
            color: #999;
            margin-left: 0.3rem;
        }
        
        /* ===== 服务图标网格 ===== */
        .service-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px;
            margin: 0 0 0.3rem 0;
        }
        .service-grid .stButton {
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
        }
        .service-grid .stButton button {
            background: rgba(255,255,255,0.7) !important;
            border: 1px solid rgba(102,126,234,0.06) !important;
            border-radius: 10px !important;
            padding: 0.6rem 0.2rem !important;
            text-align: center !important;
            font-size: 0.7rem !important;
            color: #4a4a6a !important;
            font-weight: 500 !important;
            width: 100% !important;
            height: auto !important;
            min-height: 60px !important;
            line-height: 1.3 !important;
            box-shadow: none !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.25s ease !important;
            white-space: normal !important;
            word-wrap: break-word !important;
            cursor: pointer !important;
        }
        .service-grid .stButton button:hover {
            background: rgba(102,126,234,0.08) !important;
            border-color: rgba(102,126,234,0.2) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 16px rgba(102,126,234,0.10) !important;
        }
        .service-grid .stButton button .icon {
            font-size: 1.3rem;
            margin-bottom: 2px;
        }
        
        .sidebar-logo {
            text-align: center;
            padding: 0.6rem 0 0.4rem;
            border-bottom: 1px solid rgba(102,126,234,0.06);
            margin-bottom: 0.3rem;
        }
        .sidebar-logo .icon { font-size: 2rem; }
        .sidebar-logo .title {
            font-size: 1rem;
            font-weight: 700;
            color: #4a4a6a;
            margin: 0.1rem 0 0;
        }
        .sidebar-logo .title span {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .sidebar-logo .sub {
            font-size: 0.5rem;
            color: #bbb;
            letter-spacing: 1px;
        }
        
        .main-header {
            background: transparent !important;
            padding: 0.5rem 0 1rem !important;
            border-radius: 0 !important;
            margin-bottom: 0.8rem !important;
            box-shadow: none !important;
            text-align: center !important;
        }
        .main-header h1 {
            color: #2d3436 !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            margin: 0 !important;
            text-shadow: none !important;
            letter-spacing: -0.3px;
        }
        .main-header h1 .highlight {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .main-header p {
            color: #6b7280 !important;
            font-size: 0.85rem !important;
            margin: 0.1rem 0 0 0 !important;
        }
        .main-header .badge {
            display: inline-block;
            background: rgba(102,126,234,0.06);
            padding: 0.1rem 0.8rem;
            border-radius: 16px;
            font-size: 0.55rem;
            color: #667eea;
            margin-top: 0.2rem;
            border: 1px solid rgba(102,126,234,0.08);
        }
        
        .right-module { max-width: 280px !important; margin-left: auto !important; }
        
        .welcome-card {
            background: #fff;
            border-radius: 16px;
            padding: 1.2rem 1.5rem;
            text-align: center;
            box-shadow: 0 4px 16px rgba(0,0,0,0.04);
            border: 1px solid rgba(102,126,234,0.06);
            max-width: 900px;
            margin: 0 auto;
        }
        .welcome-card .big-emoji { font-size: 2.5rem; }
        .welcome-card h3 { color: #333; font-size: 1.1rem; margin: 0.2rem 0; }
        .welcome-card p { color: #888; font-size: 0.8rem; margin: 0.2rem 0; }
        .welcome-card .tags {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 0.4rem;
            margin: 0.5rem 0;
        }
        .welcome-card .tag {
            background: #f0f2f6;
            padding: 0.2rem 0.7rem;
            border-radius: 16px;
            font-size: 0.65rem;
            color: #555;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .welcome-card .tag:hover {
            background: #667eea;
            color: #fff;
            transform: translateY(-2px);
        }
        
        .stChatMessage { animation: fadeIn 0.3s ease-out; }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        [data-testid="stChatMessage"][role="user"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff !important;
            border-radius: 16px 16px 4px 16px !important;
            padding: 0.6rem 1.2rem !important;
            margin: 0.2rem 0 0.5rem auto !important;
            max-width: 75% !important;
            box-shadow: 0 4px 12px rgba(102,126,234,0.15);
        }
        [data-testid="stChatMessage"][role="user"] p { color: #fff !important; }
        [data-testid="stChatMessage"][role="assistant"] {
            background: #fff;
            border-radius: 16px 16px 16px 4px !important;
            padding: 0.6rem 1.2rem !important;
            margin: 0.2rem 0 0.5rem 0 !important;
            max-width: 82% !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            border: 1px solid rgba(102,126,234,0.06);
        }
        
        /* ===== 搜索输入框 ===== */
        .stChatInput {
            position: fixed !important;
            bottom: 24px !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
            width: calc(100% - 340px) !important;
            max-width: 700px !important;
            min-width: 320px !important;
            z-index: 9999 !important;
            background: transparent !important;
            padding: 0 !important;
            border: none !important;
            transition: width 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
        }
        
        [data-testid="stSidebar"][aria-expanded="false"] ~ .stChatInput {
            width: calc(100% - 80px) !important;
            max-width: 900px !important;
        }
        
        .stChatInput > div {
            background: rgba(255,255,255,0.92) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-radius: 50px !important;
            border: 1px solid rgba(255,255,255,0.3) !important;
            box-shadow: 0 8px 40px rgba(0,0,0,0.04), 0 2px 12px rgba(0,0,0,0.02), inset 0 1px 0 rgba(255,255,255,0.6) !important;
            padding: 4px !important;
            transition: all 0.35s ease !important;
        }
        .stChatInput > div:focus-within {
            border-color: rgba(102,126,234,0.15) !important;
            box-shadow: 0 16px 56px rgba(102,126,234,0.06) !important;
            background: rgba(255,255,255,0.96) !important;
        }
        .stChatInput input {
            border: none !important;
            background: transparent !important;
            padding: 12px 24px !important;
            font-size: 0.95rem !important;
            color: #333 !important;
            box-shadow: none !important;
            border-radius: 50px !important;
            caret-color: #667eea !important;
        }
        .stChatInput input::placeholder { color: #bbb !important; }
        .stChatInput input:focus { box-shadow: none !important; }
        .stChatInput .st-emotion-cache-1r6slb0,
        .stChatInput .st-emotion-cache-16txtl3 { display: none !important; }
        
        .main .block-container { padding-bottom: 120px !important; }
        
        .stButton button {
            border-radius: 30px !important;
            transition: all 0.25s ease !important;
            font-weight: 500 !important;
            font-size: 0.75rem !important;
            background: #fff !important;
            border: 1px solid rgba(102,126,234,0.08) !important;
            color: #4a4a6a !important;
        }
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(102,126,234,0.12) !important;
            border-color: rgba(102,126,234,0.15) !important;
        }
        
        .stat-cards {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.3rem;
            margin: 0.3rem 0;
        }
        .stat-card {
            background: rgba(255,255,255,0.7);
            border-radius: 8px;
            padding: 0.3rem;
            text-align: center;
            border: 1px solid rgba(102,126,234,0.04);
        }
        .stat-card .num { font-size: 0.95rem; font-weight: 700; color: #667eea; }
        .stat-card .label { font-size: 0.5rem; color: #999; }
        
        .footer {
            text-align: center;
            padding: 0.6rem 0 0.2rem;
            color: #ccc;
            font-size: 0.6rem;
            border-top: 1px solid rgba(0,0,0,0.03);
            margin-top: 0.6rem;
        }
        .footer .heart { color: #e74c6f; }
        
        @media (max-width: 768px) {
            .stChatInput {
                width: 92% !important;
                bottom: 16px !important;
                min-width: unset !important;
                left: 50% !important;
                transform: translateX(-50%) !important;
            }
            [data-testid="stSidebar"][aria-expanded="false"] ~ .stChatInput {
                width: 92% !important;
                max-width: 92% !important;
            }
            .stChatInput input { padding: 10px 18px !important; font-size: 0.85rem !important; }
            .main .block-container { padding-bottom: 100px !important; }
            .main-header h1 { font-size: 1.3rem !important; }
            .right-module { max-width: 100% !important; }
            [data-testid="stSidebar"] { width: 220px !important; min-width: 220px !important; }
            .service-grid { grid-template-columns: 1fr 1fr !important; gap: 4px !important; }
            .service-grid .stButton button { min-height: 50px !important; font-size: 0.6rem !important; padding: 0.4rem 0.2rem !important; }
            .service-grid .stButton button .icon { font-size: 1.1rem !important; }
            .user-info-grid { grid-template-columns: 1fr 1fr !important; gap: 4px !important; }
            .user-info-grid .stButton button { min-height: 38px !important; font-size: 0.6rem !important; padding: 0.3rem 0.2rem !important; }
        }
        
        @media (min-width: 769px) and (max-width: 1024px) {
            .stChatInput {
                width: calc(100% - 320px) !important;
                max-width: 600px !important;
            }
            [data-testid="stSidebar"][aria-expanded="false"] ~ .stChatInput {
                width: calc(100% - 60px) !important;
                max-width: 800px !important;
            }
        }
        
        @media (min-width: 1025px) {
            .stChatInput {
                width: calc(100% - 340px) !important;
                max-width: 700px !important;
            }
            [data-testid="stSidebar"][aria-expanded="false"] ~ .stChatInput {
                width: calc(100% - 80px) !important;
                max-width: 900px !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # ==================== 初始化会话状态 ====================
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    if "current_conversation" not in st.session_state:
        st.session_state.current_conversation = []
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = 0
    if "quick_question" not in st.session_state:
        st.session_state.quick_question = None
    if "show_tool" not in st.session_state:
        st.session_state.show_tool = None
    if "export_dialog" not in st.session_state:
        st.session_state.export_dialog = False
    if "new_conversation" not in st.session_state:
        st.session_state.new_conversation = False
    if "show_user_info" not in st.session_state:
        st.session_state.show_user_info = False
    if "user_info_timestamp" not in st.session_state:
        st.session_state.user_info_timestamp = 0

    # ==================== 工具函数 ====================
    try:
        from tools import calculate_gpa, get_current_week
    except ImportError:
        def calculate_gpa(scores_str):
            try:
                scores = [float(s.strip()) for s in scores_str.split(",") if s.strip()]
                avg = sum(scores) / len(scores)
                gpa = (avg - 60) / 10 if avg >= 60 else 0
                return f"✅ 平均分：{avg:.2f} | 换算绩点：{gpa:.2f}"
            except:
                return "❌ 成绩解析失败，请用英文逗号分隔"
        def get_current_week():
            now = datetime.now()
            start_day = datetime(2026, 3, 1)
            diff_days = (now - start_day).days
            week = diff_days // 7 + 1
            return f"📅 当前为学期第 {week} 周"
    
    # ==================== 智能建议 ====================
    def generate_suggestions(query):
        suggestions_map = {
            "请假": ["奖学金条件", "宿舍报修", "一卡通补办"],
            "奖学金": ["请假流程", "选课时间", "绩点计算"],
            "报修": ["一卡通补办", "请假流程", "食堂开放"],
            "一卡通": ["宿舍报修", "请假流程", "选课时间"],
            "选课": ["奖学金条件", "绩点计算", "校历查询"],
            "校历": ["选课时间", "绩点计算", "请假流程"],
            "绩点": ["选课时间", "奖学金条件", "校历查询"],
            "快递": ["食堂开放", "班车时刻", "图书馆规则"],
            "食堂": ["快递查询", "班车时刻", "一卡通补办"],
            "班车": ["食堂开放", "快递查询", "校历查询"],
            "图书馆": ["借阅规则", "开放时间", "选课时间"],
            "医保": ["请假流程", "校医院", "一卡通补办"],
        }
        for key, vals in suggestions_map.items():
            if key in query:
                return vals
        return ["怎么请假？", "奖学金条件？", "宿舍报修？", "一卡通丢了？", "选课时间？"]
    
    # ==================== 侧边栏 ====================
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <div class="icon">🏫</div>
            <div class="title"><span class="highlight">校园生活百事通</span></div>
            <div class="sub">AI 智能校园助手</div>
        </div>
        """, unsafe_allow_html=True)
        # ===== 用户信息双列按钮 =====
        user_info = st.session_state.get("user_info", {})
        
        # ===== 用户信息提示框（一列显示，3秒后自动消失） =====
        current_time = time.time()
        if st.session_state.show_user_info:
            if current_time - st.session_state.user_info_timestamp > 2:
                st.session_state.show_user_info = False
                st.rerun()
            else:
                st.markdown(f"""
                <div class="user-info-toast">
                    <div class="label">👤 当前用户</div>
                    <div class="value"><span class="highlight">{user_info.get('name', '用户')}</span></div>
                    <div class="label" style="margin-top:6px;">🎯 角色</div>
                    <div class="value">{user_info.get('role', '访客')}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('<div class="user-info-grid">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"👤 {user_info.get('name', '用户')} · {user_info.get('role', '访客')}", key="user_info_btn", use_container_width=True):
                st.session_state.show_user_info = not st.session_state.show_user_info
                if st.session_state.show_user_info:
                    st.session_state.user_info_timestamp = time.time()
                st.rerun()
        
        with col2:
            if st.button("🚪 退出登录", key="logout_btn_sidebar", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.user_info = None
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ===== 添加新对话按钮 =====
        st.markdown('<div class="new-conversation-btn">', unsafe_allow_html=True)
        if st.button("➕ 添加新对话", key="new_conversation_btn", use_container_width=True):
            if st.session_state.messages:
                conv_id = st.session_state.conversation_id + 1
                st.session_state.conversation_id = conv_id
                st.session_state.conversation_history.append({
                    "id": conv_id,
                    "title": st.session_state.messages[0]["content"][:30] + "..." if st.session_state.messages else "新对话",
                    "messages": st.session_state.messages.copy(),
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
            st.session_state.messages = []
            st.session_state.new_conversation = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ===== 历史对话列表 =====
        st.markdown('<div class="sidebar-title">📜 历史对话</div>', unsafe_allow_html=True)
        
        if st.session_state.conversation_history:
            for conv in reversed(st.session_state.conversation_history):
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button(f"💬 {conv['title']}", key=f"history_{conv['id']}", use_container_width=True):
                        st.session_state.messages = conv["messages"].copy()
                        st.rerun()
                with col2:
                    if st.button("🗑️", key=f"del_{conv['id']}"):
                        st.session_state.conversation_history = [c for c in st.session_state.conversation_history if c["id"] != conv["id"]]
                        st.rerun()
                st.caption(f"🕐 {conv['time']}")
        else:
            st.markdown('<p style="color:#bbb; font-size:0.7rem; text-align:center; padding:0.5rem 0;">暂无历史对话</p>', unsafe_allow_html=True)
        
        st.divider()
        
        # ===== 学生服务 =====
        st.markdown('<div class="sidebar-title"><span>📚 学生服务</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="service-grid">', unsafe_allow_html=True)
        student_services = [
            ("📋", "请假流程", "怎么请假？"),
            ("🏆", "奖学金申请", "奖学金需要什么条件？"),
            ("📚", "选课指南", "选课什么时候开始？"),
            ("📊", "绩点计算", "gpa_tool"),
            ("📝", "课表查看", "schedule_tool"),
            ("🎓", "毕业要求", "毕业需要什么条件？"),
        ]
        for icon, label, key in student_services:
            if st.button(f"{icon}\n{label}", key=f"stu_{key[:6]}", use_container_width=True):
                if key == "gpa_tool":
                    st.session_state.show_tool = "gpa"
                elif key == "schedule_tool":
                    st.session_state.show_tool = "schedule"
                else:
                    st.session_state.quick_question = key
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ===== 公共服务 =====
        st.markdown('<div class="sidebar-title"><span>🏛️ 公共服务</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="service-grid">', unsafe_allow_html=True)
        public_services = [
            ("📅", "校历查询", "calendar_tool"),
            ("💳", "一卡通补办", "一卡通丢了怎么办？"),
            ("🔧", "宿舍报修", "宿舍怎么报修？"),
            ("🏥", "医保报销", "医保怎么报销？"),
            ("📖", "图书馆规则", "图书馆借书规则？"),
            ("🚍", "班车时刻", "校园班车时刻表？"),
        ]
        for icon, label, key in public_services:
            if st.button(f"{icon}\n{label}", key=f"pub_{key[:6]}", use_container_width=True):
                if key == "calendar_tool":
                    st.session_state.show_tool = "calendar"
                else:
                    st.session_state.quick_question = key
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ===== 生活服务 =====
        st.markdown('<div class="sidebar-title"><span>🍀 生活服务</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="service-grid">', unsafe_allow_html=True)
        life_services = [
            ("🍚", "食堂开放", "食堂开放时间？"),
            ("📦", "快递查询", "怎么取快递？"),
            ("🏪", "校园超市", "校园超市在哪里？"),
            ("💊", "校医院", "校医院在哪里？"),
            ("🏧", "银行网点", "校园ATM在哪里？"),
            ("📱", "校园网络", "校园网怎么连接？"),
        ]
        for icon, label, key in life_services:
            if st.button(f"{icon}\n{label}", key=f"life_{key[:6]}", use_container_width=True):
                st.session_state.quick_question = key
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        if st.session_state.messages:
            total = len(st.session_state.messages)
            user_msgs = sum(1 for m in st.session_state.messages if m["role"] == "user")
            st.markdown(f"""
            <div class="stat-cards">
                <div class="stat-card"><div class="num">{total}</div><div class="label">消息</div></div>
                <div class="stat-card"><div class="num">{user_msgs}</div><div class="label">提问</div></div>
                <div class="stat-card"><div class="num">{total - user_msgs}</div><div class="label">回复</div></div>
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ 清空", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        with col2:
            if st.button("📥 导出", use_container_width=True):
                if st.session_state.messages:
                    st.session_state.export_dialog = True
        
        st.caption("⚡ v5.0 · RAG + DeepSeek")
    
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
    col_main, col_right = st.columns([3, 1])
    
    with col_main:
        st.markdown("""
        <div class="main-header">
            <h1>🏫 <span class="highlight">校园生活百事通</span></h1>
            <p>🤖 AI 智能助手 · 校园问题一站式解答</p>
            <span class="badge">✨ 支持 RAG 检索 · 多轮对话</span>
        </div>
        """, unsafe_allow_html=True)
        
        # === 工具功能 ===
        if st.session_state.show_tool == "gpa":
            st.session_state.show_tool = None
            with st.chat_message("assistant"):
                st.markdown("### 📊 绩点计算器")
                col1, col2 = st.columns([2, 1])
                with col1:
                    scores_input = st.text_input("请输入各科成绩（英文逗号分隔）", placeholder="85,90,78", key="gpa_input")
                with col2:
                    if st.button("计算绩点"):
                        if scores_input:
                            result = calculate_gpa(scores_input)
                            st.success(result) if "✅" in result else st.error(result)
                        else:
                            st.warning("请输入成绩")
        
        if st.session_state.show_tool == "calendar":
            st.session_state.show_tool = None
            with st.chat_message("assistant"):
                st.markdown("### 📅 校历查询")
                st.info(get_current_week())
                st.caption("校历起始日：2026年3月1日（第1周）")
        
        if st.session_state.show_tool == "schedule":
            st.session_state.show_tool = None
            with st.chat_message("assistant"):
                st.markdown("### 📝 本周课表")
                schedule = {
                    "周一": ["📖 数据结构 8:00-10:00", "💻 数据库 10:15-12:15"],
                    "周二": ["📐 高数 8:00-10:00", "🌐 网络 10:15-12:15"],
                    "周三": ["📝 算法 8:00-10:00", "🔧 实训 14:00-16:00"],
                    "周四": ["📊 统计 8:00-10:00", "📚 自习 14:00-16:00"],
                    "周五": ["🏫 班会 10:00-11:00", "📖 复习 14:00-16:00"],
                }
                day = st.selectbox("选择星期", list(schedule.keys()))
                for item in schedule[day]:
                    st.markdown(f"- {item}")
        
        # === 快捷问题处理 ===
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
                suggestions = generate_suggestions(q)
                if suggestions:
                    html = '<div style="display:flex;flex-wrap:wrap;gap:0.3rem;margin-top:0.5rem;">'
                    html += '<span style="font-size:0.7rem;color:#999;margin-right:0.3rem;">💡 相关问题：</span>'
                    for sug in suggestions:
                        html += f'<span style="background:#f0f2f6;padding:0.15rem 0.6rem;border-radius:12px;font-size:0.65rem;color:#667eea;cursor:pointer;">{sug}</span>'
                    html += '</div>'
                    st.markdown(html, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        # === 消息显示 ===
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
                    <span class="tag">🍚 食堂</span>
                    <span class="tag">📦 快递</span>
                    <span class="tag">🚍 班车</span>
                </div>
                <p style="font-size:0.65rem; color:#bbb; margin-top:0.2rem;">
                    💡 左侧导航栏分类查看 · 输入问题或点击快捷提问
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
        
        # === 输入区域 ===
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
                    suggestions = generate_suggestions(prompt)
                    if suggestions:
                        html = '<div style="display:flex;flex-wrap:wrap;gap:0.3rem;margin-top:0.5rem;">'
                        html += '<span style="font-size:0.7rem;color:#999;margin-right:0.3rem;">💡 相关问题：</span>'
                        for sug in suggestions:
                            html += f'<span style="background:#f0f2f6;padding:0.15rem 0.6rem;border-radius:12px;font-size:0.65rem;color:#667eea;cursor:pointer;">{sug}</span>'
                        html += '</div>'
                        st.markdown(html, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    # ===== 右侧模块 =====
    with col_right:
        st.markdown('<div class="right-module">', unsafe_allow_html=True)
        
        total_msgs = len(st.session_state.messages)
        user_msgs_count = sum(1 for m in st.session_state.messages if m["role"] == "user")
        st.markdown(f"""
        <div style="background:#fff;border-radius:12px;padding:0.6rem 0.8rem;border:1px solid rgba(102,126,234,0.06);margin-bottom:0.6rem;">
            <div style="font-size:0.6rem;color:#999;text-transform:uppercase;letter-spacing:0.5px;">📊 今日概览</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.3rem;margin-top:0.2rem;">
                <div style="background:#f8f9fe;border-radius:8px;padding:0.3rem;text-align:center;">
                    <div style="font-size:1.1rem;font-weight:700;color:#667eea;">{total_msgs}</div>
                    <div style="font-size:0.5rem;color:#999;">消息</div>
                </div>
                <div style="background:#f8f9fe;border-radius:8px;padding:0.3rem;text-align:center;">
                    <div style="font-size:1.1rem;font-weight:700;color:#667eea;">{user_msgs_count}</div>
                    <div style="font-size:0.5rem;color:#999;">提问</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background:#fff;border-radius:12px;padding:0.6rem 0.8rem;border:1px solid rgba(102,126,234,0.06);margin-bottom:0.6rem;">
            <div style="font-size:0.6rem;color:#999;text-transform:uppercase;letter-spacing:0.5px;">⚡ 快捷功能</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.3rem;margin-top:0.2rem;">
        """, unsafe_allow_html=True)
        
        quick_funcs = [("📊", "绩点"), ("📅", "校历"), ("📝", "课表"), ("📋", "请假")]
        for icon, label in quick_funcs:
            if st.button(f"{icon} {label}", key=f"quick_{label}", use_container_width=True):
                map_key = {"绩点": "gpa", "校历": "calendar", "课表": "schedule", "请假": "leave"}
                if map_key[label] == "leave":
                    st.session_state.quick_question = "怎么请假？"
                else:
                    st.session_state.show_tool = map_key[label]
                st.rerun()
        
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background:#fff;border-radius:12px;padding:0.6rem 0.8rem;border:1px solid rgba(102,126,234,0.06);">
            <div style="font-size:0.6rem;color:#999;text-transform:uppercase;letter-spacing:0.5px;">📋 今日热点</div>
            <div style="margin-top:0.2rem;">
                <div style="display:flex;align-items:center;gap:0.4rem;padding:0.15rem 0;border-bottom:1px solid #f0f2f6;">
                    <span style="width:5px;height:5px;border-radius:50%;background:#fdcb6e;"></span>
                    <span style="font-size:0.65rem;color:#555;flex:1;">新一轮选课开始啦！</span>
                    <span style="font-size:0.45rem;background:#f0f2f6;padding:0.05rem 0.4rem;border-radius:8px;color:#999;">进行中</span>
                </div>
                <div style="display:flex;align-items:center;gap:0.4rem;padding:0.15rem 0;border-bottom:1px solid #f0f2f6;">
                    <span style="width:5px;height:5px;border-radius:50%;background:#00b894;"></span>
                    <span style="font-size:0.65rem;color:#555;flex:1;">奖学金指南已更新</span>
                    <span style="font-size:0.45rem;background:#e8f8f0;padding:0.05rem 0.4rem;border-radius:8px;color:#00b894;">已完成</span>
                </div>
                <div style="display:flex;align-items:center;gap:0.4rem;padding:0.15rem 0;">
                    <span style="width:5px;height:5px;border-radius:50%;background:#ff6b6b;"></span>
                    <span style="font-size:0.65rem;color:#555;flex:1;">四六级报名提醒</span>
                    <span style="font-size:0.45rem;background:#fef0ee;padding:0.05rem 0.4rem;border-radius:8px;color:#ff6b6b;">待处理</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== 页脚 ====================
    st.markdown("""
    <div class="footer">
        🏫 安徽交通职业技术学院 · 人工智能应用技术开发<br>
        <span class="heart">❤</span> 基于 LangChain + DeepSeek RAG <span class="heart">❤</span>
    </div>
    """, unsafe_allow_html=True)


# ==================== 程序入口 ====================
# ✅ 修复：将 st.set_page_config 放在最前面，只调用一次
st.set_page_config(
    page_title="校园生活百事通",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 初始化Session状态
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_username" not in st.session_state:
    st.session_state.login_username = ""
if "login_password" not in st.session_state:
    st.session_state.login_password = ""
if "login_error" not in st.session_state:
    st.session_state.login_error = None

# 判断是否登录
if st.session_state.get("logged_in", False):
    main_app()
else:
    login_page()