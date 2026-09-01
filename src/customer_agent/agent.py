from langchain_groq import ChatGroq
from .config import settings
from customer_agent.tools import get_order, get_user, get_user_orders
from langchain.messages import HumanMessage
from langchain.agents import create_agent 
from customer_agent.rag.tool import search_knowledge
llm = ChatGroq(
    groq_api_key=settings.groq_api_key,
    model="openai/gpt-oss-120b",
    temperature=0,
    max_tokens=500,
    verbose=True,
    )
agent = create_agent(model=llm, tools=[get_order, get_user, get_user_orders, search_knowledge])
