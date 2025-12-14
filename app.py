import streamlit as st

# ==========================================
# 1. 頁面基礎設定
# ==========================================
st.set_page_config(
    page_title="SEO 8-Step 戰略儀表板 (Project Packet Edition)",
    page_icon="⚡",
    layout="wide"
)

# ==========================================
# 2. CSS（閱讀體驗）
# ==========================================
st.markdown("""
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
    .stButton button { margin-top: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 輔助函式與全域變數
# ==========================================
STEPS = [
    "Step 1: 產品 / 計畫解析（建立 Project Packet）",
    "Step 2: SEO 任務目標 → 主題發想（寫入封包）",
    "Step 3: 關鍵字候選清單 (Pre-GKP)",
    "Step 4: GKP 數據決策 (Post-GKP)（寫入封包）",
    "Step 5: 搜尋意圖 Deep Research（建議寫入封包）",
    "Step 6: 文章標題生成（寫入封包：Backlog/文章卡）",
    "Step 7: 文章大綱（更新指定文章卡）",
    "Step 8: 文章撰寫 + 技術 SEO（更新指定文章卡）"
]

PROJECT_PACKET_TEMPLATE = """【PROJECT PACKET v1】

=== [RAW SOURCE | DO NOT MODIFY] ===
（把原始產品/計畫內容、LP文案、白皮書片段等「完整原文」貼在這裡。）
=== [/RAW SOURCE] ===

=== [PROJECT LOG | EDITABLE] ===
- 產品/計畫一句話總結：
- 目標客群：
- 核心價值主張（3–5點）：
- 痛點（3–5點）：
- 內容缺口（Information Gaps）：
- SEO 任務目標（這個一定要寫在封包裡）：
- 品牌語氣/禁忌/限制條件：
=== [/PROJECT LOG] ===

=== [STRATEGY LOG | EDITABLE] ===
- Primary Keyword（含GKP數據與理由）：
- Secondary Keywords：
- Supporting Keywords：
- SERP/Intent 洞察摘要（Winning Angle）：
- 差異化切入點（降維打擊角度）：
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
# 4. SIDEBAR：導覽＋Project Packet（可攜帶封包）
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

    st.subheader("🧳 Project Packet（可攜帶封包）")
    st.info("你要避免對話太長造成劣化：每次都只複製『最新版封包』到新對話即可續寫。")

    if "project_packet" not in st.session_state:
        st.session_state.project_packet = PROJECT_PACKET_TEMPLATE

    project_packet = st.text_area(
        "目前封包內容（請保持為單一可複製區塊）",
        height=420,
        key="project_packet"
    )
    project_packet_val = get_value(project_packet, "尚未建立封包")

    st.divider()

    st.subheader("🧩 文章卡控制（跨步驟共用）")
    current_article_id = st.text_input("目前要更新的文章ID（例：A01）", value=st.session_state.get("current_article_id", "A01"), key="current_article_id")
    current_title = st.text_input("目前文章標題（可選填，讓 Step7/8 更穩）", value=st.session_state.get("current_title", ""), key="current_title")

# ==========================================
# 5. 主畫面：各步驟
# ==========================================

# ------------------------------------------
# Step 1
# ------------------------------------------
if selected_step == STEPS[0]:
    st.markdown('<div class="main-header">✅ Step 1：產品 / 計畫解析（建立 Project Packet）</div>', unsafe_allow_html=True)
    st.caption("目標：把原始資料與專案摘要封裝成『可移植封包』，之後任何新對話只靠封包就能續寫。")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="sub-header">📥 輸入資料（Raw Source）</div>', unsafe_allow_html=True)
        p1_input = st.text_area("原始產品/計畫內容（請貼完整原文）", height=320, placeholder="貼上你的產品說明、Landing Page 文案、白皮書片段（完整原文）...", key="s1_input")

    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        raw_source = get_value(p1_input, "內容貼在這裡（完整原文）")

        prompt1 = f"""你將收到一份「PROJECT PACKET v1」，以及我提供的原始資料（RAW SOURCE）。

【硬性規則】
1) 你必須輸出「完整最新版 PROJECT PACKET v1」於單一 Markdown code block。
2) 你必須確保封包中 RAW SOURCE 區塊「逐字原封不動」回傳（包含換行/標點/空白），不得改寫、不得摘要、不得重排、不得刪字。
3) 若封包 RAW SOURCE 目前是空或佔位，你必須把我提供的 RAW SOURCE 原文逐字貼入封包 RAW SOURCE 區塊。
4) 除非我明確要求，禁止新增封包以外的新段落。

------------------------------------------------------------
以下是目前的 PROJECT PACKET（若為首次可視為模板）：

{project_packet_val}

------------------------------------------------------------
以下是我提供的 RAW SOURCE（請逐字貼入封包 RAW SOURCE 區塊）：

{raw_source}

------------------------------------------------------------
請先完成解析，並更新封包的 PROJECT LOG（僅更新這些欄位）：
- 產品/計畫一句話總結
- 目標客群
- 核心價值主張（3–5點）
- 痛點（3–5點）
- 內容缺口（Information Gaps）
- 品牌語氣/禁忌/限制條件（若未提供請寫「未指定」）

最後：輸出「完整最新版 PROJECT PACKET v1」在單一 Markdown code block。
"""
        st.code(prompt1, language="markdown")

    st.divider()
    st.button("👉 前往下一步：Step 2", on_click=go_to_step, args=(1,), type="primary")

# ------------------------------------------
# Step 2
# ------------------------------------------
elif selected_step == STEPS[1]:
    st.markdown('<div class="main-header">✅ Step 2：SEO 任務目標 → 主題發想（寫入封包）</div>', unsafe_allow_html=True)
    st.caption("目標：主題發想 + 把 SEO 任務目標寫回封包，確保可攜帶續寫。")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="sub-header">📥 輸入</div>', unsafe_allow_html=True)
        p2_goal_input = st.text_area("SEO 任務目標（你希望這批文章達成什麼）", height=180, placeholder="例如：針對中小企業主，建立權威並導向諮詢/試用...", key="s2_goal")

    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        p2_goal = get_value(p2_goal_input, "任務目標")

        prompt2 = f"""以下是目前的 PROJECT PACKET（你必須只依賴封包作答）：

{project_packet_val}

【任務】
1) 依據封包的 PROJECT LOG + RAW SOURCE 背景，根據我提供的 SEO 任務目標產出 10–20 個可操作的主題方向（Topic Clusters），並以表格呈現：
| 主題方向 | 關鍵字類型 | 搜尋意圖類型 | 註解 |

2) 你必須更新封包：在 PROJECT LOG 中填入「SEO 任務目標」。

【硬性規則】
- 你必須輸出「完整最新版 PROJECT PACKET v1」於單一 Markdown code block。
- RAW SOURCE 區塊必須逐字原封不動回傳，不得改寫/摘要/重排/刪字。

SEO 任務目標：{p2_goal}
"""
        st.code(prompt2, language="markdown")

    st.divider()
    st.button("👉 前往下一步：Step 3", on_click=go_to_step, args=(2,), type="primary")

# ------------------------------------------
# Step 3
# ------------------------------------------
elif selected_step == STEPS[2]:
    st.markdown('<div class="main-header">✅ Step 3：關鍵字候選清單 (Pre-GKP)</div>', unsafe_allow_html=True)
    st.caption("目標：把 Topic 轉成可丟進 GKP 的關鍵字清單。這步通常不必更新封包。")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="sub-header">📥 輸入</div>', unsafe_allow_html=True)
        p3_topics = st.text_area("Step 2 產出的主題清單 / Topic Clusters", height=220, placeholder="貼上 Step2 的表格或主題清單...", key="s3_topics")

    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        topics_val = get_value(p3_topics, "主題清單")

        prompt3 = f"""以下是目前的 PROJECT PACKET（供背景，不要求更新封包也可）：

{project_packet_val}

請根據以下主題/Topic 清單，產出關鍵字候選清單，用於丟進 Google Keyword Planner (GKP)：

主題清單：
{topics_val}

請**嚴格**依照以下格式輸出（GKP 專用格式）：
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
        p4_data = st.text_area("GKP 輸出數據（貼表格/CSV文字）", height=320, placeholder="直接貼上 GKP 表格或 CSV 文字...", key="s4_gkp")

    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        gkp_val = get_value(p4_data, "GKP 輸出資料")

        prompt4 = f"""以下是目前的 PROJECT PACKET：

{project_packet_val}

請根據以下 GKP 數據，決定關鍵字策略，並更新封包 STRATEGY LOG（Primary/Secondary/Supporting）。

GKP 數據：
{gkp_val}

請輸出分析：
1) Primary Keyword（含數據與理由）
2) Secondary Keywords（含用途）
3) Supporting Keywords
4) 策略邏輯說明（流量 vs 競爭度取捨）
5) 後續 SERP 分析建議（帶出你要看什麼）

