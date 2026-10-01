import os
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.callbacks import BaseCallbackHandler

from business_function import sum, calculate_discount, get_weather


load_dotenv()
AGENT_MODEL = os.getenv("AGENT_MODEL")
llm = ChatGroq(model=AGENT_MODEL)
#model_id = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"

#llm = ChatBedrock( model_id=model_id, region_name=os.getenv("AWS_REGION", "us-east-1"))

class CallTracker(BaseCallbackHandler):
    """Prints and counts every LLM call and tool call made by the agent.
    Official documentation: https://reference.langchain.com/python/langchain-core/callbacks/base/BaseCallbackHandler
    """

    def __init__(self, llm):
        self.model_name = getattr(llm, "model_name", "unknown")
        self.llm_calls = 0
        self.tool_calls = 0
        self.tool_counts = {}
        self.total_llm = 0
        self.total_tool = 0

    def on_llm_start(self, serialized, prompts, **kwargs):
        self.llm_calls += 1
        print(f"   [LLM ] call #{self.llm_calls} -> {self.model_name}")

    def on_tool_start(self, serialized, input_str, **kwargs):
        self.tool_calls += 1
        name = (serialized or {}).get("name", "unknown_tool")
        self.tool_counts[name] = self.tool_counts.get(name, 0) + 1
        print(f"   [TOOL] call #{self.tool_calls} -> {name}({input_str})")

    def on_tool_end(self, output, **kwargs):
        print(f"   [TOOL] result  -> {output}")

    def finish_turn(self):
        """Fold this turn's counts into the session totals and reset."""
        self.total_llm += self.llm_calls
        self.total_tool += self.tool_calls
        breakdown = ", ".join(f"{k}={v}" for k, v in self.tool_counts.items()) or "none"
        summary = (
            f"LLM calls: {self.llm_calls} | Tool calls: {self.tool_calls} ({breakdown})"
        )
        self.llm_calls = 0
        self.tool_calls = 0
        self.tool_counts = {}
        return summary


@tool
def add_numbers(a: int, b: int):
    """Add two integers and return their sum."""
    return sum(a, b)


@tool
def discount(price: float, percentage: float):
    """Calculate the final price after applying a percentage discount."""
    return calculate_discount(price, percentage)


@tool
def weather(city: str):
    """Get the current weather conditions for a city."""
    return get_weather(city)


def create_ai_agent(llm, tools):
    agent = create_agent(
        llm,
        tools=tools,
        system_prompt="You are a helpful AI assistant. Use tools when needed.",
    )
    return agent


def ask_agent(question: str, agent, tracker: CallTracker):
    try:
        result = agent.invoke(
            {"messages": [("human", question)]},
            config={"callbacks": [tracker]},
        )
        return result["messages"][-1].content
    except Exception as e:
        return {"error": str(e)}


def main() -> None:
    """Run an interactive session for testing the business tools."""
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    agent = create_ai_agent(llm, [add_numbers, discount, weather])
    tracker = CallTracker(llm)

    print("Business function agent is ready.")
    print("Enter a natural-language scenario, or type 'exit' to quit.\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not question:
            continue

        if question.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break

        print("   -- agent running --")
        response = ask_agent(question, agent, tracker)
        print(f"Agent: {response}")
        print(f"   >> this turn: {tracker.finish_turn()}\n")

    print(
        f"\nSession totals: LLM calls: {tracker.total_llm} | "
        f"Tool calls: {tracker.total_tool}"
    )


if __name__ == "__main__":
    main()

