import streamlit as st

# ==========================================
# 1. 頁面基礎設定
# ==========================================
st.set_page_config(
    page_title="SEO 8-Step 戰略儀表板",
    page_icon="⚡",
    layout="wide"
)

# ==========================================
# 2. CSS 優化 (針對側邊欄與閱讀體驗)
# ==========================================
st.markdown("""
<style>
    /* 輸入框字體優化 */
    .stTextArea textarea {
        font-family: "Consolas", "Monaco", monospace;
        font-size: 0.95rem;
        background-color: #f8f9fa;
        color: #333;
    }
    /* 主標題樣式 */
    .main-header {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1E3A8A; /* 深藍色 */
        border-bottom: 2px solid #eee;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    /* 副標題樣式 */
    .sub-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #2563EB; /* 亮藍色 */
        margin-top: 10px;
        margin-bottom: 5px;
    }
    /* 調整側邊欄頂部間距 */
    .css-1d391kg {
        padding-top: 1rem;
    }
    /* 優化按鈕間距 */
    .stButton button {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 輔助函式與全域變數
# ==========================================
# 定義步驟清單，供導航使用
STEPS = [
    "Step 1: 產品 / 計畫解析",
    "Step 2: 任務目標 → 主題發想",
    "Step 3: 關鍵字候選清單 (Pre-GKP)",
    "Step 4: GKP 數據決策 (Post-GKP)",
    "Step 5: 搜尋意圖 Deep Research",
    "Step 6: 文章標題生成",
    "Step 7: 文章大綱",
    "Step 8: 文章撰寫 + 技術 SEO"
]

def get_value(input_val, placeholder_text):
    """
    如果使用者有輸入內容，則回傳內容；
    若無，則回傳預設佔位符，方便 Prompt 閱讀。
    """
    if input_val and str(input_val).strip():
        return str(input_val).strip()
    return f"[{placeholder_text}]"

def go_to_step(step_index):
    """
    用於切換步驟的 Callback 函式
    """
    if 0 <= step_index < len(STEPS):
        st.session_state.nav_radio = STEPS[step_index]

# ==========================================
# 4. SIDEBAR：導覽與記憶核心
# ==========================================
with st.sidebar:
    st.title("⚡ SEO 戰略中控")
    
    # --- A. 步驟導覽 ---
    st.subheader("📍 步驟導覽")
    
    # 確保 session state 中有 nav_radio 變數
    if "nav_radio" not in st.session_state:
        st.session_state.nav_radio = STEPS[0]

    selected_step = st.radio(
        "選擇當前進度：",
        STEPS,
        index=0,
        key="nav_radio"  # 綁定 key 以便透過按鈕控制
    )
    
    st.divider()

    # --- B. 全局脈絡 (會議紀錄) ---
    st.subheader("🧠 戰略大腦 (會議紀錄)")
    st.info("💡 提示：請點擊 AI 回覆中代碼區塊右上角的「Copy」按鈕，再貼回下方。")
    
    # key="global_meeting_log" 確保切換頁面時內容不流失
    meeting_log = st.text_area(
        "目前會議紀錄內容",
        height=400,
        key="global_meeting_log",
        placeholder=(
            "建議格式：\n"
            "【會議紀錄】\n"
            "[一] 產品 / 計畫摘要\n...\n"
            "[二] 關鍵字與搜尋意圖\n...\n"
            "[三] 最終大綱\n..."
        )
    )
    meeting_log_val = get_value(meeting_log, "目前尚無會議紀錄（由 Step 1 產生初版）")

# ==========================================
# 5. 主畫面邏輯 (根據 Sidebar 選擇渲染內容)
# ==========================================

# ------------------------------------------
# Step 1 頁面
# ------------------------------------------
if selected_step == STEPS[0]:
    st.markdown('<div class="main-header">✅ Step 1：產品 / 計畫解析</div>', unsafe_allow_html=True)
    st.caption("目標：將原本零散的產品資訊或白皮書，轉化為結構化的 SEO 專案摘要。")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="sub-header">📥 輸入資料</div>', unsafe_allow_html=True)
        # key="s1_input" 確保切換頁面後輸入內容不消失
        p1_input = st.text_area("產品/計畫內容", height=300, placeholder="貼上你的產品說明、Landing Page 文案...", key="s1_input")
        
    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        p1_content = get_value(p1_input, "內容貼在這裡")
        
        prompt1 = f"""以下是目前專案的會議紀錄（若為首次執行可忽略內容僅供參考）：
{meeting_log_val}

請先理解其中的專案背景、目標客群與任務目標，接著根據我提供的產品/計畫內容，進行條列式解析。

請依照以下格式輸出解析結果：
1. 一句話總結（What is it）
2. 目標客群（Target User）
3. 核心價值主張（Value Proposition）
4. 使用者痛點（Pain Points）
5. 目前內容說明的缺口（Information Gaps）

⸻
**【輸出格式強制要求：Markdown Code Block】**

在完成解析後，請務必將「完整的最新版會議紀錄」獨立輸出在一個 **Markdown 代碼區塊** 中，格式必須如下所示（請嚴格遵守，方便我一鍵複製）：

```markdown
【會議紀錄】
[一] 產品 / 計畫摘要
- 一句話總結（What is it）：
- 目標客群：
- 任務目標（這篇 SEO 文要達成什麼）：
- 整理後的核心價值主張（3–5 點）：
- 關鍵限制條件：若目前尚未指定，請先寫「尚未明確指定，可依一般專業語氣處理」。

[二] 關鍵字與搜尋意圖
- 請暫時寫：「尚未決定，待關鍵字決策步驟更新」。

[三] 最終大綱
- 請暫時寫：「尚未產出，待大綱步驟更新」。
```

請注意：**務必使用三個反引號 (```) 包覆會議紀錄內容。**

⸻
以下是產品/計畫內容：
{p1_content}"""
        st.code(prompt1, language="markdown")
    
    # 底部導航按鈕
    st.divider()
    st.button("👉 前往下一步：Step 2 (主題發想)", on_click=go_to_step, args=(1,), type="primary")

# ------------------------------------------
# Step 2 頁面
# ------------------------------------------
elif selected_step == STEPS[1]:
    st.markdown('<div class="main-header">✅ Step 2：任務目標 → 主題發想</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="sub-header">📥 輸入資料</div>', unsafe_allow_html=True)
        p2_input = st.text_area("SEO 任務目標", height=200, placeholder="例如：針對中小企業主，建立品牌權威並引導試用註冊...", key="s2_input")
        
    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        p2_goal = get_value(p2_input, "任務目標")
        prompt2 = f"""以下是目前專案的會議紀錄：
{meeting_log_val}

請在理解上述背景的前提下，根據這篇 SEO 文章的任務目標進行主題發想。
任務目標：{p2_goal}

請產出 10–20 個可操作的主題方向（Topic Clusters），並以表格呈現：
| 主題方向 | 關鍵字類型 | 搜尋意圖類型 | 註解 |

本步驟僅需輸出主題表格，無須更新會議紀錄。"""
        st.code(prompt2, language="markdown")
    
    # 底部導航按鈕
    st.divider()
    st.button("👉 前往下一步：Step 3 (關鍵字候選)", on_click=go_to_step, args=(2,), type="primary")

# ------------------------------------------
# Step 3 頁面
# ------------------------------------------
elif selected_step == STEPS[2]:
    st.markdown('<div class="main-header">✅ Step 3：關鍵字候選清單 (Pre-GKP)</div>', unsafe_allow_html=True)
    st.caption("目標：將發想出的主題，轉化為可以丟進 Google Keyword Planner 的格式。")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="sub-header">📥 輸入資料</div>', unsafe_allow_html=True)
        p3_input = st.text_area("Step 2 產出的主題清單", height=200, placeholder="貼上 AI 剛剛產生的主題方向/Topic 清單...", key="s3_input")
        
    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        p3_list = get_value(p3_input, "主題清單")
        prompt3 = f"""以下是目前專案的會議紀錄：
{meeting_log_val}

請根據以下主題/Topic 清單，產出關鍵字候選清單，用於丟進 Google 關鍵字規劃工具 (GKP)。
主題清單：{p3_list}

請**嚴格**依照以下格式輸出（GKP 專用格式）：
1. 純文字清單，**關鍵字之間請用「英文逗號 (,)」分隔**。
2. 不要編號、不要項目符號。
3. 每 10 個關鍵字一組，組與組之間空一行。
4. 務必包含「最短的核心大字」（Seed Keywords）與長尾詞。

本步驟無須更新會議紀錄。"""
        st.code(prompt3, language="markdown")
    
    # 底部導航按鈕
    st.divider()
    st.button("👉 前往下一步：Step 4 (GKP 決策)", on_click=go_to_step, args=(3,), type="primary")

# ------------------------------------------
# Step 4 頁面
# ------------------------------------------
elif selected_step == STEPS[3]:
    st.markdown('<div class="main-header">✅ Step 4：GKP 數據決策 (Post-GKP)</div>', unsafe_allow_html=True)
    st.caption("目標：這一步最重要。請根據真實數據（流量/競爭度）來鎖定核心關鍵字。")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="sub-header">📥 輸入資料</div>', unsafe_allow_html=True)
        p4_input = st.text_area("GKP 輸出數據", height=300, placeholder="直接貼上 GKP 的 CSV 內容，或複製表格數據...", key="s4_input")
        
    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        p4_data = get_value(p4_input, "GKP 輸出資料")
        
        prompt4 = f"""以下是目前專案的會議紀錄：
{meeting_log_val}

請根據以下 GKP 數據，決定本篇 SEO 文章的關鍵字策略，並更新會議紀錄。
GKP 數據：
{p4_data}

請依照下列格式輸出分析：
1. 核心關鍵字 (Primary) - 含數據與理由
2. 次要關鍵字 (Secondary) - 含用途
3. 補充關鍵字 (Supporting)
4. 策略邏輯說明 (流量 vs 競爭度取捨)
5. 後續 SERP 分析建議

⸻
**【輸出格式強制要求：Markdown Code Block】**

請務必將「更新後的完整會議紀錄」獨立輸出在一個 **Markdown 代碼區塊** 中，格式必須如下所示：

```markdown
【會議紀錄】
[一] 產品 / 計畫摘要 (保留或修正)
...

[二] 關鍵字與搜尋意圖 (請大幅更新此處，列出具體關鍵字策略)
...

[三] 最終大綱
- 尚未產出，待大綱步驟更新
```

請注意：**務必使用三個反引號 (```) 包覆會議紀錄內容，以便我直接複製。**"""
        st.code(prompt4, language="markdown")
    
    # 底部導航按鈕
    st.divider()
    st.button("👉 前往下一步：Step 5 (SERP 研究)", on_click=go_to_step, args=(4,), type="primary")

# ------------------------------------------
# Step 5 頁面
# ------------------------------------------
elif selected_step == STEPS[4]:
    st.markdown('<div class="main-header">✅ Step 5：搜尋意圖 SERP Deep Research</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="sub-header">📥 輸入資料</div>', unsafe_allow_html=True)
        p5_input = st.text_area("Step 4 選定的核心關鍵字", height=200, key="s5_input")
        
    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        p5_keywords = get_value(p5_input, "核心關鍵字")
        prompt5 = f"""以下是目前專案的會議紀錄：
{meeting_log_val}

請對以下核心關鍵字進行 SERP Deep Research：
{p5_keywords}

請完成：
1. 研究 Google 前 20 筆結果的標題模式
2. 搜尋意圖推論 (主要/次要/隱性)
3. 競爭者內容缺口 (Content Gap)

本步驟無須更新會議紀錄。"""
        st.code(prompt5, language="markdown")
    
    # 底部導航按鈕
    st.divider()
    st.button("👉 前往下一步：Step 6 (標題生成)", on_click=go_to_step, args=(5,), type="primary")

# ------------------------------------------
# Step 6 頁面
# ------------------------------------------
elif selected_step == STEPS[5]:
    st.markdown('<div class="main-header">✅ Step 6：文章標題生成</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="sub-header">📥 輸入資料</div>', unsafe_allow_html=True)
        p6_input = st.text_area("Step 5 意圖分析結果", height=200, key="s6_input")
        
    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        p6_intent = get_value(p6_input, "搜尋意圖結果")
        prompt6 = f"""以下是目前專案的會議紀錄：
{meeting_log_val}

根據以下搜尋意圖分析結果，設計文章標題：
{p6_intent}

請產出 15-20 個標題，分為：
1. 資訊型
2. 比較型 / 選擇型
3. 行動導向型

要求：融入核心關鍵字、有點擊動機、不重複。"""
        st.code(prompt6, language="markdown")
    
    # 底部導航按鈕
    st.divider()
    st.button("👉 前往下一步：Step 7 (文章大綱)", on_click=go_to_step, args=(6,), type="primary")

# ------------------------------------------
# Step 7 頁面
# ------------------------------------------
elif selected_step == STEPS[6]:
    st.markdown('<div class="main-header">✅ Step 7：文章大綱</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="sub-header">📥 輸入資料</div>', unsafe_allow_html=True)
        p7_input = st.text_input("最終選擇的文章標題", key="s7_input")
        
    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        p7_title = get_value(p7_input, "最終標題")
        
        prompt7 = f"""以下是目前專案的會議紀錄：
{meeting_log_val}

根據最終標題產出大綱，並更新會議紀錄。
標題：{p7_title}

要求：
1. 結構：H1, H2 (主節點), H3 (子節點)
2. 每個 H2 需回答明確使用者問題
3. 附上大綱邏輯解說 (如何對應意圖)

⸻
**【輸出格式強制要求：Markdown Code Block】**

請務必將「更新後的完整會議紀錄」獨立輸出在一個 **Markdown 代碼區塊** 中，格式必須如下所示：

```markdown
【會議紀錄】
[一] 產品 / 計畫摘要 (完整版)
...

[二] 關鍵字與搜尋意圖 (完整版)
...

[三] 最終大綱 (請更新此處，包含 H1/H2/H3 結構與邏輯)
...
```

請注意：**務必使用三個反引號 (```) 包覆會議紀錄內容，以便我直接複製。**"""
        st.code(prompt7, language="markdown")
    
    # 底部導航按鈕
    st.divider()
    st.button("👉 前往下一步：Step 8 (撰寫 + 技術 SEO)", on_click=go_to_step, args=(7,), type="primary")

# ------------------------------------------
# Step 8 頁面
# ------------------------------------------
elif selected_step == STEPS[7]:
    st.markdown('<div class="main-header">✅ Step 8：文章撰寫 + 技術 SEO</div>', unsafe_allow_html=True)
    st.caption("目標：這是最後一步，結合所有決策進行寫作。")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="sub-header">📥 輸入資料</div>', unsafe_allow_html=True)
        p8_word = st.text_input("字數需求", value="1500 字", key="s8_word")
        p8_cta = st.text_input("CTA 文案", value="免費試用：[https://example.com](https://example.com)", key="s8_cta")
        p8_outline = st.text_area("確認後的完整大綱", height=200, placeholder="若會議紀錄已有大綱，此處可選填...", key="s8_outline")
        
    with col2:
        st.markdown('<div class="sub-header">📤 複製 Prompt</div>', unsafe_allow_html=True)
        # 注意：使用 session_state 抓取跨頁面的變數 (因為切換頁面後，Step 7 的輸入框已消失，只能從記憶體抓)
        p8_title_final = get_value(st.session_state.get("s7_input", ""), "最終標題(請回Step7輸入)") 
        p8_outline_final = get_value(p8_outline, "完整大綱 (以會議紀錄為主)")
        
        prompt8 = f"""以下是目前專案的會議紀錄：
{meeting_log_val}

請根據會議紀錄撰寫文章。
• 標題：{p8_title_final}
• 字數：{p8_word}
• CTA：{p8_cta}
• 補充大綱指示：{p8_outline_final}

產出：
1. 完整文章 (專業語氣、結構清晰)
2. Meta Title (<60字元)
3. Meta Description (<160字元)
4. Schema Markup 建議"""
        st.code(prompt8, language="markdown")
    
    st.divider()
    st.success("🎉 全流程結束！請確認您已保存所有產出內容。")
