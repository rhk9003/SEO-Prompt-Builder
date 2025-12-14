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
    "Step 2: SEO 任務目標 → 主題發想（寫入封包）",
    "Step 3: 關鍵字候選清單 (Pre-GKP)",
    "Step 4: GKP 數據決策 (Post-GKP)（寫入封包）",
    "Step 5: 搜尋意圖 Deep Research（寫入封包）",
    "Step 6: 文章標題生成（寫入封包：Backlog/文章卡）",
    "Step 7: 文章大綱（更新指定文章卡）",
    "Step 8: 文章撰寫 + 技術 SEO（更新指定文章卡）"
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
"""

def get_value(input_val, placeholder_text):
    if input_val is not None and str(input_val).strip():
        return str(input_val).strip()
    return f"[{placeholder_text}]"

def go_to_step(step_index: int):
    if 0 <= step_index < len(STEPS):
        st.session_state.nav_radio = STEPS[step_index]

# ==========================================
# 4. Sidebar: Navigation + Project Packet
# ==========================================
with st.sidebar:
    st.title("⚡ SEO 戰略中控")

    st.subheader("📍 步驟導覽")
    if "nav_radio" not in st.session_state:
        st.session_state.nav_radio = STEPS[0]

    selected_step = st.radio(
        "選擇當前進度：",
        STEPS,
        index=0,
        key="nav_radio"
    )

    st.divider()

    st.subheader("🧳 Project Packet（輕封包）")
    st.info("封包只保存「決策與狀態」。需要時你再把原始資料於新對話重新貼上即可。")

    if "project_packet" not in st.session_state:
        st.session_state.project_packet = PROJECT_PACKET_TEMPLATE

    project_packet = st.text_area(
        "目前封包內容（建議保持為單一可複製區塊）",
        height=420,
        key="project_packet"
    )
    project_packet_val = get_value(project_packet, "尚未建立封包")

    st.divider()

    st.subheader("🧩 文章卡控制（跨步驟共用）")
    st.session_state.current_article_id = st.text_input(
        "目前要更新的文章ID（例：A01）",
        value=st.session_state.get("current_article_id", "A01"),
        key="current_article_id"
    )
    st.session_state.current_title = st.text_input(
        "目前文章標題（可選填，讓 Step7/8 更穩）",
        value=st.session_state.get("current_title", ""),
        key="current_title"
    )

# ==========================================
# 5. Main
# ==========================================

# ------------------------------------------
# Step 1
# ------------------------------------------
if selected_step == STEPS[0]:
    st.markdown('<div class="main-header">✅ Step 1：專案摘要 (Project Log) 建立</div>', unsafe_allow_html=True)
    st.caption("目標：把你貼的原始資料『萃取成決策狀態』寫入封包（不保存原文）。")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="sub-header">📥 輸入資料</div>', unsafe_allow_html=True)
        st.markdown('<div class="hint">貼原始內容即可（LP/產品說明/白皮書片段）。本工具不要求把原文存進封包。</div>', unsafe_allow_html=True)
        p1_source = st.text_area(
            "原始資料（本回合用，開新對話可再貼）",
            height=320,
            placeholder="貼上你的產品說明、Landing Page 文案、白皮書片段（可部分或完整）...",
            key="s1_source"
        )

    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)

        source_val = get_value(p1_source, "內容貼在這裡")
        prompt1 = f"""以下是目前的 PROJECT PACKET（你必須以它為唯一跨回合狀態）：

{project_packet_val}

【本回合原始資料（僅本回合參考，不要寫入封包，不要復誦原文）】
{source_val}

【任務】
請基於原始資料，更新封包的 PROJECT LOG（只更新/補齊以下欄位）：
- 產品/計畫一句話總結
- 目標客群（Persona）
- 核心價值主張（3–5點）
- 痛點（3–5點）
- 內容缺口（Information Gaps）
- 品牌語氣/禁忌/限制條件（若未知寫「未指定」）

【輸出規則（降噪版）】
1) 僅輸出「完整最新版 PROJECT PACKET v1 | LIGHT」於單一 Markdown code block。
2) 除非我明確要求，禁止在 code block 外加任何額外段落。
3) 只更新被指示的欄位；其餘封包內容保持原樣。
"""
        st.code(prompt1, language="markdown")

    st.divider()
    st.button("👉 前往下一步：Step 2", on_click=go_to_step, args=(1,), type="primary")

# ------------------------------------------
# Step 2
# ------------------------------------------
elif selected_step == STEPS[1]:
    st.markdown('<div class="main-header">✅ Step 2：SEO 任務目標 → 主題發想（寫入封包）</div>', unsafe_allow_html=True)
    st.caption("目標：主題發想 + 把 SEO 任務目標寫回封包（避免跨對話遺失）。")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="sub-header">📥 輸入</div>', unsafe_allow_html=True)
        p2_goal = st.text_area(
            "SEO 任務目標（你希望這批文章達成什麼）",
            height=180,
            placeholder="例如：建立權威、導向諮詢/試用、提高特定品類自然搜尋...",
            key="s2_goal"
        )

    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        goal_val = get_value(p2_goal, "任務目標")

        prompt2 = f"""以下是目前的 PROJECT PACKET：

