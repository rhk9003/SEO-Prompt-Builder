import streamlit as st

# --- 頁面設定 ---
st.set_page_config(
    page_title="SEO Prompt 逐步生成器",
    page_icon="📋",
    layout="centered"
)

# --- Session State 初始化 ---
# 用來儲存使用者在每個步驟輸入的資訊，確保切換步驟時資料不丟失
default_values = {
    "step": 1,
    "product_info": "",
    "seo_goal": "",
    "ai_suggested_topics": "",  # 雖然不串API，但為了產生Prompt3，需要使用者貼上AI給的主題
    "selected_keywords": "",
    "search_intent_info": "",
    "selected_title": "",
    "final_outline": "",
    "word_count": "1500字",
    "cta_link": ""
}

for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- 輔助函式：顯示 Prompt 區塊 ---
def display_copyable_prompt(prompt_text, step_num):
    st.info(f"👇 複製下方的 Prompt (步驟 {step_num})，貼給你的 AI 助手：")
    st.code(prompt_text, language="markdown")

# --- 側邊欄 ---
with st.sidebar:
    st.header("流程進度")
    step_names = [
        "1. 產品解析", "2. 關鍵字主題", "3. 核心關鍵字", 
        "4. 搜尋意圖研究", "5. 標題建議", "6. 大綱擬定", "7. 文章撰寫"
    ]
    
    # 顯示進度條
    progress = (st.session_state.step / 7)
    st.progress(progress)
    
    # 導航按鈕 (允許使用者跳回之前的步驟修改)
    st.write(f"目前步驟: **{step_names[st.session_state.step - 1]}**")
    
    st.divider()
    if st.button("🔄 重置所有進度"):
        for key in default_values.keys():
            st.session_state[key] = default_values[key]
        st.rerun()

# --- 主標題 ---
st.title("📋 SEO 文章寫作 Prompt 生成器")
st.markdown("填寫必要資訊，自動生成完整的 SEO Prompt 指令。")

# --- Step 1: 產品解析 ---
if st.session_state.step == 1:
    st.header("Step 1: 產品/計畫解析")
    st.markdown("首先，我們需要讓 AI 理解你要寫什麼產品或計畫。")
    
    st.session_state.product_info = st.text_area(
        "請貼上產品/計畫頁面的內容或描述：", 
        value=st.session_state.product_info,
        height=200,
        placeholder="例如：這是一個協助中小企業自動化記帳的 SaaS 服務，主要功能包含..."
    )
    
    if st.session_state.product_info:
        prompt = f"""幫我解析，這個計畫/產品頁中，提供了什麼?解決了什麼問題?

產品資訊如下:
{st.session_state.product_info}"""
        
        display_copyable_prompt(prompt, 1)
        
        if st.button("下一步：設定目標 ➡️"):
            st.session_state.step = 2
            st.rerun()

# --- Step 2: 設定目標 ---
elif st.session_state.step == 2:
    st.header("Step 2: 設定 SEO 目標")
    
    st.session_state.seo_goal = st.text_area(
        "請描述這篇文章的 SEO 任務目標：",
        value=st.session_state.seo_goal,
        placeholder="例如：針對剛創業的年輕老闆，讓他們搜尋『記帳軟體』時能看到我們，並強調省時的優點。"
    )
    
    if st.session_state.seo_goal:
        prompt = f"""現在我有個任務目標，我要撰寫一篇SEO為目的的文章，利用搜尋結果達成以下目的:

{st.session_state.seo_goal}

為了這個目的，你認為我選關鍵字該鎖定哪些主題?"""
        
        display_copyable_prompt(prompt, 2)
        
        st.write("---")
        st.markdown("**💡 執行後：** 請將 AI 建議的關鍵字主題大致看過，準備進入下一步。")
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("⬅️ 上一步"):
                st.session_state.step = 1
                st.rerun()
        with col2:
            if st.button("下一步：篩選關鍵字 ➡️"):
                st.session_state.step = 3
                st.rerun()

# --- Step 3: 篩選核心關鍵字 ---
elif st.session_state.step == 3:
    st.header("Step 3: 篩選核心關鍵字")
    
    st.markdown("請將 AI 在上一步驟 (Step 2) 產生的回答或關鍵字列表貼在下方，或是直接輸入你想讓 AI 挑選的關鍵字清單。")
    
    st.session_state.ai_suggested_topics = st.text_area(
        "貼上關鍵字/主題清單：",
        value=st.session_state.ai_suggested_topics,
        height=150
    )
    
    if st.session_state.ai_suggested_topics:
        prompt = f"""根據這些關鍵字，你認為哪些字最適合作為這篇文章操作的核心關鍵字

關鍵字清單參考:
{st.session_state.ai_suggested_topics}"""
        
        display_copyable_prompt(prompt, 3)
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("⬅️ 上一步"):
                st.session_state.step = 2
                st.rerun()
        with col2:
            if st.button("下一步：搜尋意圖研究 ➡️"):
                st.session_state.step = 4
                st.rerun()

