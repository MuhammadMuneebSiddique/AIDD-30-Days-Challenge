import os
from dotenv import load_dotenv
from agents import Agent, OpenAIChatCompletionsModel,AsyncOpenAI
from extract import extract_text_from_pdf, clean_text

load_dotenv()

# API Requirements:
# - Library: openai-agents
# - Base URL: https://generativelanguage.googleapis.com/v1beta/openai/
# - Use GEMINI_API_KEY from .env
# - Model: OpenaiChatCompletionModel with Gemini model

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

# External Client 
external_client = AsyncOpenAI(
    api_key = GEMINI_API_KEY,
    base_url ="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Model
model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_client
)

# System Prompt:
# "Summarize uploaded PDFs and generate quizzes strictly from extracted text.
# MCQs must contain a question, four options (A–D), and correct_answer.
# Do not invent content. Follow JSON-safe structured output."

study_agent = Agent(
    name="PDF Study Notes Summarizer & Quiz Generator",
    instructions=(
        "Summarize uploaded PDFs and generate quizzes strictly from extracted text. "
        "MCQs must contain a question, four options (A–D), and correct_answer. "
        "Do not invent content. Follow JSON-safe structured output."
    ),
    tools=[extract_text_from_pdf, clean_text],
    model=model
)