【硬性規則】
- 你必須輸出「完整最新版 PROJECT PACKET v1」於單一 Markdown code block。
- RAW SOURCE 區塊必須逐字原封不動回傳。
"""
        st.code(prompt4, language="markdown")

    st.divider()
    st.button("👉 前往下一步：Step 5", on_click=go_to_step, args=(4,), type="primary")

# ------------------------------------------
# Step 5
# ------------------------------------------
elif selected_step == STEPS[4]:
    st.markdown('<div class="main-header">✅ Step 5：搜尋意圖 Deep Research（建議寫入封包）</div>', unsafe_allow_html=True)
    st.caption("目標：SERP 真實戰況 + 深層意圖洞察。建議把 Winning Angle 與洞察摘要寫回封包 STRATEGY LOG。")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="sub-header">📥 輸入</div>', unsafe_allow_html=True)
        p5_keywords = st.text_area(
            "核心關鍵字（可貼 Primary + 重要 Secondary）",
            height=180,
            placeholder="例如：\nB群 什麼時候吃\nB群 空腹\n上班族 疲勞 補充品",
            key="s5_kw"
        )

    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        kw_val = get_value(p5_keywords, "核心關鍵字")

        prompt5 = f"""以下是目前的 PROJECT PACKET：

{project_packet_val}