{project_packet_val}

【任務】
1) 以封包 PROJECT LOG 為前提，根據我提供的 SEO 任務目標，產出 10–20 個可操作主題方向（Topic Clusters），以表格呈現：
| 主題方向 | 關鍵字類型 | 搜尋意圖類型 | 註解 |

2) 將「SEO 任務目標」寫回封包 PROJECT LOG 的對應欄位。

SEO 任務目標：{goal_val}

【輸出規則】
- 僅輸出「完整最新版 PROJECT PACKET v1 | LIGHT」於單一 Markdown code block。
- 只更新被指示區塊；其餘封包內容保持原樣。
"""
        st.code(prompt2, language="markdown")

    st.divider()
    st.button("👉 前往下一步：Step 3", on_click=go_to_step, args=(2,), type="primary")

# ------------------------------------------
# Step 3
# ------------------------------------------
elif selected_step == STEPS[2]:
    st.markdown('<div class="main-header">✅ Step 3：關鍵字候選清單 (Pre-GKP)</div>', unsafe_allow_html=True)
    st.caption("目標：把 Topic 轉成可丟進 GKP 的關鍵字清單（通常不更新封包）。")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="sub-header">📥 輸入</div>', unsafe_allow_html=True)
        p3_topics = st.text_area(
            "Step 2 的 Topic Clusters / 主題方向",
            height=240,
            placeholder="貼上 Step2 的主題表格或清單...",
            key="s3_topics"
        )

    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        topics_val = get_value(p3_topics, "主題清單")

        prompt3 = f"""以下是目前的 PROJECT PACKET（供背景，可不更新封包）：

{project_packet_val}

請根據以下主題/Topic 清單，產出關鍵字候選清單，用於丟進 Google Keyword Planner (GKP)：

主題清單：
{topics_val}

【GKP 專用輸出格式（嚴格）】
1) 純文字清單，關鍵字之間用英文逗號 (,) 分隔
2) 不要編號、不要項目符號
3) 每 10 個關鍵字一組，組與組之間空一行
4) 務必包含 Seed Keywords + 長尾詞
"""
        st.code(prompt3, language="markdown")

    st.divider()
    st.button("👉 前往下一步：Step 4", on_click=go_to_step, args=(3,), type="primary")

# ------------------------------------------
# Step 4
# ------------------------------------------
elif selected_step == STEPS[3]:
    st.markdown('<div class="main-header">✅ Step 4：GKP 數據決策 (Post-GKP)（寫入封包）</div>', unsafe_allow_html=True)
    st.caption("目標：用真實數據決定 Primary/Secondary/Supporting，並寫回封包 STRATEGY LOG。")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="sub-header">📥 輸入</div>', unsafe_allow_html=True)
        p4_gkp = st.text_area(
            "GKP 輸出數據（貼表格/CSV文字）",
            height=320,
            placeholder="直接貼上 GKP 表格或 CSV 文字...",
            key="s4_gkp"
        )

    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        gkp_val = get_value(p4_gkp, "GKP 輸出資料")

        prompt4 = f"""以下是目前的 PROJECT PACKET：

{project_packet_val}

【任務】
請根據以下 GKP 數據，決定關鍵字策略，並更新封包 STRATEGY LOG（Primary/Secondary/Supporting）。

GKP 數據：
{gkp_val}

【分析輸出（寫回封包 STRATEGY LOG）】
- Primary Keyword（含數據與理由）
- Secondary Keywords（含用途）
- Supporting Keywords
- 策略邏輯說明（流量 vs 競爭度取捨）
- 後續 SERP 分析建議（你要看什麼）

