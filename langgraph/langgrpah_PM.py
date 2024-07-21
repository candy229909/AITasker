import os
import re
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCia5xHVKOeC5LfdjLCIcYkfCmR6OYOugY'
from IPython.display import Image, display
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain import LLMChain
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)
evaluation_prompt_template = PromptTemplate(
    template="請根據以下標準評估需求是否完整：\n"
    "1. 需求是否涵蓋了所有關鍵功能和特性？\n"
    "2. 需求是否描述得足夠詳細？\n"
    "3. 需求是否說明時程？\n"
    "請給出一個 1 到 5 的評分，1 代表最不完整，5 代表最完整。\n"
    "最後一行顯示'此需求的評分為:?', ?為上述3點問題的分數平均\n"
    "需求：{requirements}",
    input_variables=["requirements"],
)

# user_info = "['我需要訂購一個新的膠囊咖啡機，價格介於1000~3000，使用的咖啡以美式和拿鐵為主', '膠囊系統選Nespresso，尺寸的話小於長90cm寬90cm高90cm，網站以蝦皮購物為主', '因為我下周要送禮，有哪台咖啡機可以三天內就可以到貨嗎?', '我選擇Nespresso Essenza Mini', 'Nespresso官網購買，顏色黑色', '水箱容量40l內']"
# llm_chain = LLMChain(prompt=evaluation_prompt_template, llm=llm)
# response = llm_chain.run(requirements=[user_info])
# response = llm_chain.run(requirements=r["requirements"])
# print(response)
# re.findall(r'此需求的評分為: (\d)', response)


def concat(original: list, new: list) -> list:
    return original + new

class PMState(TypedDict):
    messages: Annotated[list, concat]
    requirements: Annotated[list, concat]
    evaluation_score: int

def collect_requirement(state: PMState):
    # 收集需求
    user_input = state["messages"][-1].content
    state["requirements"].append(user_input)
    return {"messages": [llm.invoke(state["requirements"])]}


def evaluate_requirement(state: PMState):
    # 評估需求是否完整
    llm_chain = LLMChain(prompt=evaluation_prompt_template, llm=llm)
    response = llm_chain.run(requirements=state["requirements"])
    try:
        score = int(re.findall(r'此需求的評分為: (\d)', response)[0]) # 獲取評分
    except:
        score = state["evaluation_score"]
    return {"evaluation_score": score}


# 建立graph
workflow = StateGraph(PMState)
workflow.add_node("collect_requirement", collect_requirement)
workflow.add_node("evaluate_requirement", evaluate_requirement)
workflow.set_entry_point("collect_requirement")
workflow.add_edge("collect_requirement", "evaluate_requirement")
workflow.add_edge("evaluate_requirement", END)
graph = workflow.compile(checkpointer=MemorySaver())
# display(Image(graph.get_graph().draw_mermaid_png()))

config = {"configurable": {"thread_id": "1"}}
r = graph.invoke(
    {"messages": [SystemMessage(content="You are a Project Manager."),
                  HumanMessage("你好!")], "requirements": [], "evaluation_score": 0},
    config=config
)    

# 啟動對話迴圈
while True:
    if r["evaluation_score"] >= 3:
        print("是否還有需要補充的呢?")
        user_input = input("User: ")
        if user_input.lower() in ['沒有', 'no','沒了']:
            print("Goodbye!")
            break 
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    r = graph.invoke(
        {"messages": [SystemMessage(content="You are a Project Manager. 你的目標是將需求者的問題整理, 使用者提供的資訊足夠的時候，將資訊整理顯示出來給開發著閱讀"),
                      HumanMessage(user_input)], "requirements": [], "evaluation_score": 0},
        config=config
    )    
    print("AI: " + r["messages"][-1].content)
    # print("需求列表：", r["requirements"])
    print("評估分數：", r["evaluation_score"])
