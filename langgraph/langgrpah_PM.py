import os
import re
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCia5xHVKOeC5LfdjLCIcYkfCmR6OYOugY'
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages 
from langgraph.checkpoint import MemorySaver
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



class PMState(TypedDict):
    messages: Annotated[list, add_messages]
    evaluation_score: int  

def evaluate_requirement(state: PMState):
    # 評估需求是否完整
    llm_chain = LLMChain(prompt=evaluation_prompt_template, llm=llm)
    response = llm_chain.run(requirements=state["messages"][-1].content)
    try:
        score = int(re.findall(r'此需求的評分為: (\d)', response)[0]) # 獲取評分
    except:
        score = state["evaluation_score"]
    return {"messages": [llm.invoke(state["messages"][-1].content)], "evaluation_score": score}

def init_conversation():
    # 初始化graph
    workflow = StateGraph(PMState)
    workflow.add_node("evaluate_requirement", evaluate_requirement)
    workflow.set_entry_point("evaluate_requirement") 
    workflow.add_edge("evaluate_requirement", END)
    graph = workflow.compile(checkpointer=MemorySaver())
    
    return graph

        
# # display graph in plots
# from IPython.display import Image, display
# display(Image(graph.get_graph().draw_mermaid_png()))     
        


