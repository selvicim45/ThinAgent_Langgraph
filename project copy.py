# Import Statements
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Loads the .env key for openai
load_dotenv()


class CalculatorAgent(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def add(num1: int, num2: int) -> int:
    """This is an add tool, that add two given numbers"""
    result = num1 + num2
    return result


@tool
def sub(num1: int, num2: int) -> int:
    """This is an subtract tool, that subtract two given numbers"""
    result = num1 - num2
    return result


@tool
def mul(num1: int, num2: int) -> int:
    """This is an multiplication tool, that multiplies two given numbers"""
    result = num1 * num2
    return result


@tool
def div(num1: int, num2: int) -> float:
    """Divides two given numbers, returns an error message if dividing by zero."""
    if num2 == 0:
        raise ValueError("Division by zero is not allowed. Please enter a non-zero denominator.")
    return num1 / num2


# List of all available tools
tools = [add, sub, mul, div]

# Instantiate the model and bind tools
model = ChatOpenAI(model="gpt-4o").bind_tools(tools)


def model_call(state: CalculatorAgent) -> CalculatorAgent:
    system_prompt = SystemMessage(content="You are a helpful AI agent, please answer the query to your best ability")
    response = model.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}


# condition edge for the langgraph
def should_continue(state: CalculatorAgent)->str:
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"


graph = StateGraph(CalculatorAgent)
graph.add_node("llm", model_call)
tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)
graph.set_entry_point("llm")
graph.add_conditional_edges("llm", should_continue, {"continue": "tools", "end": END})
graph.add_edge("tools", "llm")
app = graph.compile()


def print_stream(stream):
    for s in stream:
        messages = s["messages"][-1]
        if isinstance(messages, tuple):
            print(messages)
        else:
            messages.pretty_print()


input = {"messages": ["user", "add 1 and 3"]}
# input={"messages":["user", "sub 1 and 3"]}
# input={"messages":["user", "mul 1 and 3"]}
# input={"messages":["user", "div 4 and 0"]}
print_stream(app.stream(input, stream_mode="values"))










