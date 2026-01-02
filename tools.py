import os
import json
from datetime import datetime
import yfinance as yf
from yahooquery import search as yq_search
from crewai.tools import tool
from crewai_tools import SerperDevTool 
from dotenv import load_dotenv

load_dotenv()

# WEB SEARCH TOOL USING SERPER DEV API
try:
    serper_tool = SerperDevTool(api_key=os.environ["SERPER_API_KEY"])
except Exception as e:
    print(f"Error initializing Serper Dev Tool: {e}")


# Helper to resolve ticker symbol from company name
def resolve_ticker(company_name: str) -> str | None:
    try:
        results = yq_search(company_name)
        quotes = results.get("quotes", []) or []
        for q in quotes:
            if q.get("quoteType") == "EQUITY" and q.get("symbol"):
                return q.get("symbol")
        return quotes[0].get("symbol") if quotes else None
    except Exception:
        return None


# GET COMPANY STOCK & INVESTMENT DATA TOOL
@tool("Get Company Stock & Investment Data")
def get_company_stock_info(company_name: str) -> str:
    """
    Returns structured financial information and recent price series as JSON for the given company.
    No files are written; everything is returned in-memory.
    """
    try:
        symbol = resolve_ticker(company_name) or company_name
        ticker = yf.Ticker(symbol)
        info = ticker.info or {}

        # Quarterly financials (last up to 4 quarters)
        quarterly_income = ticker.quarterly_income_stmt
        last_4 = []
        try:
            if quarterly_income is not None and not quarterly_income.empty:
                for col in quarterly_income.columns[:4]:
                    last_4.append({
                        "Quarter": str(getattr(col, "date", lambda: col)()),
                        "Revenue": quarterly_income.loc["Total Revenue", col] if "Total Revenue" in quarterly_income.index else None,
                        "EBITDA": quarterly_income.loc["EBITDA", col] if "EBITDA" in quarterly_income.index else None,
                        "EBIT": quarterly_income.loc["EBIT", col] if "EBIT" in quarterly_income.index else None,
                        "Net Income": quarterly_income.loc["Net Income Common Stockholders", col] if "Net Income Common Stockholders" in quarterly_income.index else None,
                    })
        except Exception:
            pass

        # Historical prices (1y daily) as inline array for charting
        prices = []
        try:
            hist = ticker.history(period="1y", interval="1d")
            if not hist.empty:
                hist = hist.reset_index()
                for _, row in hist.iterrows():
                    date_val = row.get("Date")
                    if isinstance(date_val, datetime):
                        date_str = date_val.strftime("%Y-%m-%d")
                    else:
                        date_str = str(date_val)
                    prices.append({
                        "date": date_str,
                        "close": float(row.get("Close", 0)) if row.get("Close") is not None else None
                    })
        except Exception:
            pass

        company_data = {
            "Company Name": info.get("shortName"),
            "Symbol": symbol,
            "Sector": info.get("sector"),
            "Industry": info.get("industry"),
            "Country": info.get("country"),
            "City": info.get("city"),
            "Employees": info.get("fullTimeEmployees"),

            "Current Stock Price": info.get("regularMarketPrice"),
            "52 Week Low": info.get("fiftyTwoWeekLow"),
            "52 Week High": info.get("fiftyTwoWeekHigh"),
            "50 Day Average": info.get("fiftyDayAverage"),
            "200 Day Average": info.get("twoHundredDayAverage"),

            "Market Cap": info.get("marketCap"),
            "Enterprise Value": info.get("enterpriseValue"),
            "Trailing P/E": info.get("trailingPE"),
            "Forward P/E": info.get("forwardPE"),
            "Price to Book": info.get("priceToBook"),
            "PEG Ratio": info.get("pegRatio"),

            "Revenue Growth": info.get("revenueGrowth"),
            "Earnings Growth": info.get("earningsGrowth"),
            "Gross Margins": info.get("grossMargins"),
            "Operating Margins": info.get("operatingMargins"),
            "EBITDA Margins": info.get("ebitdaMargins"),
            "Profit Margins": info.get("profitMargins"),

            "Total Cash": info.get("totalCash"),
            "Free Cash Flow": info.get("freeCashflow"),
            "Operating Cash Flow": info.get("operatingCashflow"),
            "EBITDA": info.get("ebitda"),
            "Debt to Equity": info.get("debtToEquity"),
            "Current Ratio": info.get("currentRatio"),
            "Return on Equity": info.get("returnOnEquity"),
            "Return on Assets": info.get("returnOnAssets"),

            "Dividend Yield": info.get("dividendYield"),
            "Payout Ratio": info.get("payoutRatio"),

            "Beta": info.get("beta"),
            "Short Ratio": info.get("shortRatio"),

            "Recommendation": info.get("recommendationKey"),
            "Target Mean Price": info.get("targetMeanPrice"),

            "Quarterly Financials (Last 4 Quarters)": last_4,
            "Prices": prices
        }

        return json.dumps(company_data, indent=2)

    except Exception as e:
        return json.dumps({"error": f"Error fetching stock data: {str(e)}"})