# --- Step 4: 搜尋意圖研究 ---
elif st.session_state.step == 4:
    st.header("Step 4: 搜尋意圖深度研究")
    
    st.markdown("請輸入你決定要操作的那些「核心關鍵字」。")
    
    st.session_state.selected_keywords = st.text_area(
        "核心關鍵字 (一行一個或是用逗號分隔)：",
        value=st.session_state.selected_keywords,
        placeholder="例如：\n自動化記帳\n雲端會計軟體"
    )
    
    if st.session_state.selected_keywords:
        prompt = f"""幫我針對下列關鍵字進行研究(deep research)
我需要知道的事情有，這些關鍵字在搜尋結果中，排名前兩頁的搜尋結果標題都是些什麼?進而幫我推論，搜尋我給的這些字的使用者具有什麼樣的搜尋意圖與資訊需求?

請研究後，幫我彙整每個關鍵字對應的搜尋意圖。

關鍵字清單:
{st.session_state.selected_keywords}"""
        
        display_copyable_prompt(prompt, 4)
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("⬅️ 上一步"):
                st.session_state.step = 3
                st.rerun()
        with col2:
            if st.button("下一步：標題建議 ➡️"):
                st.session_state.step = 5
                st.rerun()

# --- Step 5: 標題建議 ---
elif st.session_state.step == 5:
    st.header("Step 5: 文章標題建議")
    
    st.markdown("為了讓 AI 給出精準標題，建議將 Step 4 AI 分析出的「搜尋意圖」貼入下方。")
    
    st.session_state.search_intent_info = st.text_area(
        "貼上 Step 4 的搜尋意圖分析結果 (或是產品背景資訊)：",
        value=st.session_state.search_intent_info,
        height=150
    )
    
    if st.session_state.search_intent_info:
        prompt = f"""請幫我根據我給的資訊/搜尋意圖，給我這篇文章的標題建議清單

參考資訊/搜尋意圖:
{st.session_state.search_intent_info}"""
        
        display_copyable_prompt(prompt, 5)
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("⬅️ 上一步"):
                st.session_state.step = 4
                st.rerun()
        with col2:
            if st.button("下一步：擬定大綱 ➡️"):
                st.session_state.step = 6
                st.rerun()

# --- Step 6: 擬定大綱 ---
elif st.session_state.step == 6:
    st.header("Step 6: 擬定文章大綱")
    
    st.markdown("從 Step 5 生成的建議中，選一個你最喜歡的標題填入。")
    
    st.session_state.selected_title = st.text_input(
        "輸入文章標題：",
        value=st.session_state.selected_title
    )
    
    if st.session_state.selected_title:
        prompt = f"""我選擇的標題如下，請根據這個標題幫我擬定這篇文章的大綱
我希望標題能夠都以問題導向呈現。

文章標題: {st.session_state.selected_title}"""
        
        display_copyable_prompt(prompt, 6)
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("⬅️ 上一步"):
                st.session_state.step = 5
                st.rerun()
        with col2:
            if st.button("下一步：撰寫文章 ➡️"):
                st.session_state.step = 7
                st.rerun()

# --- Step 7: 撰寫文章 ---
elif st.session_state.step == 7:
    st.header("Step 7: 撰寫內容")
    
    st.markdown("最後一步！確認大綱、字數與 CTA。")
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        st.session_state.word_count = st.text_input("文章字數需求：", value=st.session_state.word_count)
    with col_input2:
        st.session_state.cta_link = st.text_input("CTA 連結與文字：", value=st.session_state.cta_link)
    
    st.session_state.final_outline = st.text_area(
        "貼上確認後的文章大綱：",
        value=st.session_state.final_outline,
        height=200
    )
    
    if st.session_state.final_outline:
        prompt = f"""請幫我根據前面訂好的大鋼與標題，撰寫文章內容

文章標題: {st.session_state.selected_title}
文章字數需求: {st.session_state.word_count}
文章CTA 連結: {st.session_state.cta_link}

大綱:
{st.session_state.final_outline}"""
        
        display_copyable_prompt(prompt, 7)
        
        st.success("🎉 恭喜！你已完成所有 Prompt 的生成。")
        
        if st.button("⬅️ 上一步"):
            st.session_state.step = 6
            st.rerun()
