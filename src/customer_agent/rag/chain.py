# # rag/chain.py
# # for stabdalone rag chain
# # Not required for our agentic rag
# # Kept for testing rag alone

# from langchain_core.prompts import ChatPromptTemplate

# from customer_agent.agent import llm
# from customer_agent.rag.retriever import get_retriever


# retriever = get_retriever()


# prompt = ChatPromptTemplate.from_messages([
#     (
#         "system",
#         """You are a customer support assistant.
#         Answer the question using only the provided context.
#         If the context does not contain the answer, say you don't have
#         enough information.
#         Context:
#         {context}
#         """
#      ),
#     ("human", "{question}"),
# ])


# def answer_question(question: str) -> str:

#     documents = retriever.invoke(question)

#     context = "\n\n".join(
#         document.page_content
#         for document in documents
#     )

#     messages = prompt.invoke({
#         "question": question,
#         "context": context,
#     })

#     response = llm.invoke(messages)

#     return response.content