請針對以下「核心關鍵字」執行 Deep Research（需實際搜索 SERP 前 10–20 名）：
關鍵字：{kw_val}

請依六大區塊輸出：
【一】SERP 真實戰況分析（Explicit Intent）
【二】SERP 隱性意圖（Implicit Intent）
【三】情境化意圖（Contextual Intent）
【四】未被滿足的深層意圖（差異化切入點）
【五】需求生成式意圖（Demand-Gen）
【六】意圖全景摘要（5–7 主軸意圖 + Winning Angle）

【封包更新要求（建議執行）】
- 請把「SERP/Intent 洞察摘要（Winning Angle）」與「差異化切入點」寫回封包 STRATEGY LOG。

【硬性規則】
- 你必須輸出「完整最新版 PROJECT PACKET v1」於單一 Markdown code block。
- RAW SOURCE 區塊必須逐字原封不動回傳。
"""
        st.code(prompt5, language="markdown")

    st.divider()
    st.button("👉 前往下一步：Step 6", on_click=go_to_step, args=(5,), type="primary")

# ------------------------------------------
# Step 6
# ------------------------------------------
elif selected_step == STEPS[5]:
    st.markdown('<div class="main-header">✅ Step 6：文章標題生成（寫入封包：Backlog/文章卡）</div>', unsafe_allow_html=True)
    st.caption("目標：產出標題池（Backlog）+ 建議分群與寫作順序；必要時建立多張文章卡。")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="sub-header">📥 輸入</div>', unsafe_allow_html=True)
        p6_intent = st.text_area("Step5 的意圖分析結果（或直接依封包 Strategy Log）", height=220, key="s6_intent")

    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        intent_val = get_value(p6_intent, "可留空（以封包 STRATEGY LOG 為準）")

        prompt6 = f"""以下是目前的 PROJECT PACKET：

{project_packet_val}

若你需要補充參考，這是額外的意圖分析內容（可忽略，以封包為主）：
{intent_val}

【任務】
1) 產出 15–25 個文章標題，分為：
   - 資訊型
   - 比較/選擇型
   - 行動導向型
   要求：融入 Primary Keyword、有點擊動機、不重複。

2) 請把標題寫入封包的 CONTENT QUEUE -> [Backlog Titles]，每行一個標題。

3) 請將標題做 3–5 個 Cluster，並給「建議寫作順序」（先 pillar 後 supporting）。

4) 請在封包 [Article Cards] 中，至少建立 3 張新文章卡（A01/A02/A03 或延續既有編號），每張卡先填：
   - 文章ID
   - 標題
   - Primary/Secondary/Supporting（若封包已有，按 cluster 分配）
   - Winning Angle（從封包 STRATEGY LOG 套用到各卡）

