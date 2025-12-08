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
    if input_val and input_val.strip():
        return input_val.strip()
    return f"[{placeholder_text}]"

# ==========================================
# Step 1: 產品 / 計畫解析
# ==========================================
st.markdown('<div class="step-header">✅ Step 1：產品 / 計畫解析</div>', unsafe_allow_html=True)
col1_s1, col2_s1 = st.columns([1, 1])

with col1_s1:
    p1_input = st.text_area("Step 1 輸入：產品/計畫內容", height=200, placeholder="貼上你的產品說明、Landing Page 文案或計畫白皮書...")

with col2_s1:
    st.markdown("### 📋 複製 Prompt")
    p1_content = get_value(p1_input, "內容貼在這裡")
    
    prompt1 = f"""請根據我提供的產品/計畫內容，進行條列式解析。

請依照以下格式輸出：
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

以下是產品/計畫內容：
{p1_content}"""
    st.code(prompt1, language="markdown")

# ==========================================
# Step 2: 任務目標 → 主題發想
# ==========================================
st.markdown('<div class="step-header">✅ Step 2：任務目標 → 主題發想</div>', unsafe_allow_html=True)
col1_s2, col2_s2 = st.columns([1, 1])

with col1_s2:
    p2_input = st.text_area("Step 2 輸入：SEO 任務目標", height=150, placeholder="例如：針對中小企業主，建立品牌權威並引導試用註冊...")

with col2_s2:
    st.markdown("### 📋 複製 Prompt")
    p2_goal = get_value(p2_input, "任務目標")
    
    prompt2 = f"""以下是我這篇 SEO 文章的任務目標：
{p2_goal}

請根據這個目標，產出 10–20 個可操作的主題方向（Topic Clusters），並以表格方式呈現：

| 主題方向（Topic） | 關鍵字類型（核心/長尾/商業/資訊） | 搜尋意圖類型（資訊/商業/比較/交易） | 註解（為什麼適合此目標） |

要求：
• 與任務目標高度相關
• 涵蓋資訊意圖與商業意圖
• 主題之間不重複
• 儘量用「使用者會搜尋的語言」描述 Topic"""
    st.code(prompt2, language="markdown")

# ==========================================
# Step 3: 關鍵字候選清單（給 GKP 用）
# ==========================================
st.markdown('<div class="step-header">✅ Step 3：關鍵字候選清單 (Pre-GKP)</div>', unsafe_allow_html=True)
col1_s3, col2_s3 = st.columns([1, 1])

with col1_s3:
    p3_input = st.text_area("Step 3 輸入：Step 2 產出的主題清單", height=150, placeholder="貼上 AI 剛剛產生的主題方向/Topic 清單...")

with col2_s3:
    st.markdown("### 📋 複製 Prompt")
    p3_list = get_value(p3_input, "主題清單")
    
    prompt3 = f"""以下是我們前一步整理出的主題/Topic 清單：
{p3_list}

請根據這些主題，幫我產出一份「關鍵字候選清單」，目的是丟進 Google 關鍵字規劃工具 (GKP) 測量數據。

請**嚴格**依照以下格式輸出，方便我直接複製：

1. **格式要求**：純文字清單，**每個關鍵字必須獨立一行** (One keyword per line)。
2. **禁止事項**：不要有編號 (1. 2.)、不要有項目符號 (-)、不要有逗號分隔、不要有任何解釋文字。
3. **分組優化**：每 10 個關鍵字一組，組與組之間空一行，方便分批複製。

輸出範例：
關鍵字A
關鍵字B
關鍵字C
...
關鍵字J

關鍵字K
關鍵字L
...

要求：
1. 產出至少 30-40 個關鍵字。
2. 包含核心詞、長尾詞、變體與問題型搜尋。
3. 使用使用者真實搜尋語句。"""
    st.code(prompt3, language="markdown")

# ==========================================
# Step 4: GKP 資料 → 決定核心關鍵字
# ==========================================
st.markdown('<div class="step-header">✅ Step 4：GKP 數據決策 (Post-GKP)</div>', unsafe_allow_html=True)
col1_s4, col2_s4 = st.columns([1, 1])

with col1_s4:
    p4_input = st.text_area("Step 4 輸入：Google 關鍵字規劃工具的數據", height=200, placeholder="直接貼上 GKP 的 CSV 內容，或複製表格數據...")