#%%
嗨，我需要和你討論即將開展的軟體開發專案。
我們計畫開發一個新的手機應用程式，用於管理個人財務。
這個應用程式應該讓使用者能夠追蹤開支、建立預算，並生成報告。我們的目標用戶主要是年齡在25至35歲之間的年輕成年人，他們對科技敏感，並關心如何有效地管理財務。
我們計劃在iOS和Android平台上推出。至於開發技術，我們偏好使用React Native，因為它具有跨平台的能力。
資料安全至關重要。應用程式應該在傳輸和靜態存儲時都加密用戶數據。我們還需要強大的身份驗證機制。
我們希望在六個月內推出，所以開發工作需要在那之前完成。
#%%
User: 嗨，我需要和你討論即將開展的軟體開發專案。
AI: 你好！我很樂意協助你討論你的軟體開發專案。請告訴我更多資訊，例如：

* **專案目標:** 你希望透過這個軟體達成什麼目標？
* **目標使用者:** 你的目標使用者是誰？
* **主要功能:** 這個軟體需要具備哪些主要功能？
* **預算和時程:** 你有預算和時程方面的限制嗎？
* **技術需求:** 你有特定的技術需求嗎，例如程式語言、平台或框架？

提供越詳細的資訊，我就能越有效地幫助你。 

評估分數： 1  
******************************************************************************************************************************** 
User: 我們計畫開發一個新的手機應用程式，用於管理個人財務。
AI: 太好了！我很樂意協助您討論您的個人財務管理應用程式。  

為了更有效地幫助您，請您提供更多資訊：

* **目標客群:** 您的目標客群是誰？ (例如：學生、年輕專業人士、家庭)
* **主要功能:** 您希望應用程式具備哪些核心功能？ (例如：預算追蹤、帳單支付、投資管理)
* **平台:** 您打算開發哪個平台的應用程式？ (例如：iOS、Android、網頁)
* **預算和時程:** 您是否有預定的預算和開發時程？
* **設計理念:** 您希望應用程式呈現什麼樣的風格和感覺？ (例如：簡潔、現代、專業)

 有了這些資訊，我可以更深入地了解您的需求，並提供更具體的建議。 

評估分數： 1
********************************************************************************************************************************
User: 這個應用程式應該讓使用者能夠追蹤開支、建立預算，並生成報告。我們的目標用戶主要是年齡在25至35歲之間的年輕成年人，他們對科技敏感，並關心如何有效地管理財務。
AI: 聽起來是個很棒的點子！我很樂意協助你討論這個個人財務應用程式的開發。

為了更深入地了解你的需求，你能否提供更多關於以下方面的資訊：

* **主要功能：**除了追蹤開支、建立預算和生成報告之外，還有其他想要包含的功能嗎？例如，帳單提醒、儲蓄目標設定、投資追蹤等？
* **平台：**你打算開發 iOS、Android 還是兩個平台的應用程式？
* **設計風格：**你希望應用程式呈現什麼樣的視覺風格？簡約、現代、活潑還是其他風格？
* **預算和時間表：**你是否有預定的預算和開發時間表？
* **技術堆疊：**你是否考慮使用特定的技術堆疊來開發應用程式？

了解這些資訊後，我可以更有效地幫助你規劃專案，例如：

* **功能需求分析：**詳細列出應用程式所需的所有功能和特性。
* **使用者流程設計：**設計使用者在應用程式中的操作流程，確保操作直觀流暢。
* **技術架構設計：**選擇合適的技術堆疊和架構來構建應用程式。
* **開發成本估算：**根據功能需求和技術方案，估算開發成本和時間。

期待你的進一步資訊，讓我們一起打造一個成功的個人財務應用程式！ 

評估分數： 2
********************************************************************************************************************************
User: 我們計劃在iOS和Android平台上推出。至於開發技術，我們偏好使用React Native，因為它具有跨平台的能力。資料安全至關重要。應用程式應該在傳輸和靜態存儲時都加密用戶數據。我們還需要強大的身份驗證機制。
AI: 聽起來你們有個很棒的應用程式構想！我很樂意協助你們開發。你們已經有很好的計畫，並清楚說明了目標受眾、功能和技術方向。

為了更深入地了解這個專案，我想請教幾個問題：