【輸出規則】
- 僅輸出「完整最新版 PROJECT PACKET v1 | LIGHT」於單一 Markdown code block。
- 只更新 STRATEGY LOG；其餘封包內容保持原樣。
"""
        st.code(prompt4, language="markdown")

    st.divider()
    st.button("👉 前往下一步：Step 5", on_click=go_to_step, args=(4,), type="primary")

# ------------------------------------------
# Step 5
# ------------------------------------------
elif selected_step == STEPS[4]:
    st.markdown('<div class="main-header">✅ Step 5：搜尋意圖 Deep Research（寫入封包）</div>', unsafe_allow_html=True)
    st.caption("目標：SERP 真實戰況 + 深層意圖洞察。將 Winning Angle、差異化切入點寫回封包。")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="sub-header">📥 輸入</div>', unsafe_allow_html=True)
        p5_keywords = st.text_area(
            "核心關鍵字（Primary + 重要 Secondary）",
            height=180,
            placeholder="例如：\nB群 什麼時候吃\nB群 空腹\n上班族 疲勞 補充品",
            key="s5_kw"
        )

    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        kw_val = get_value(p5_keywords, "核心關鍵字")

        prompt5 = f"""以下是目前的 PROJECT PACKET：

{project_packet_val}

【任務】
請針對以下核心關鍵字做 SERP/Intent Deep Research（需實際搜索 SERP 前 10–20 名）：
關鍵字：{kw_val}

【輸出（請寫回封包 STRATEGY LOG）】
請將結果收斂寫回這三欄：
- SERP/Intent 洞察摘要（Winning Angle）
- 差異化切入點（降維打擊角度）
- 排除與不做（Avoid List）

【研究過程（不需寫回封包，可簡短）】
你可以先用條列輸出：
1) SERP 同質化點
2) 使用者顯性/隱性問題
3) 你的 Winning Angle（1句）
4) 內容打法（3–5點）

【輸出規則】
- 僅輸出「完整最新版 PROJECT PACKET v1 | LIGHT」於單一 Markdown code block。
- 只更新 STRATEGY LOG；其餘封包內容保持原樣。
"""
        st.code(prompt5, language="markdown")

    st.divider()
    st.button("👉 前往下一步：Step 6", on_click=go_to_step, args=(5,), type="primary")

# ------------------------------------------
# Step 6
# ------------------------------------------
elif selected_step == STEPS[5]:
    st.markdown('<div class="main-header">✅ Step 6：文章標題生成（寫入封包：Backlog/文章卡）</div>', unsafe_allow_html=True)
    st.caption("目標：產出標題池（Backlog）+ 分群與寫作順序；至少建立 3 張文章卡。")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="sub-header">📥（可選填）補充線索</div>', unsafe_allow_html=True)
        p6_hint = st.text_area(
            "補充：你想偏好的角度/禁語/受眾（可留空，以封包為準）",
            height=220,
            placeholder="例如：更偏商業導向、避開醫療宣稱、語氣要犀利但專業...",
            key="s6_hint"
        )

    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        hint_val = get_value(p6_hint, "（無）")

        prompt6 = f"""以下是目前的 PROJECT PACKET：

{project_packet_val}

補充偏好（可選）：{hint_val}

【任務】
1) 產出 15–25 個文章標題，分為：
   - 資訊型
   - 比較/選擇型
   - 行動導向型
   要求：融入 Primary Keyword、有點擊動機、不重複。

2) 將標題寫入封包 CONTENT QUEUE -> [Backlog Titles]（每行一個）。

3) 將標題分成 3–5 個 Cluster，並給「建議寫作順序」（先 pillar 後 supporting）。

4) 在封包 [Article Cards] 中，至少建立 3 張新文章卡（A01/A02/A03 或延續既有編號），每張卡先填：
   - 文章ID
   - 標題
   - Primary/Secondary/Supporting（按 cluster 分配）
   - Winning Angle（從封包 STRATEGY LOG 套用到各卡）

【輸出規則】
- 僅輸出「完整最新版 PROJECT PACKET v1 | LIGHT」於單一 Markdown code block。
- 只更新 CONTENT QUEUE（必要時也可補齊 STRATEGY LOG，但避免擴寫無關內容）。
"""
        st.code(prompt6, language="markdown")

    st.divider()
    st.button("👉 前往下一步：Step 7", on_click=go_to_step, args=(6,), type="primary")

# ------------------------------------------
# Step 7
# ------------------------------------------
elif selected_step == STEPS[6]:
    st.markdown('<div class="main-header">✅ Step 7：文章大綱（更新指定文章卡）</div>', unsafe_allow_html=True)
    st.caption("目標：只更新你指定的文章ID那張卡，避免污染其他文章。")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="sub-header">📥 指定文章</div>', unsafe_allow_html=True)
        p7_article_id = st.text_input(
            "要更新的文章ID（建議與側欄一致）",
            value=st.session_state.get("current_article_id", "A01"),
            key="s7_aid"
        )
        p7_title = st.text_input(
            "標題（可留空，若封包該文章卡已有標題）",
            value=st.session_state.get("current_title", ""),
            key="s7_title"
        )
        p7_source = st.text_area(
            "（可選）本回合補充原始資料片段/要點（不存封包，不復誦原文）",
            height=140,
            placeholder="若這篇需要特定資料支撐，你可以貼片段或要點...",
            key="s7_source"
        )

    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        aid_val = get_value(p7_article_id, "A01")
        title_val = get_value(p7_title, "（若封包該卡已有標題可留空）")
        s7_source_val = get_value(p7_source, "（無）")

        prompt7 = f"""以下是目前的 PROJECT PACKET：