with col2_s4:
    st.markdown("### 📋 複製 Prompt")
    p4_data = get_value(p4_input, "GKP 輸出資料")
    
    prompt4 = f"""以下是 Google 關鍵字規劃工具的輸出資料（包含關鍵字、平均每月搜尋量、競爭度、出價區間等）：
{p4_data}

請依據這些數據，幫我完成本篇 SEO 文章的關鍵字策略分級。

請依照下列格式輸出：

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
• 說明 “為何不是主關鍵字但仍值得包含”

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
• 以及理由"""
    st.code(prompt4, language="markdown")

# ==========================================
# Step 5: 搜尋意圖 Deep Research
# ==========================================
st.markdown('<div class="step-header">✅ Step 5：搜尋意圖 SERP Deep Research</div>', unsafe_allow_html=True)
col1_s5, col2_s5 = st.columns([1, 1])

with col1_s5:
    p5_input = st.text_area("Step 5 輸入：Step 4 選定的核心關鍵字", height=150, placeholder="例如：\n核心關鍵字A\n核心關鍵字B")

with col2_s5:
    st.markdown("### 📋 複製 Prompt")
    p5_keywords = get_value(p5_input, "核心關鍵字")
    
    prompt5 = f"""請對以下核心關鍵字進行 SERP Deep Research：
{p5_keywords}

請完成以下內容：

⸻

1. 模擬 Google 前 20 筆結果的標題
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

請按「每個關鍵字」獨立分段輸出。"""
    st.code(prompt5, language="markdown")

# ==========================================
# Step 6: 文章標題生成
# ==========================================
st.markdown('<div class="step-header">✅ Step 6：文章標題生成</div>', unsafe_allow_html=True)
col1_s6, col2_s6 = st.columns([1, 1])

with col1_s6:
    p6_input = st.text_area("Step 6 輸入：搜尋意圖分析結果", height=150, placeholder="貼上 Step 5 的意圖分析與缺口分析...")

with col2_s6:
    st.markdown("### 📋 複製 Prompt")
    p6_intent = get_value(p6_input, "搜尋意圖結果")
    
    prompt6 = f"""以下是搜尋意圖分析結果：
{p6_intent}

請根據這些意圖，產出 15–20 個 SEO 文章標題，並分成三類：

⸻

1. 資訊型（Information Intent）

2. 比較型 / 選擇型（Comparison Intent）

3. 行動導向型（Transactional / CTA Intent）

⸻

要求：
• 必須融入核心關鍵字
• 有明顯點擊動機（但不浮誇）
• 每個標題彼此不重複
• 各類型至少 5 個以上"""
    st.code(prompt6, language="markdown")

# ==========================================
# Step 7: 文章大綱
# ==========================================
st.markdown('<div class="step-header">✅ Step 7：文章大綱</div>', unsafe_allow_html=True)
col1_s7, col2_s7 = st.columns([1, 1])

with col1_s7:
    p7_input = st.text_input("Step 7 輸入：最終選擇的文章標題", placeholder="輸入你選好的那個標題...")

with col2_s7:
    st.markdown("### 📋 複製 Prompt")
    p7_title = get_value(p7_input, "最終標題")
    
    prompt7 = f"""以下是我選擇的文章標題：
{p7_title}

請根據這個標題，產出完整 SEO 大綱。

格式要求：

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
• 文章如何避免淪為通用內容（差異化策略）"""
    st.code(prompt7, language="markdown")

# ==========================================
# Step 8: 文章撰寫 + 技術 SEO
# ==========================================
st.markdown('<div class="step-header">✅ Step 8：文章撰寫 + 技術 SEO</div>', unsafe_allow_html=True)
col1_s8, col2_s8 = st.columns([1, 1])

with col1_s8:
    p8_word = st.text_input("文章字數需求：", value="1500 字")
    p8_cta = st.text_input("CTA 文案與連結：", value="免費試用：https://example.com")
    p8_outline = st.text_area("Step 8 輸入：確認後的完整大綱", height=200, placeholder="貼上 Step 7 的完整大綱...")

with col2_s8:
    st.markdown("### 📋 複製 Prompt")
    # 使用上一步的標題，如果沒填則顯示佔位符
    p8_title_final = get_value(p7_input, "最終標題")
    p8_outline_final = get_value(p8_outline, "完整大綱")
    
    prompt8 = f"""請根據以下資訊撰寫文章：
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
• 若是 FAQPage 或 HowTo，需提供建議的 Question/Answer 或步驟標題"""
    st.code(prompt8, language="markdown")

# --- 底部 ---
st.divider()
st.info("💡 Tip: 建議另開一個文件視窗，一邊複製 Prompt，一邊貼上 AI 的產出結果，逐步完成整篇文章。")
