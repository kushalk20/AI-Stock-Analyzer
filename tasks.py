from crewai import Task
from agents import log_analyzer, stock_analysis_agent, investment_advisor_agent

# 1) Task: Gather company news
get_company_news_task = Task(
    name="Get Company News",
    description="Gather the latest news and information about the company: {company_name}",
    agent=log_analyzer,
    expected_output="A summarized report of the latest news and information about {company_name}"
    #async_execution=True
)

# 2) Task: Analyze stock & financials
analyze_stock_task = Task(
    name="Analyze Company Stock",
    description=(
        "Fetch detailed stock, financial, and investment-related indicators for {company_name}. "
        "Analyze valuation, growth, profitability, and key risks. If price series available, "
        "summarize trend observations."
    ),
    agent=stock_analysis_agent,
    expected_output=(
        "A structured analysis including:\n"
        "1) Company overview\n"
        "2) Key stock & valuation metrics\n"
        "3) Charts (if applicable)\n"
        "4) Financial strength & growth analysis\n"
        "5) Risk factors\n"
        "6) Summary of trend observations"
    )
    #async_execution=True
)

# 3) Task: Synthesize final investment decision (consumes context of 1 & 2)
investment_decision_task = Task(
    name="Synthesize Investment Decision",
    description=(
        "Using the outputs of the news summary and stock analysis for {company_name}, "
        "synthesize an investment decision. Provide Buy/Sell/Hold with rationale grounded in "
        "both qualitative news and quantitative metrics, top risks, mitigations, key thresholds, "
        "and a final investor note with target price and duration."
    ),
    agent=investment_advisor_agent,
    expected_output=(
        "Final recommendation (Buy/Sell/Hold) with structured rationale, risks, investor note, "
        "and target price with timeline."
    ),
    context=[get_company_news_task, analyze_stock_task]
)