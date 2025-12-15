import streamlit as st

# ==========================================
# 1. Page config
# ==========================================
st.set_page_config(
    page_title="SEO 8-Step 戰略儀表板 (Light Project Packet Edition)",
    page_icon="⚡",
    layout="wide"
)

# ==========================================
# 2. CSS
# ==========================================
st.markdown(
    """
<style>
    .stTextArea textarea, .stTextInput input {
        font-family: "Consolas", "Monaco", monospace;
        font-size: 0.95rem;
        background-color: #f8f9fa;
        color: #333;
    }
    .main-header {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1E3A8A;
        border-bottom: 2px solid #eee;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #2563EB;
        margin-top: 10px;
        margin-bottom: 5px;
    }
    .hint {
        font-size: 0.9rem;
        color: #475569;
        margin-top: 6px;
        margin-bottom: 10px;
    }
    .stButton button { margin-top: 0.5rem; }
</style>
""",
    unsafe_allow_html=True
)

# ==========================================
# 3. Steps & Templates
# ==========================================
STEPS = [
    "Step 1: 專案摘要 (Project Log) 建立",
    "Step 1.5: Persona/Voice 建模（寫入封包，可選）",
    "Step 2: SEO 任務目標 → 主題發想（寫入封包）",
    "Step 3: 關鍵字候選清單 (Pre-GKP)",
    "Step 4: GKP 數據決策 (Post-GKP)（寫入封包）",
    "Step 5: 搜尋意圖 Deep Research（寫入封包）",
    "Step 6: 文章標題生成（寫入封包：Backlog/文章卡）",
    "Step 7: 文章大綱（更新指定文章卡）",
    "Step 8: 文章撰寫 + 技術 SEO（更新指定文章卡）",
    "Step 9: 改稿（Revision）+ 變更紀錄（寫入封包）",
]

PROJECT_PACKET_TEMPLATE = """【PROJECT PACKET v1 | LIGHT】

=== [SOURCE NOTE | OPTIONAL] ===
- 原始資料類型：LP / 產品說明 / 白皮書 / Notion / Google Doc（擇一或多）
- 開新對話是否需要重貼原始資料：是（建議）
- 備註：本封包只存「決策與狀態」。原始資料可在需要時於新對話重新貼上。
=== [/SOURCE NOTE] ===

=== [PROJECT LOG | EDITABLE] ===
- 產品/計畫一句話總結：
- 目標客群（Persona）：
- 核心價值主張（3–5點）：
- 痛點（3–5點）：
- 內容缺口（Information Gaps）：
- SEO 任務目標（必填）：
- 品牌語氣/禁忌/限制條件（必填，未知可寫「未指定」）：
=== [/PROJECT LOG] ===

=== [VOICE CONTEXT | EDITABLE] ===
[PERSONA LOG]
- 作者世界觀一句話：
- 對讀者的定位（上對下/並肩/挑釁/對話）：
- 核心信念/價值觀（3–7條）：
- 動機邊界（他為什麼寫、他不做什麼）：
- 允許的模糊與留白（哪些可以不講死）：
- 禁語/禁套路（含理由）：

[VOICE SPEC]
- tone_mix（%）：冷靜__ / 犀利__ / 幽默__ / 溫度__
- sentence_rhythm：短句比例__%；每段__–__行；轉折頻率__
- stance_rules：如何下結論/如何留白/如何反問
- lexical_rules：常用詞/避免詞/禁詞
- structure_rules：常用推理順序（例：現象→對照→推論→選項）
- do_not：絕對禁止事項
- sample_lines（<=5句，每句<=25字）：
=== [/VOICE CONTEXT] ===

=== [STRATEGY LOG | EDITABLE] ===
- Primary Keyword（含GKP數據與理由）：
- Secondary Keywords：
- Supporting Keywords：
- SERP/Intent 洞察摘要（Winning Angle）：
- 差異化切入點（降維打擊角度）：
- 排除與不做（Avoid List）：
=== [/STRATEGY LOG] ===

=== [CONTENT QUEUE | EDITABLE] ===
[Backlog Titles | one per line]
- （每行一個標題）

[Article Cards]
- 文章ID：A01
  - 標題：
  - Primary/Secondary/Supporting：
  - Winning Angle：
  - 大綱（H1/H2/H3）：
  - 字數：
  - CTA：
  - Meta Title/Meta Desc/Schema：
  - 產出備註/連結：
=== [/CONTENT QUEUE] ===

=== [REVISION LOG | EDITABLE] ===
- 本次改稿文章ID：
- 客戶回饋摘要（1–5點）：
- 修改清單 Must / Should / Could：
- 已採納（含理由摘要）：
- 未採納（含理由摘要）：
- 版本紀錄（v1→v2 差異一句話）：
- 需要同步更新 VOICE CONTEXT 嗎？（是/否；若是，列出更新條款）：
=== [/REVISION LOG] ===
"""