* **關於追蹤開支的功能，你們希望如何讓使用者輸入他們的交易資訊？ 手動輸入、連結銀行帳戶，還是兩者兼具？**
* **預算功能是否需要提供一些彈性，例如自訂預算週期、設定不同類別的預算限額，以及提供預算超支提醒？**
* **報表功能需要涵蓋哪些面向？ 例如支出分析、預算與實際支出比較，還是投資回報率分析？**
* **關於身份驗證，你們考慮使用哪些機制？ 例如雙重驗證、生物識別登入，還是單點登入？**

回答這些問題將有助於我更全面地了解你們的需求，並提供更具體的建議。 

此外，我們還可以討論以下幾個方面：

* **專案時程安排：** 你們希望多久完成這個應用程式的開發？
* **預算：** 你們為這個專案預留了多少預算？
* **團隊：** 你們是否已經有開發團隊？ 還是需要我協助組建團隊？

期待你們的回覆，讓我們一起打造一個成功的個人財務管理應用程式！ 

評估分數： 2
********************************************************************************************************************************
User: 身份驗證使用雙重驗證、生物識別登入。時程的話我們希望在六個月內推出，所以開發工作需要在那之前完成。預算大約100萬內。沒有開發團隊，希望以外包的方式請別人開發。
AI: 好的，我很樂意與您討論您的個人財務管理應用程式開發專案。根據您提供的資訊，我整理了以下重點和一些初步想法：

**目標：**

* 開發一個手機應用程式，幫助使用者追蹤開支、建立預算和生成財務報告。
* 目標用戶：25-35 歲，科技敏感，注重財務管理的年輕人。

**功能：**

*  **開支追蹤：**
    *  記錄收入和支出。
    *  自動分類交易（可自訂）。
    *  支援多種貨幣。
    *  可拍照上傳收據。
*  **預算管理：**
    *  設定預算目標（每月、每週、自訂）。
    *  追蹤預算進度和支出。
    *  提供預算超支提醒。
*  **報告生成：**
    *  可視化顯示支出模式（圖表、圖形）。
    *  自訂報告期間（每月、每週、自訂）。
    *  匯出報告（PDF、CSV）。
*  **其他功能：**
    *  帳戶連結（銀行、信用卡）。
    *  財務目標設定和追蹤。
    *  提供個人化財務建議。

**技術：**

*  **開發平台：** iOS 和 Android。
*  **開發框架：** React Native。
*  **資料安全：**
    *  資料加密（傳輸中和靜態儲存）。
    *  強大的身份驗證機制（雙重驗證、生物識別）。

**時程和預算：**

*  開發時間：6 個月。
*  預算：100 萬。
*  開發方式：外包。

**接下來的步驟：**

1. **需求分析和文件撰寫：** 
    *  詳細定義應用程式功能和規格。
    *  設計使用者介面 (UI) 和使用者體驗 (UX)。
    *  制定開發計畫和時程表。
2. **尋找合適的外包團隊：**
    *  尋找具有 React Native 開發經驗的團隊。
    *  評估團隊的技術能力、溝通能力和專案管理經驗。
3. **開發階段：**
    *  進行程式碼開發和測試。
    *  定期與外包團隊溝通和追蹤進度。
4. **應用程式上架：**
    *  在 App Store 和 Google Play 上架應用程式。
    *  進行應用程式推廣和行銷。

**其他考量因素：**

*  **市場調查：** 研究競爭對手和目標用戶需求。
*  **最小可行產品 (MVP)：** 考慮先開發核心功能，然後再逐步迭代。
*  **持續維護和更新：** 預留預算和資源，用於應用程式上架後的維護和更新。

這只是一個初步的框架，我們可以根據您的具體需求和目標進行調整。 

您接下來希望討論哪些方面呢？ 例如，我們可以更深入地探討功能列表、技術細節、外包團隊選擇，或者任何您想進一步了解的內容。 
評估分數： 3
********************************************************************************************************************************
是否還有需要補充的呢?
User: 沒有
Goodbye!