{project_packet_val}

【本回合補充原始資料/要點（可選，僅本回合參考，不要寫入封包，不要復誦原文）】
{s7_source_val}

【任務】
- 針對文章ID：{aid_val} 生成文章大綱（H1/H2/H3）。
- 若我提供標題：{title_val}，以此為準；若未提供，請從封包該文章卡的「標題」欄位讀取。
- 將大綱寫回封包該文章卡的「大綱（H1/H2/H3）」欄位。

【要求】
1) 結構：H1/H2/H3
2) 每個 H2 必須對應明確使用者問題（以封包 STRATEGY LOG 的意圖洞察對齊）
3) 大綱邏輯簡述：寫在該文章卡「產出備註/連結」欄位（簡短即可）

【輸出規則（很重要）】
- 僅輸出「完整最新版 PROJECT PACKET v1 | LIGHT」於單一 Markdown code block。
- 只能更新該文章ID對應的文章卡；其他文章卡不得更動。
"""
        st.code(prompt7, language="markdown")

    st.divider()
    st.button("👉 前往下一步：Step 8", on_click=go_to_step, args=(7,), type="primary")

# ------------------------------------------
# Step 8
# ------------------------------------------
elif selected_step == STEPS[7]:
    st.markdown('<div class="main-header">✅ Step 8：文章撰寫 + 技術 SEO（更新指定文章卡）</div>', unsafe_allow_html=True)
    st.caption("目標：只依賴封包 + 本回合補充資料完成寫作，並把產出寫回該文章卡（跨對話可續）。")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="sub-header">📥 寫作參數</div>', unsafe_allow_html=True)
        p8_article_id = st.text_input(
            "要撰寫的文章ID（建議與側欄一致）",
            value=st.session_state.get("current_article_id", "A01"),
            key="s8_aid"
        )
        p8_word = st.text_input("字數需求", value="1500 字", key="s8_word")
        p8_cta = st.text_input("CTA 文案", value="免費試用：https://example.com", key="s8_cta")
        p8_extra = st.text_area(
            "補充寫作指示（口吻/禁語/一定要提的點）",
            height=140,
            placeholder="例如：避免醫療宣稱、語氣冷靜專業、要加入比較表、要加FAQ...",
            key="s8_extra"
        )
        p8_source = st.text_area(
            "（可選）本回合原始資料/事實要點（不存封包，不復誦原文）",
            height=140,
            placeholder="若要更準確，可貼支撐點/數據/產品規格/限制條款等...",
            key="s8_source"
        )

    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        aid_val = get_value(p8_article_id, "A01")
        word_val = get_value(p8_word, "1500字")
        cta_val = get_value(p8_cta, "CTA")
        extra_val = get_value(p8_extra, "（無）")
        p8_source_val = get_value(p8_source, "（無）")

        prompt8 = f"""以下是目前的 PROJECT PACKET：

{project_packet_val}

【本回合原始資料/事實要點（可選，僅本回合參考，不要寫入封包，不要復誦原文）】
{p8_source_val}

【任務】
請只依賴封包（+本回合補充要點）撰寫文章ID：{aid_val} 的完整文章。
- 字數：{word_val}
- CTA：{cta_val}
- 補充指示：{extra_val}

【產出要求（寫回該文章卡）】
請在該文章卡中更新/填入：
1) 正文（建議放在「產出備註/連結」欄位中，以 Markdown 排版）
2) Meta Title（<60字）
3) Meta Description（<160字）
4) Schema Markup 建議（條列）
5) 技術 SEO 檢查清單（條列：內鏈建議、段落結構、FAQ、表格/清單使用點）

【輸出規則（很重要）】
- 僅輸出「完整最新版 PROJECT PACKET v1 | LIGHT」於單一 Markdown code block。
- 只能更新該文章ID對應的文章卡；其他文章卡不得更動。
"""
        st.code(prompt8, language="markdown")

    st.divider()
    st.success("✅ 建議操作：每一步只複製最新版『Project Packet | LIGHT』到新對話，即可續寫下一篇，不靠長對話記憶。")
