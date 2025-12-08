import streamlit as st
import os
import requests
from datetime import datetime
import pytz

# ==========================================
# 1. 頁面基礎設定
# ==========================================
st.set_page_config(
    page_title="數位行銷自動化解決方案 | Portfolio",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# ==========================================
# 2. 核心邏輯：全站訪客計數 (隱藏式)
# ==========================================
COUNTER_URL = "https://api.counterapi.dev/v1"
NAMESPACE = "rhk_portfolio_system" 
KEY = "total_site_visits" # 改名為 site_visits，統計所有造訪

# 利用 Cache 儲存「上一次」造訪時間 (Server Cache)
@st.cache_resource
def get_server_state():
    return {"last_visit_timestamp": "系統重啟後首位"}

server_state = get_server_state()

def get_tw_time():
    tw = pytz.timezone('Asia/Taipei')
    return datetime.now(tw).strftime("%Y-%m-%d %H:%M:%S")

def increment_visit():
    """造訪次數 +1 (寫入)"""
    try:
        requests.get(f"{COUNTER_URL}/{NAMESPACE}/{KEY}/up", timeout=1)
    except:
        pass
    
    # 更新 Server 上的最後造訪時間
    server_state["last_visit_timestamp"] = get_tw_time()

def get_current_stats():
    """讀取目前數據 (唯讀)"""
    try:
        r = requests.get(f"{COUNTER_URL}/{NAMESPACE}/{KEY}/", timeout=1)
        count = r.json().get("count", 0) if r.status_code == 200 else 0
    except:
        count = 0
    
    return count, server_state["last_visit_timestamp"]

# --- 自動計數邏輯 ---
# 只要 session_state 中沒有 'visited' 標記，就代表是新開的網頁，執行 +1
if "visited" not in st.session_state:
    increment_visit()
    st.session_state.visited = True # 標記為已造訪，刷新頁面不會再加

# ==========================================
# 3. CSS 樣式
# ==========================================
st.markdown("""
<style>
    /* 全局設定 */
    .main-header {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #2c3e50;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 1rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 30px;
        font-weight: 400;
    }
    
    /* 聯絡資訊 */
    .contact-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        margin-bottom: 25px;
        color: #475569;
        font-size: 1rem;
    }
    .contact-card a { color: #2563eb; text-decoration: none; font-weight: 600; }

    /* 分類標題 */
    .category-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #334155;
        border-left: 5px solid #3b82f6;
        padding-left: 10px;
        margin-top: 30px;
        margin-bottom: 15px;
        background: linear-gradient(90deg, #f1f5f9 0%, #ffffff 100%);
        padding-top: 8px;
        padding-bottom: 8px;
    }

    /* 卡片與排版 */
    .tool-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 8px;
        white-space: nowrap; 
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .solution-badge {
        font-size: 0.8rem;
        color: #047857;
        background-color: #d1fae5;
        padding: 4px 8px;
        border-radius: 4px;
        display: inline-block;
        margin-bottom: 12px;
        font-weight: 600;
        border: 1px solid #6ee7b7;
    }
    .desc-text {
        font-size: 0.95rem;
        color: #475569;
        line-height: 1.5;
        margin-top: 10px;
        margin-bottom: 15px;
        min-height: 80px; 
    }
    .admin-zone {
        background-color: #fef2f2;
        padding: 15px;
        border-radius: 8px;
        border: 1px dashed #ef4444;
    }
    
    /* 圖片樣式 */
    img {
        border-radius: 4px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    
    /* 後台數據顯示 */
    .stat-box {
        background-color: #f1f5f9;
        border: 1px solid #cbd5e1;
        padding: 10px;
        border-radius: 6px;
        margin-bottom: 15px;
        font-family: monospace;
        color: #334155;
    }
    .stat-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
        font-size: 0.85rem;
    }
    .stat-val {
        font-weight: bold;
        color: #0f172a;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. 權限控制 (Sidebar: 管理員後台)
# ==========================================
is_unlocked = False

with st.sidebar:
    st.title("🔐 Admin Access")
    
    password = st.text_input("Access Key", type="password", placeholder="輸入密碼查看數據")
    
    if password == "790420":
        is_unlocked = True
        
        # 讀取數據 (不增加次數，只讀取)
        total_visits, last_time = get_current_stats()
        
        st.success("✅ Authorized")
        
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-row">
                <span>🌍 Total Visits:</span>
                <span class="stat-val">{total_visits}</span>
            </div>
            <hr style="margin: 5px 0; border-color: #cbd5e1;">
            <div class="stat-row">
                <span>🕒 Last Visit:</span>
            </div>
            <div style="font-size: 0.8rem; text-align: right; color: #64748b;">
                {last_time}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif password:
        st.error("❌ Access Denied")
    
    st.divider()
    st.caption("System Status: 🟢 Online")

# ==========================================
# 5. 標題與簡介
# ==========================================
st.markdown('<div class="main-header">數位行銷自動化解決方案中心</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Strategic Automation Hub: Enhancing Efficiency & Decision Quality</div>', unsafe_allow_html=True)

st.markdown("""
<div class="contact-card">
    👋 專案負責人：<strong>Rh K</strong>
    &nbsp;&nbsp;<span style="color:#cbd5e1">|</span>&nbsp;&nbsp;
    📧 Email：<a href="mailto:rhk9903@gmail.com">rhk9903@gmail.com</a>
</div>
""", unsafe_allow_html=True)

with st.expander("ℹ️ 關於此平台 (About this Portfolio)", expanded=True):
    st.warning("""
    **⚠️ 免責聲明 (Disclaimer)**
    本平台為個人 Portfolio Demo，所有邏輯以泛用模型 (Generic Models) 與模擬數據 (Synthetic Data) 設計，
    **不涉及任何實際客戶或前公司機密資料**。僅供技術展示與邏輯驗證使用。
    """)
    st.markdown("""
    此平台整合了我開發的自動化工具，旨在解決數位行銷工作中常見的**「重複性作業」**與**「數據盲點」**問題。
    **(點擊下方卡片按鈕可預覽功能，完整操作需解鎖 Demo Access)**
    """)

# ==========================================
# 6. 設定區：連結與圖片
# ==========================================
TOOLS = {
    "market_miner": "https://market-miner-ptfhq6qjq8vhuzaf4nkhre.streamlit.app/",
    "prompt_gen": "https://8wiqqppginsnnhexjv6chv.streamlit.app/",
    "seo_gen": "https://seo-prompt-builder-jamwdfnwpn36rwsyvznj5s.streamlit.app/", 
    "ads_analytics": "https://adsanalyticsforcourse-7vi6zvnjeautmk4qg2s2tl.streamlit.app/",
    "traffic_audit": "https://jfhcpyfqfqp7pwhc6yx2aw.streamlit.app/",
    "web_scraper": "https://competitive-intelligence-snapshot-b5sbxe3kqndxgb89782ofb.streamlit.app/",
    "system_core": "https://dennisisgod-dihjnspatfsqmks2w4me2n.streamlit.app/"
}

# 圖片檔名對照
IMG_FILES = {
    "market_miner": "demo_market.png",
    "prompt_gen": "demo_strategy.png",
    "seo_gen": "demo_seo.png",
    "ads_analytics": "demo_ads.png",
    "traffic_audit": "demo_traffic.png",
    "web_scraper": "demo_scraper.png",
    "system_core": "demo_console.png"
}

def show_demo_image(key):
    filename = IMG_FILES.get(key)
    if filename and os.path.exists(filename):
        st.image(filename, use_container_width=True)
    else:
        st.info(f"🖼️ 待上傳截圖：{filename}")

def render_secure_btn(url, btn_key, label="🚀 開啟工具 (Launch)"):
    if is_unlocked:
        st.link_button(label=label, url=url, type="primary", use_container_width=True)
    else:
        # 未解鎖狀態：鎖定按鈕
        if st.button("🔒 Demo Restricted", key=btn_key, type="secondary", use_container_width=True, disabled=False):
            st.toast("🚫 請輸入 Admin Key 以解鎖試用功能", icon="🔒")

# ==========================================
# 7. 儀表板佈局
# ==========================================

# --- Phase 1: 策略 ---
st.markdown('<div class="category-header">Phase 1: 市場決策與策略制定</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown('<div class="tool-title">💎 Market Insight Miner</div>', unsafe_allow_html=True)
        st.markdown('<div class="solution-badge">解決：市場調查耗時且缺乏標準</div>', unsafe_allow_html=True)
        show_demo_image("market_miner")
        st.markdown("""
        <div class="desc-text">
        將搜尋量數據轉化為「紅藍海策略地圖」。協助團隊在投入預算前，快速識別高需求但低競爭的利基市場。
        </div>
        """, unsafe_allow_html=True)
        render_secure_btn(TOOLS["market_miner"], "btn_market")

with col2:
    with st.container(border=True):
        st.markdown('<div class="tool-title">🎯 Strategy Decoder</div>', unsafe_allow_html=True)
        st.markdown('<div class="solution-badge">解決：廣告缺乏差異化，憑感覺</div>', unsafe_allow_html=True)
        show_demo_image("prompt_gen")
        st.markdown("""
        <div class="desc-text">
        從對手文案中提煉受眾心理，自動生成具備「差異化優勢」的行銷切角，確保素材突圍。
        </div>
        """, unsafe_allow_html=True)
        render_secure_btn(TOOLS["prompt_gen"], "btn_prompt")

with col3:
    with st.container(border=True):
        st.markdown('<div class="tool-title">📑 SEO Prompt Gen</div>', unsafe_allow_html=True)
        st.markdown('<div class="solution-badge">解決：AI 寫文章缺乏 SEO 架構</div>', unsafe_allow_html=True)
        show_demo_image("seo_gen")
        st.markdown("""
        <div class="desc-text">
        全流程 SEO 戰略生成器。從產品解析、關鍵字調研到意圖分析，一步步引導 AI 產出高排名文章架構。
        </div>
        """, unsafe_allow_html=True)
        # 這裡不需鎖定，直接顯示連結
        st.link_button("🚀 開啟工具 (Launch)", TOOLS["seo_gen"], type="primary", use_container_width=True)

# --- Phase 2: 成效 ---
st.markdown('<div class="category-header">Phase 2: 成效優化與風險控制</div>', unsafe_allow_html=True)
col4, col5 = st.columns(2)

with col4:
    with st.container(border=True):
        st.markdown('<div class="tool-title">📈 Automated Performance Audit</div>', unsafe_allow_html=True)
        st.markdown('<div class="solution-badge">解決：人工報表製作耗時，異常滯後</div>', unsafe_allow_html=True)
        show_demo_image("ads_analytics")
        st.markdown("""
        <div class="desc-text">
        取代人工 Excel 拉表，自動進行成效診斷。能比人工更早發現 CPA 暴漲或 CTR 衰退跡象，實現「即時止損」。
        </div>
        """, unsafe_allow_html=True)
        render_secure_btn(TOOLS["ads_analytics"], "btn_ads", label="📈 查看儀表板 (Dashboard)")

with col5:
    with st.container(border=True):
        st.markdown('<div class="tool-title">⚖️ Traffic Quality & Fraud Guard</div>', unsafe_allow_html=True)
        st.markdown('<div class="solution-badge">解決：無效流量浪費預算與誤導</div>', unsafe_allow_html=True)
        show_demo_image("traffic_audit")
        st.markdown("""
        <div class="desc-text">
        針對廣告帳戶進行健康度檢查，揪出「幽靈點擊」與「展示灌水」行為。確保預算花在真實的高品質潛在客戶身上。
        </div>
        """, unsafe_allow_html=True)
        render_secure_btn(TOOLS["traffic_audit"], "btn_traffic", label="🛡️ 執行診斷 (Diagnostic)")

# --- Phase 3: 競情與維運 ---
st.markdown('<div class="category-header">Phase 3: 競情蒐集與系統維運</div>', unsafe_allow_html=True)
col6, col7 = st.columns(2)

with col6:
    with st.container(border=True):
        st.markdown('<div class="tool-title">📥 Competitive Intelligence</div>', unsafe_allow_html=True)
        st.markdown('<div class="solution-badge">解決：手動截圖效率低，難以追蹤</div>', unsafe_allow_html=True)
        show_demo_image("web_scraper")
        st.markdown("""
        <div class="desc-text">
        模擬使用者行為，自動擷取競爭對手的動態網頁資料 (如 FB 廣告檔案庫)。解決「無限捲動」問題，建立戰略資料庫。
        </div>
        """, unsafe_allow_html=True)
        render_secure_btn(TOOLS["web_scraper"], "btn_scraper", label="📥 啟動擷取 (Scraper)")

with col7:
    with st.container(border=True):
        st.markdown('<div class="admin-zone">', unsafe_allow_html=True)
        st.markdown('<div class="tool-title" style="color:#991b1b;">🔒 System Integrity Monitor</div>', unsafe_allow_html=True)
        show_demo_image("system_core")
        
        st.markdown("""
        <div style="font-size: 0.85rem; color: #7f8c8d; margin-bottom: 10px; line-height:1.5;">
        <strong>[Demo Module]</strong> 監控 API 連線狀態與系統日誌。<br>
        確保分析數據準確性。
        </div>
        """, unsafe_allow_html=True)
        
        # 系統中控台連結 (不需鎖定，保持外部跳轉)
        if st.button("⚡ Initialize Connection", use_container_width=True, type="primary"):
            st.link_button("🔧 Enter Demo Console", TOOLS["system_core"], use_container_width=True)
        # 注意：st.button 按下後會刷新，直接用 link_button 更直覺，這裡為保持儀式感使用 link_button
        st.link_button("🔧 Enter Demo Console", TOOLS["system_core"], use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 8. 頁尾
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.8rem;">
    © 2024 Strategic Automation Portfolio. Designed to solve real-world marketing challenges.
</div>
""", unsafe_allow_html=True)
