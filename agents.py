import os
from crewai import Agent, LLM
from dotenv import load_dotenv
from tools import serper_tool
from tools import get_company_stock_info


load_dotenv()


hf_llm = LLM(
    base_url="https://router.huggingface.co/v1",
    model = "huggingface/meta-llama/Llama-3.3-70B-Instruct",
    api_key=os.environ["HF_TOKEN"]
)

# 1) News and info researcher
log_analyzer = Agent(
    role="News and info researcher",
    goal="Gather and provide the latest news and information about the company from various sources.",
    backstory="Expert researcher skilled in finding and summarizing relevant news articles, press releases, and social updates.",
    llm= hf_llm,
    tools=[serper_tool],
    cache=True,
    max_iterations=6,
    max_rpm=15,
    max_execution_time=600,
    memory=True,
    temperature=0.2,
    verbose=True
)

# 2) Stock investment analyst
stock_analysis_agent = Agent(
    role="Stock Investment Analyst",
    goal="Extract stock, financial health, valuation metrics, and investment indicators to assess attractiveness.",
    backstory="Professional equity research analyst with expertise in fundamental analysis, valuation, and risk assessment.",
    tools=[get_company_stock_info],
    llm= hf_llm,
    verbose=True,
    max_iterations=4,
    max_rpm=15,
    max_execution_time=600,
    memory=True,
    temperature=0.2
)

# 3) Investment decision advisor
investment_advisor_agent = Agent(
    role="Investment Decision Advisor",
    goal=(
        "Consume both the latest news summary and structured stock analysis to provide "
        "a clear investment recommendation (Buy/Sell/Hold) with rationale, risks, and "
        "key metrics supporting the decision."
    ),
    backstory="Seasoned portfolio strategist synthesizing qualitative news flow and quantitative metrics.",
    llm= hf_llm,
    tools=[],  # relies on the context from prior tasks
    verbose=True,
    memory=True,
    max_iterations=4,
    max_execution_time=800,
    temperature=0.2
)