import streamlit as st

# --- 頁面設定 ---
st.set_page_config(
    page_title="SEO 8-Step 戰略儀表板",
    page_icon="⚡",
    layout="wide"
)

# --- CSS 優化 ---
st.markdown("""
<style>
    .stTextArea textarea {
        font-family: monospace;
        font-size: 0.9rem;
        background-color: #f0f2f6;
    }
    h3 {
        color: #0066cc; /* 標題藍色強調 */
        font-size: 1.1rem;
        font-weight: 600;
    }
    .step-header {
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ SEO 8-Step 戰略儀表板 (GKP 強化版)")
st.caption("從主題發想、GKP 數據驗證到 SERP 深度研究的全流程 Prompt 生成器。")

# --- 輔助函式 ---
def get_value(input_val, placeholder_text):
    if input_val and str(input_val).strip():
        return str(input_val).strip()
    return f"[{placeholder_text}]"

# ==========================================
# 全流程共用：目前會議紀錄
# ==========================================
st.markdown("### 🧩 目前會議紀錄（全流程共用）")
meeting_log = st.text_area(
    "貼上上一輪 AI 產出的【會議紀錄】（或你調整後的版本）。第一次使用可留白，會在 Step 1 產出初版。",
    height=200,
    placeholder=(
        "建議格式：\n"
        "【會議紀錄】\n"
        "[一] 產品 / 計畫摘要\n"
        "- 一句話總結：\n"
        "- 目標客群：\n"
        "- 任務目標：\n"
        "- 核心價值主張：\n"
        "- 關鍵限制條件：\n\n"
        "[二] 關鍵字與搜尋意圖\n"
        "- 核心關鍵字：\n"
        "- 次要關鍵字：\n"
        "- 補充關鍵字：\n"
        "- 關鍵字策略重點：\n\n"
        "[三] 最終大綱\n"
        "- H1 / H2 / H3 結構：\n"
        "- 大綱設計邏輯："
    )
)
meeting_log_val = get_value(meeting_log, "目前尚無會議紀錄（由 Step 1 產生初版）")

st.divider()

# ==========================================
# Step 1: 產品 / 計畫解析
# ==========================================
st.markdown('<div class="step-header">✅ Step 1：產品 / 計畫解析</div>', unsafe_allow_html=True)
col1_s1, col2_s1 = st.columns([1, 1])

with col1_s1:
    p1_input = st.text_area(
        "Step 1 輸入：產品/計畫內容",
        height=200,
        placeholder="貼上你的產品說明、Landing Page 文案或計畫白皮書..."
    )

with col2_s1:
    st.markdown("### 📋 複製 Prompt")
    p1_content = get_value(p1_input, "內容貼在這裡")

    prompt1 = f"""以下是目前專案的會議紀錄（若為首次執行可忽略內容僅供參考）：
{meeting_log_val}

請先理解其中的專案背景、目標客群與任務目標，接著根據我提供的產品/計畫內容，進行條列式解析。

請依照以下格式輸出解析結果：

1. 一句話總結（What is it）
   • 用最精準的一句話描述產品/計畫是什麼。

2. 目標客群（Target User）
   • 列出 1–2 類主要客群
   • 若有次要客群也一併列出。

3. 核心價值主張（Value Proposition）
   • 列出 3–5 個最核心的價值
   • 每點需是明確的使用者利益。

4. 使用者痛點（Pain Points）
   • 明確列出這個產品/計畫要解決的問題。

5. 目前內容說明的缺口（Information Gaps）
   • 依照資訊架構角度，指出內容可能沒講清楚或需要補強的地方。

⸻
【會議紀錄輸出要求（重點）】

在完成上述解析後，請在回覆最下方額外輸出一個區塊：**完整的最新版會議紀錄**，格式如下：

【會議紀錄】
[一] 產品 / 計畫摘要
- 一句話總結（What is it）：
- 目標客群：
- 任務目標（這篇 SEO 文要達成什麼）：
- 整理後的核心價值主張（3–5 點）：
- 關鍵限制條件（語氣、禁用風格等）：若目前尚未指定，請先寫「尚未明確指定，可依一般專業語氣處理」。

[二] 關鍵字與搜尋意圖
- 請暫時寫：「尚未決定，待關鍵字決策步驟更新」。

[三] 最終大綱
- 請暫時寫：「尚未產出，待大綱步驟更新」。

請務必完整輸出上述三個區塊，這份【會議紀錄】將會在後續步驟中被覆蓋更新並重複使用。

⸻
以下是產品/計畫內容：
{p1_content}"""
    st.code(prompt1, language="markdown")

# ==========================================
# Step 2: 任務目標 → 主題發想
# ==========================================
st.markdown('<div class="step-header">✅ Step 2：任務目標 → 主題發想</div>', unsafe_allow_html=True)
col1_s2, col2_s2 = st.columns([1, 1])

with col1_s2:
    p2_input = st.text_area(
        "Step 2 輸入：SEO 任務目標",
        height=150,
        placeholder="例如：針對中小企業主，建立品牌權威並引導試用註冊..."
    )

with col2_s2:
    st.markdown("### 📋 複製 Prompt")
    p2_goal = get_value(p2_input, "任務目標")

    prompt2 = f"""以下是目前專案的會議紀錄：
{meeting_log_val}

請在理解上述背景的前提下，根據這篇 SEO 文章的任務目標進行主題發想。

以下是本次任務目標：
{p2_goal}

請根據這個目標，產出 10–20 個可操作的主題方向（Topic Clusters），並以表格方式呈現：

| 主題方向（Topic） | 關鍵字類型（核心/長尾/商業/資訊） | 搜尋意圖類型（資訊/商業/比較/交易） | 註解（為什麼適合此目標） |

要求：
• 與任務目標高度相關
• 涵蓋資訊意圖與商業意圖
• 主題之間不重複
• 儘量用「使用者會搜尋的語言」描述 Topic

本步驟僅需輸出主題表格，無須更新會議紀錄。"""
    st.code(prompt2, language="markdown")

# ==========================================
# Step 3: 關鍵字候選清單（給 GKP 用）
# ==========================================
st.markdown('<div class="step-header">✅ Step 3：關鍵字候選清單 (Pre-GKP)</div>', unsafe_allow_html=True)
col1_s3, col2_s3 = st.columns([1, 1])

with col1_s3:
    p3_input = st.text_area(
        "Step 3 輸入：Step 2 產出的主題清單",
        height=150,
        placeholder="貼上 AI 剛剛產生的主題方向/Topic 清單..."
    )

with col2_s3:
    st.markdown("### 📋 複製 Prompt")
    p3_list = get_value(p3_input, "主題清單")

    prompt3 = f"""以下是目前專案的會議紀錄：
{meeting_log_val}

請在理解專案背景與任務目標的前提下，根據以下主題/Topic 清單，產出關鍵字候選清單，用於丟進 Google 關鍵字規劃工具 (GKP) 測量數據。

以下是前一步整理出的主題/Topic 清單：
{p3_list}

請**嚴格**依照以下格式輸出，方便我直接複製至 GKP：

1. 格式要求：純文字清單，**關鍵字之間請用「英文逗號 (,)」分隔**。
2. 禁止事項：不要有編號 (1. 2.)、不要有項目符號 (-)、不要有任何解釋文字。
3. 分組優化：每 10 個關鍵字一組，組與組之間空一行。
4. 重要策略：請務必包含「最短的核心大字」（Seed Keywords），不要只給長尾詞。

輸出範例：
數位轉型, 企業轉型, 轉型策略, 數位化, 轉型顧問, 數位轉型定義, 數位轉型案例, 中小企業數位轉型, 數位轉型趨勢, 產業升級

工廠無紙化, 數位轉型失敗原因, 二代接班轉型, 數位轉型診斷, 企業轉型步驟, 傳產轉型, 數位行銷轉型, 組織變革, 數位工具, 雲端轉型

要求：
1. 產出至少 30–40 個關鍵字。
2. 前 5–10 個字必須是該主題流量可能最大的「核心大字」(Broad Terms)。
3. 接著列出中長尾詞、具體問題（如：如何...、流程...）、相關變體。
4. 使用使用者真實搜尋語句。

本步驟無須更新會議紀錄，只需輸出關鍵字清單。"""
    st.code(prompt3, language="markdown")

# ==========================================
# Step 4: GKP 資料 → 決定核心關鍵字（會議紀錄 [二] 的主要更新點）
# ==========================================
st.markdown('<div class="step-header">✅ Step 4：GKP 數據決策 (Post-GKP)</div>', unsafe_allow_html=True)
col1_s4, col2_s4 = st.columns([1, 1])

with col1_s4:
    p4_input = st.text_area(
        "Step 4 輸入：Google 關鍵字規劃工具的數據",
        height=200,
        placeholder="直接貼上 GKP 的 CSV 內容，或複製表格數據..."
    )

with col2_s4:
    st.markdown("### 📋 複製 Prompt")
    p4_data = get_value(p4_input, "GKP 輸出資料")

    prompt4 = f"""以下是目前專案的會議紀錄：
{meeting_log_val}

請在理解產品/計畫摘要與任務目標的前提下，根據以下 Google 關鍵字規劃工具 (GKP) 的輸出資料，決定本篇 SEO 文章的關鍵字策略，並更新會議紀錄中關於「關鍵字與搜尋意圖」的部分。

以下是 GKP 輸出資料（包含關鍵字、平均每月搜尋量、競爭度、出價區間等）：
{p4_data}

請依照下列格式輸出分析結果：

⸻
1. 核心關鍵字（Primary Keywords）
• 1–3 個
• 附上每個的搜尋量、競爭度
• 說明為何適合作為本篇文章主要優化目標
• 說明與任務目標的關聯度

⸻
2. 次要關鍵字（Secondary Keywords）
• 5–8 個
• 說明用途（例如：補長尾、對特定族群、補意圖深度）
• 說明放在次要層級的理由

⸻
3. 補充關鍵字（Supporting Keywords）
• 3–5 個
• 適合用於 FAQ、補充段落或案例
• 說明「為何不是主關鍵字但仍值得包含」

⸻
4. 策略邏輯說明
請解釋：
• 你如何在「搜尋量 vs 競爭度」之間做取捨
• 為何建議本篇文章鎖定這幾組核心關鍵字
• 若流量/競爭度矛盾時，你如何做決策

⸻
5. 後續搜尋意圖分析建議
請指出：
• 接下來 SERP Deep Research（下一步）應優先深入分析哪 1–2 個核心關鍵字
• 以及理由

⸻
【會議紀錄更新要求（重點）】

假設目前已有一份舊的會議紀錄（即上方所示），請在本次回覆最下方，輸出一份「更新後的完整會議紀錄」，格式如下：

【會議紀錄】
[一] 產品 / 計畫摘要
- 若與舊版相同可重寫同樣內容；如有需要調整請直接修正後寫出完整版本。

[二] 關鍵字與搜尋意圖
- 核心關鍵字（Primary）：列出每個關鍵字，並標註搜尋量、競爭度、主要搜尋意圖。
- 次要關鍵字（Secondary）：同上。
- 補充關鍵字（Supporting）：列出並簡述用途。
- 關鍵字策略重點：整理 3–5 點條列說明。

[三] 最終大綱
- 仍可暫時保留「尚未產出，待大綱步驟更新」。

請注意：
- 這份【會議紀錄】將覆蓋舊版本，請務必寫成一份完整、可獨立閱讀的文件。
- 不要只寫「同上」，請把該寫的內容完整寫出。"""
    st.code(prompt4, language="markdown")

# ==========================================
# Step 5: 搜尋意圖 Deep Research
# ==========================================
st.markdown('<div class="step-header">✅ Step 5：搜尋意圖 SERP Deep Research</div>', unsafe_allow_html=True)
col1_s5, col2_s5 = st.columns([1, 1])

with col1_s5:
    p5_input = st.text_area(
        "Step 5 輸入：Step 4 選定的核心關鍵字",
        height=150,
        placeholder="例如：\n核心關鍵字A\n核心關鍵字B"
    )

with col2_s5:
    st.markdown("### 📋 複製 Prompt")
    p5_keywords = get_value(p5_input, "核心關鍵字")

    prompt5 = f"""以下是目前專案的會議紀錄：
{meeting_log_val}

請在理解產品摘要與目前關鍵字策略的前提下，對以下核心關鍵字進行 SERP Deep Research：
{p5_keywords}

請完成以下內容：

⸻
1. 研究 Google 前 20 筆結果的標題
• 至少列出 10 種常見標題模式
• 標記內容形式（教學 / 比較 / 介紹 / FAQ / 官方說明 / 心得）

⸻
2. 搜尋意圖推論
• 主要意圖（1 個）
• 次要意圖（1–3 個）
• 隱性需求（使用者會關心但不會直接搜尋）

⸻
3. 競爭者內容缺口（Content Gap）
• SERP 現在沒有，但使用者會想知道的內容
• 競爭者普遍弱的地方
• 適合我在文章中補強的段落

⸻
請按「每個關鍵字」獨立分段輸出。

本步驟無須重新輸出會議紀錄，只需給出 SERP 研究結果。"""
    st.code(prompt5, language="markdown")

# ==========================================
# Step 6: 文章標題生成
# ==========================================
st.markdown('<div class="step-header">✅ Step 6：文章標題生成</div>', unsafe_allow_html=True)
col1_s6, col2_s6 = st.columns([1, 1])

with col1_s6:
    p6_input = st.text_area(
        "Step 6 輸入：搜尋意圖分析結果",
        height=150,
        placeholder="貼上 Step 5 的意圖分析與缺口分析..."
    )

with col2_s6:
    st.markdown("### 📋 複製 Prompt")
    p6_intent = get_value(p6_input, "搜尋意圖結果")

    prompt6 = f"""以下是目前專案的會議紀錄：
{meeting_log_val}

請在理解產品摘要、關鍵字策略與既有搜尋意圖的前提下，根據以下搜尋意圖分析結果，設計本篇文章的標題選項：
{p6_intent}

請根據這些意圖綜合上述所有分析，產出 15–20 個 SEO 文章標題，並分成三類：

⸻
1. 資訊型（Information Intent）

2. 比較型 / 選擇型（Comparison Intent）

3. 行動導向型（Transactional / CTA Intent）

⸻
要求：
• 必須融入核心關鍵字
• 有明顯點擊動機（但不浮誇）
• 每個標題彼此不重複
• 各類型至少 5 個以上

本步驟可僅輸出標題列表，暫不強制更新會議紀錄。"""
    st.code(prompt6, language="markdown")

# ==========================================
# Step 7: 文章大綱（會議紀錄 [三] 的更新點）
# ==========================================
st.markdown('<div class="step-header">✅ Step 7：文章大綱</div>', unsafe_allow_html=True)
col1_s7, col2_s7 = st.columns([1, 1])

with col1_s7:
    p7_input = st.text_input(
        "Step 7 輸入：最終選擇的文章標題",
        placeholder="輸入你選好的那個標題..."
    )

with col2_s7:
    st.markdown("### 📋 複製 Prompt")
    p7_title = get_value(p7_input, "最終標題")

    prompt7 = f"""以下是目前專案的會議紀錄：
{meeting_log_val}

請在理解產品摘要與關鍵字策略的前提下，根據以下最終選擇的文章標題，產出完整 SEO 大綱，並更新會議紀錄中的「最終大綱」區塊。

以下是我選擇的文章標題：
{p7_title}

請依照以下要求輸出大綱：

⸻
1. 整體結構
• H1：文章標題
• H2：主節點 5–7 個
• H3：每個 H2 下的子節點 2–4 個

⸻
2. 每個 H2 必須回答一個「明確的使用者問題」
• 問題需與搜尋意圖吻合
• 問題需是使用者會問的自然語句

⸻
3. 文章邏輯解說（寫在大綱後）
必須包含：
• 本大綱如何對應搜尋意圖
• 內容如何覆蓋主要與次要關鍵字
• 文章如何避免淪為通用內容（差異化策略）

⸻
【會議紀錄更新要求（重點）】

請在本次回覆最下方，輸出一份「更新後的完整會議紀錄」，格式如下：

【會議紀錄】
[一] 產品 / 計畫摘要
- 依照目前最新理解，重新寫出完整內容（如與舊版相同可沿用，但請重新寫出）。

[二] 關鍵字與搜尋意圖
- 沿用上一步關鍵字決策的內容，如有因大綱設計而有任何調整請一併修正後寫出完整版本。

[三] 最終大綱
- H1：最終標題
- H2 / H3 結構：完整列出
- 大綱設計邏輯：條列 3–5 點說明大綱如何對應搜尋意圖與關鍵字策略。

請注意：
- 這份【會議紀錄】將作為 Step 8 寫作與未來所有改版的基準，請務必寫成一份完整、可獨立閱讀的文件。"""
    st.code(prompt7, language="markdown")

# ==========================================
# Step 8: 文章撰寫 + 技術 SEO
# ==========================================
st.markdown('<div class="step-header">✅ Step 8：文章撰寫 + 技術 SEO</div>', unsafe_allow_html=True)
col1_s8, col2_s8 = st.columns([1, 1])

with col1_s8:
    p8_word = st.text_input("文章字數需求：", value="1500 字")
    p8_cta = st.text_input("CTA 文案與連結：", value="免費試用：https://example.com")
    p8_outline = st.text_area(
        "Step 8 輸入：確認後的完整大綱",
        height=200,
        placeholder="貼上 Step 7 的完整大綱（或會議紀錄中 [三] 的大綱部分）..."
    )

with col2_s8:
    st.markdown("### 📋 複製 Prompt")
    p8_title_final = get_value(p7_input, "最終標題")
    p8_outline_final = get_value(p8_outline, "完整大綱")

    prompt8 = f"""以下是目前專案的會議紀錄：
{meeting_log_val}

請在完整理解會議紀錄（尤其是關鍵字策略與最終大綱）的前提下，根據以下資訊撰寫文章：

• 標題：{p8_title_final}
• 文章字數：{p8_word}
• CTA：{p8_cta}
• 大綱：{p8_outline_final}

請完成：

⸻
寫作要求
1. 語氣專業、清楚、不浮誇
2. 避免行銷腔調
3. 內容需能回答搜尋意圖
4. 每段落保持結構與邏輯
5. 自然融入次要與補充關鍵字
6. 文章需可直接上線使用

⸻
文章完成後，請額外輸出以下 SEO 元件：

1. Meta Title
• ≤ 60 字元
• 必須包含核心關鍵字
• 具有點擊誘因

2. Meta Description
• ≤ 160 字元
• 必須包含核心關鍵字
• 結尾需帶 CTA（例如：立即了解 / 點擊查看更多）

3. Schema Markup 建議
請提出適合本文的 Schema 類型，並說明：
• 選擇理由
• 對 SEO 或 CTR 的幫助
• 若是 FAQPage 或 HowTo，需提供建議的 Question/Answer 或步驟標題

本步驟主要依賴既有的【會議紀錄】，可不必再次輸出更新版會議紀錄；若你認為有關鍵調整，也可以在最後補充「建議更新會議紀錄的說明」。"""
    st.code(prompt8, language="markdown")

# --- 底部 ---
st.divider()
st.info("💡 建議流程：在 Step 1、Step 4、Step 7 執行後，將 AI 回覆中的【會議紀錄】整理成你認可的版本，貼回最上方欄位，讓後續所有步驟都能在斷線或另開對話時延續同一份決策脈絡。")
