"""
CalculatorAgent (LangGraph)

What this agent does:
- Reads a natural-language math request (e.g., "multiply 6 by 7 then add 4").
- Lets the LLM decide which tool(s) to call (add/sub/mul/div) via tool-calling.
- Optionally "reflects" (reviews its own answer) up to 2 times to improve quality.

Key ideas:
- StateGraph orchestrates the flow between nodes.
- Nodes: LLM node, Tool node, Reflection node.
- Conditional edges decide whether to call tools again or reflect, or finish.
"""
from IPython.display import Image,display
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv

# LLM, messages, and tools from LangChain
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool

# LangGraph pieces for message aggregation and graph building
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Load OpenAI API Key
# Make sure you have a .env file with OPENAI_API_KEY=...
load_dotenv()

class CalculatorAgent(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    reflections: int  # Track number of reflections

# Define tools
# The @tool decorator exposes these functions as callable tools.
@tool
def add(num1: int, num2: int) -> int:
    """Add numbers"""
    return num1 + num2

@tool
def sub(num1: int, num2: int) -> int:
    """Subtract numbers"""
    return num1 - num2

@tool
def mul(num1: int, num2: int) -> int:
    """Multiply numbers"""
    return num1 * num2

@tool
def div(num1: int, num2: int) -> float:
    """Divide numbers, error if b=0"""
    if num2 == 0:
        raise ValueError("Division by zero is not allowed.")
    return num1 / num2

 #Register all tools in a list
tools = [add, sub, mul, div]

# Create the LLM and BIND the tools so it can call them autonomously.
model = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools)

# Main LLM Reasoning Node
# runs the model on the current messages to decide the next step.
# It might either:
#      - call a tool (tool_calls present), OR
#      - produce a final natural-language answer (no tool_calls), OR
#      - ask to reflect (our graph decides based on last message).
def model_call(state: CalculatorAgent) -> CalculatorAgent:
    system_prompt = SystemMessage(content="You are a helpful math agent. " \
    "Use tools if needed to solve problems.")
    response = model.invoke([system_prompt] + state["messages"])
    return {"messages": [response], "reflections": state.get("reflections", 0)}

# Reflection Node
#- gives the model a chance to improve its last answer.
#- At most 2 reflections to avoid infinite loops / cost blowups.
def reflect(state: CalculatorAgent) -> CalculatorAgent:
    reflections_done = state.get("reflections", 0)
    # Stop reflecting if limit reached
    if reflections_done >= 2:
        return state
    
    system_prompt = SystemMessage(content="Review the previous answer. " \
    "Check for mistakes or improvements. Answer only with the best final answer.")
    
    # Run the LLM again with this reflection instruction + full context
    reflection_response = model.invoke([system_prompt] + state["messages"])
    
    # (Optional) Print reflection to console for visibility during dev runs
    print(f"\n[Reflection #{reflections_done+1}] {reflection_response.content}\n")
    
    # Append the reflection message to history and increment reflection counter
    new_messages = state["messages"] + [reflection_response]
    return {"messages": new_messages, "reflections": reflections_done + 1}

# Conditional for main loop
def should_continue(state: CalculatorAgent) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "continue"
    else:
        return "reflect"

# Conditional for reflection loop
def should_reflect(state: CalculatorAgent) -> str:
    if state.get("reflections", 0) < 2:
        return "reflect"
    else:
        return END

# Build Graph
graph = StateGraph(CalculatorAgent)
graph.add_node("llm", model_call)
graph.add_node("tools", ToolNode(tools=tools))
graph.add_node("reflect", reflect)

# Entry point
graph.set_entry_point("llm")

# Edges
graph.add_conditional_edges("llm", should_continue, {"continue": "tools", "reflect": "reflect"})
graph.add_edge("tools", "llm")
graph.add_conditional_edges("reflect", should_reflect, {"reflect": "reflect", END: END})

# Compile
app = graph.compile()

#To print the graph
# --- Save graph to a PNG file (any Python environment) ---
png_bytes = app.get_graph().draw_mermaid_png()
with open("calculator_agent_graph.png", "wb") as f:
    f.write(png_bytes)

print("Saved diagram to calculator_agent_graph.png")


# Stream printer
def print_stream(stream):
    for s in stream:
        msg = s["messages"][-1]
        try:
            msg.pretty_print()
        except:
            print(msg)

# Run Example
print_stream(app.stream({"messages": ["user", "multiply 6 by 7 then add 4"], 
"reflections": 0}, stream_mode="values"))
