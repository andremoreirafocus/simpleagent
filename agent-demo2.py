from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

#Example: ChatGroq with System + Human Prompt + Prompt Template
#System Prompt → Defines the AI's role, rules, behavior
#Human Prompt → User's actual request/input
#Prompt Template → Reusable structure with variables

# 1. Create LLM
llm = ChatGroq(model="openai/gpt-oss-120b",
    temperature=0.2
)

#Low temperature (0.0–0.2): More deterministic, factual, and consistent.
# High temperature (0.8–2.0): More creative, varied, and sometimes less predictable.

# 2. Create Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert AI Engineer.

Rules:
- Explain concepts clearly
- Give enterprise examples
- Use simple language
- Provide production best practices
"""
        ),
        (
            "human",
            """
Explain {topic}.

Include:
1. What it is
2. Why companies use it
3. Real-world example
"""
        )
    ]
)


# 3. Add user input
chain = prompt | llm


response = chain.invoke(
    {
        "topic": "What is RAG "
    }
)


print(response.content)