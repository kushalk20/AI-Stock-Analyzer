

# 📈 AI Stock Analyzer


[![CrewAI](https://img.shields.io/badge/CrewAI-1.7.2-orange?logo=crewai&logoColor=white)](https://crewai.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-brightgreen?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Inference-blueviolet?logo=huggingface&logoColor=white)](https://huggingface.co)
[![Llama](https://img.shields.io/badge/Llama-3.3_70B-yellow?logo=llama&logoColor=white)](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct)
[![YahooFinance](https://img.shields.io/badge/YahooFinance-Data-blue?logo=yahoo&logoColor=white)](https://finance.yahoo.com)

**AI-powered stock research platform** that analyzes company news, financials, and delivers **Buy/Sell/Hold** recommendations using CrewAI multi-agent system and Llama 3.3 70B.


## 🚀 Features

| 📰 **News Research** | 📊 **Financial Analysis** | 🎯 **AI Recommendations** |
|---------------------|---------------------------|---------------------------|
| Real-time news via Serper | 50+ metrics (P/E, EBITDA, Debt/Equity) | Buy/Sell/Hold with rationale |
| Press releases & updates | Quarterly financials | Target prices & timelines |
| Semantic summaries | 1Y price history | Risk assessment |

## 🛠 Tech Stack
```
Frontend: FastAPI + HTML/JS (Single Page App)
AI: CrewAI + Llama 3.3 70B (Hugging Face)
Data: yfinance + yahooquery + SerperDev
Deployment: pyngrok + uvicorn
```

## 📁 Project Structure
```
ai-stock-analyzer/
├── agents.py # 3 specialized AI agents
├── tools.py # Serper search + stock data tools
├── tasks.py # Sequential task pipeline
├── app.py # FastAPI backend + CrewAI orchestration
├── index.html # Modern SPA frontend
└── requirements.txt # Dependencies
```

## ⚙️ Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/YOUR_USERNAME/ai-stock-analyzer.git
cd ai-stock-analyzer
```
### 2. Environment
```bash
cp .env.example .env
# Add your keys:
# HF_TOKEN=your_huggingface_token
# SERPER_API_KEY=your_serper_key
```
### 3. Install & Run
```bash
pip install -r requirements.txt
python app.py
```
### 4. Access
```bash
http://localhost:8000
```

## 🎯 How It Works
```bash
1. User searches "Tesla" → Autocomplete symbols
2. Click Analyze → 3 agents collaborate:
   📰 News Agent → SerperDevTool → Latest headlines
   📈 Stock Agent → yfinance → 50+ metrics + charts  
   🎯 Advisor → Synthesizes → Buy/Sell/Hold + Target Price
3. Results display in clean dashboard
```

## 🧠 AI Agents
| Agent | Role | Tools |
|-------|------|-------|
| **News Researcher** | Latest news & updates | SerperDev |
| **Stock Analyst** | Financial metrics & trends | yfinance |
| **Investment Advisor** | Final Buy/Sell/Hold | News + Financials |

## 📊 Sample Output
```bash
Company: Tesla (TSLA)
Financials: P/E 85.2 | Revenue Growth +12% | Market Cap $1.2T
News: Q4 deliveries beat estimates | Robotaxi event Feb 2026
✅ RECOMMENDATION: **BUY** | Target $420 (12 months)
```

## 🔑 Environment Variables
| Key | Sources | Purpose |
|-------|------|-------|
| **HF_TOKEN** | Hugging Face | Llama 3.3 70B inference |
| **SERPER_API_KEY** | Serper.dev | 	Real-time news search |

## 🤝 **Contributing**

1. Fork the repo
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing-feature`)
5. Open Pull Request


## 🙏 **Acknowledgments**
- [CrewAI](https://crewai.com) - Multi-agent orchestration framework
- [Hugging Face](https://huggingface.co) - Llama 3.3 70B inference endpoint
- [FastAPI](https://fastapi.tiangolo.com) - Lightning-fast API framework
- [Yahoo Finance](https://finance.yahoo.com) - Comprehensive stock data via yfinance
- [Serper.dev](https://serper.dev) - Real-time news search API
- [yahooquery](https://github.com/dpguthrie/yahooquery) - Advanced Yahoo Finance queries
---

<div align="center">

**⭐ Star this repo if it helped you!**

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Made with-HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white](https://img.shields.io/badge/Made%20with-HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://html.spec.whatwg.org)
[![Made with-FastAPI-009485?style=for-the-badge&logo=fastapi&logoColor=white](https://img.shields.io/badge/Made%20with-FastAPI-009485?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

</div>