def get_value(input_val, placeholder_text):
    if input_val is not None and str(input_val).strip():
        return str(input_val).strip()
    return f"[{placeholder_text}]"

def go_to_step(step_index: int):
    if 0 <= step_index < len(STEPS):
        st.session_state.nav_radio = STEPS[step_index]

# ==========================================
# 4. Init session defaults
# ==========================================
st.session_state.setdefault("nav_radio", STEPS[0])
st.session_state.setdefault("project_packet", PROJECT_PACKET_TEMPLATE)
st.session_state.setdefault("current_article_id", "A01")
st.session_state.setdefault("current_title", "")
st.session_state.setdefault("voice_bank", "")

# ==========================================
# 5. Sidebar: Navigation + Packet + Voice Bank
# ==========================================
with st.sidebar:
    st.title("⚡ SEO 戰略中控")

    st.subheader("📍 步驟導覽")
    selected_step = st.radio(
        "選擇當前進度：",
        STEPS,
        index=STEPS.index(st.session_state.nav_radio) if st.session_state.nav_radio in STEPS else 0,
        key="nav_radio"
    )

    st.divider()

    st.subheader("🧳 Project Packet（輕封包）")
    st.info("封包只保存「決策與狀態」。原始資料需要時再貼；不要把原文硬塞進封包。")

    project_packet = st.text_area(
        "目前封包內容（建議保持為單一可複製區塊）",
        height=360,
        key="project_packet"
    )
    project_packet_val = get_value(project_packet, "尚未建立封包")

    st.divider()

    st.subheader("🎛️ Voice Bank（全流程外掛）")
    st.info("你已整理好的語感/價值觀/寫作規則可貼在這。只要這裡有內容，所有步驟都會優先採用。")
    voice_bank = st.text_area(
        "Voice Bank（PERSONA LOG / VOICE SPEC / 禁語 / 範例句等）",
        height=260,
        key="voice_bank",
        placeholder="貼上你的語感規則（可長）。建議用條列/小標題，便於AI穩定引用。"
    )

    colvb1, colvb2 = st.columns([1, 1])
    with colvb1:
        if st.button("清空 Voice Bank"):
            st.session_state.voice_bank = ""
    with colvb2:
        st.caption("（此版本不自動改封包；由 AI 在輸出時寫回封包 VOICE CONTEXT）")

    st.divider()

    st.subheader("🧩 文章卡控制（跨步驟共用）")
    current_article_id = st.text_input(
        "目前要更新的文章ID（例：A01）",
        value=st.session_state.get("current_article_id", "A01"),
        key="current_article_id"
    )
    current_title = st.text_input(
        "目前文章標題（可選填，讓 Step7/8 更穩）",
        value=st.session_state.get("current_title", ""),
        key="current_title"
    )

# ==========================================
# 6. Prompt building blocks
# ==========================================
def state_reference_block(packet: str) -> str:
    return f"""【狀態參考（非輸出對象）】
以下內容僅供你理解目前狀態；本回合「主要產出」不是重寫這份文件：
{packet}
"""

def voice_bank_block(voice_bank_text: str) -> str:
    vb = (voice_bank_text or "").strip()
    if not vb:
        return "【VOICE BANK（外掛語感資產）】（未提供）"
    return f"""【VOICE BANK（外掛語感資產｜優先於封包 VOICE CONTEXT）】
{vb}
"""

def voice_priority_rules() -> str:
    return """【語感優先規則（必讀）】
- 若 VOICE BANK 有內容：視為最高優先語感規格（高於封包內 VOICE CONTEXT）。
- 若 VOICE BANK 與封包 VOICE CONTEXT 衝突：先輸出「衝突點 + 合併策略」（<
