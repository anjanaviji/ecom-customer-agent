from langchain_groq import ChatGroq
from .config import settings
from customer_agent.tools import get_order, get_user, get_user_orders
from langchain.messages import HumanMessage
from langchain.agents import create_agent 
from customer_agent.rag.tool import search_knowledge

SYSTEM_PROMPT = """
You are a customer support assistant.

Answer the user's question using ONLY the information provided
by the available tools and retrieved knowledge.

Rules:
1. If the provided context does not contain enough information
   to answer the question, say:
   "I don't have sufficient information to answer that question."

2. Do not use your general knowledge to fill in missing information.

3. Do not invent policies, prices, dates, procedures, or other facts.

4. If you use information from the knowledge base, rely only on
   the retrieved content.
"""
llm = ChatGroq(
    groq_api_key=settings.groq_api_key,
    model="openai/gpt-oss-120b",
    temperature=0,
    max_tokens=500,
    verbose=True,
    )


agent = create_agent(model=llm, tools=[get_order, get_user, get_user_orders, search_knowledge], 
system_prompt=SYSTEM_PROMPT)