【硬性規則】
- 你必須輸出「完整最新版 PROJECT PACKET v1」於單一 Markdown code block。
- RAW SOURCE 區塊必須逐字原封不動回傳。
"""
        st.code(prompt6, language="markdown")

    st.divider()
    st.button("👉 前往下一步：Step 7", on_click=go_to_step, args=(6,), type="primary")

# ------------------------------------------
# Step 7
# ------------------------------------------
elif selected_step == STEPS[6]:
    st.markdown('<div class="main-header">✅ Step 7：文章大綱（更新指定文章卡）</div>', unsafe_allow_html=True)
    st.caption("目標：只更新你指定的文章ID那張卡（避免污染其他文章）。")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="sub-header">📥 輸入</div>', unsafe_allow_html=True)
        p7_article_id = st.text_input("要更新的文章ID（建議與側欄一致）", value=st.session_state.get("current_article_id", "A01"), key="s7_aid")
        p7_title = st.text_input("要寫的大綱標題（可選填，若封包文章卡已有可留空）", value=st.session_state.get("current_title", ""), key="s7_title")

    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        aid_val = get_value(p7_article_id, "A01")
        title_val = get_value(p7_title, "（若封包該文章卡已有標題可留空）")

        prompt7 = f"""以下是目前的 PROJECT PACKET：

{project_packet_val}

【任務】
- 請針對文章ID：{aid_val} 生成文章大綱（H1/H2/H3），並把大綱寫回封包該文章卡的「大綱（H1/H2/H3）」欄位。
- 若我有提供標題：{title_val}，請以此為準；若未提供，請從封包該文章卡的標題欄位讀取。

【要求】
1) 結構：H1, H2, H3
2) 每個 H2 必須對應明確使用者問題（以意圖洞察對齊）
3) 附上大綱邏輯簡述（放在該文章卡內「產出備註/連結」欄位即可）

【硬性規則】
- 你必須輸出「完整最新版 PROJECT PACKET v1」於單一 Markdown code block。
- RAW SOURCE 區塊必須逐字原封不動回傳。
- 只能更新該文章ID對應的文章卡；其他文章卡內容不得更動。
"""
        st.code(prompt7, language="markdown")

    st.divider()
    st.button("👉 前往下一步：Step 8", on_click=go_to_step, args=(7,), type="primary")

# ------------------------------------------
# Step 8
# ------------------------------------------
elif selected_step == STEPS[7]:
    st.markdown('<div class="main-header">✅ Step 8：文章撰寫 + 技術 SEO（更新指定文章卡）</div>', unsafe_allow_html=True)
    st.caption("目標：只依賴封包 + 指定文章卡完成寫作，並把產出寫回該卡（可攜帶續寫）。")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="sub-header">📥 寫作參數</div>', unsafe_allow_html=True)
        p8_article_id = st.text_input("要撰寫的文章ID（建議與側欄一致）", value=st.session_state.get("current_article_id", "A01"), key="s8_aid")
        p8_word = st.text_input("字數需求", value="1500 字", key="s8_word")
        p8_cta = st.text_input("CTA 文案", value="免費試用：https://example.com", key="s8_cta")

        st.markdown('<div class="sub-header">（可選填）補充指示</div>', unsafe_allow_html=True)
        p8_extra = st.text_area("補充寫作指示（例如：口吻、禁語、一定要提的段落）", height=140, key="s8_extra")

    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        aid_val = get_value(p8_article_id, "A01")
        word_val = get_value(p8_word, "1500字")
        cta_val = get_value(p8_cta, "CTA")
        extra_val = get_value(p8_extra, "（無）")

        prompt8 = f"""以下是目前的 PROJECT PACKET：

{project_packet_val}

【任務】
請只依賴封包內容，撰寫文章ID：{aid_val} 的完整文章。
- 字數：{word_val}
- CTA：{cta_val}
- 補充指示：{extra_val}

【產出要求（寫回該文章卡）】
請在該文章卡中更新/填入：
1) 完整文章（可放在「產出備註/連結」欄位內，或新增「正文」欄位也可，但必須在該文章卡範圍內）
2) Meta Title（<60字）
3) Meta Description（<160字）
4) Schema Markup 建議（條列）
5) 技術 SEO 檢查清單（條列：內鏈建議、段落結構、FAQ、表格/清單使用點）

【硬性規則】
- 你必須輸出「完整最新版 PROJECT PACKET v1」於單一 Markdown code block。
- RAW SOURCE 區塊必須逐字原封不動回傳。
- 只能更新該文章ID對應的文章卡；其他文章卡內容不得更動。
"""
        st.code(prompt8, language="markdown")

    st.divider()
    st.success("🎯 建議流程：每次只複製『最新版 Project Packet』到新對話，就能繼續寫下一篇（不怕對話變長劣化）。")
