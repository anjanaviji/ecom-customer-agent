from langchain_groq import ChatGroq
from .config import settings
from customer_agent.tools import get_order
from langchain.messages import ToolMessage
llm = ChatGroq(
    groq_api_key=settings.groq_api_key,
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=500,
    verbose=True,
    )
llm_with_tools = llm.bind_tools([get_order])
user_message = "Get the order details for order ID 1"
ai_message = llm_with_tools.invoke(user_message)
tool_messages = []

for tool_call in ai_message.tool_calls:
    if tool_call["name"] == "get_order":
        result = get_order.invoke(tool_call["args"])

        tool_messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"],
            )
        )

# Give tool result back to LLM
final_response = llm_with_tools.invoke(
    [
        user_message,
        ai_message,
        *tool_messages,
    ]
)

print("\nFinal answer:")
print(final_response.content)