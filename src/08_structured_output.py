
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

project_root = Path(__file__).resolve().parents[1]
load_dotenv(
    project_root / ".env",
    override=not os.getenv("GROQ_API_KEY", "").strip(),
)
load_dotenv(
    project_root / "tests" / ".env",
    override=not os.getenv("GROQ_API_KEY", "").strip(),
)

api_key = os.getenv("GROQ_API_KEY", "").strip()
if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Add it to the project-root .env file "
        "or tests/.env; see .env.example."
    )


class QuestionClassification(BaseModel):
    category: str = Field(
        description="One of: langgraph, rag, general"
    )
    explanation: str = Field(
        description="Why the question belongs to this category"
    )


llm = ChatGroq(
    api_key=api_key,
    model=os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-120b",
    ),
    temperature=0,
)

# Use the provider's supported structured-output mechanism.
classifier = llm.with_structured_output(
    QuestionClassification,
    method="function_calling",
)

result = classifier.invoke(
    "Classify this question: What is RAG? Return the result as JSON."
)

print(result)
print("Category:", result.category)
