"**Web Scraping with LLMs**":

---

````markdown
# 🕷️ Web Scraping with Large Language Models (LLMs)

## 📘 Introduction

Web scraping is the process of extracting data from websites, traditionally done through scripts that parse HTML. However, with the emergence of Large Language Models (LLMs), such as OpenAI's GPT models, scraping has become more adaptive and robust. LLMs help handle dynamic websites and evolving layouts more intelligently.

---

## 🚀 Methods of LLM-Based Web Scraping

We explore 3 powerful LLM-assisted scraping approaches:

1. [Langchain](#1-langchain)
2. [ScrapeGraphAI](#2-scrapegraphai)
3. [Multi-Agent Systems](#3-multi-agent-systems-using-autogen--apify)

---

## 1. ⚙️ Langchain

### 🔄 Pipeline Components:

- **Search:** Query → URL (e.g., via GoogleSearchAPIWrapper)
- **Load:** URL → HTML (e.g., AsyncHtmlLoader / AsyncChromiumLoader)
- **Transform:** HTML → Text (e.g., BeautifulSoup, HTML2Text)

### 🧩 Components

#### 🔌 Loader

- Loads HTML from URLs asynchronously.
- Extracts text from tags like `<p>`, `<li>`, `<div>`, and `<a>`.

#### 🔄 Transformer

- Converts HTML into readable text using `BeautifulSoup` or `HTML2Text`.

#### ✅ Advantage of Using LLM Functions

- Traditional scrapers break when site layouts change.
- With LLM + OpenAI Functions, your code adapts without constant rewriting.
- Uses `gpt-3.5-turbo-0613` to enable structured extraction via schema.

### 📄 Example Schema

```python
schema = {
  "properties": {
    "news_article_title": {"type": "string"},
    "news_article_summary": {"type": "string"},
  },
  "required": ["news_article_title", "news_article_summary"],
}
````

### 🔍 Sample Scraper Code

```python
from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain.chains.openai_functions import create_openai_fn_extraction_chain
import pprint

def scrape_with_playwright(urls, schema):
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(docs, tags_to_extract=["span"])

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=0)
    splits = splitter.split_documents(docs_transformed)

    extract = create_openai_fn_extraction_chain(schema)
    extracted_content = extract.run(splits[0].page_content)
    
    pprint.pprint(extracted_content)
    return extracted_content

urls = ["https://www.wsj.com"]
extracted_content = scrape_with_playwright(urls, schema)
```

> **Note**: You may encounter `NotImplementedError` depending on Langchain version.

---

## 2. 🔗 ScrapeGraphAI

A flexible, LLM-powered framework that adapts to web layout changes—minimizing manual updates.

### ✅ Key Features

* Supports GPT, Gemini, HuggingFace, Azure, and **local models** via **Ollama**.
* Uses **graph pipelines** for different tasks.

### 🧠 Common Graph Types

| Graph             | Description                                                   |
| ----------------- | ------------------------------------------------------------- |
| SmartScraperGraph | One-page scraper using URL + prompt                           |
| SearchGraph       | Multi-page search engine scraper (built on SmartScraperGraph) |
| SpeechGraph       | TTS pipeline with audio + text output (requires URL + prompt) |

---

## 3. 🤖 Multi-Agent Systems using Autogen + Apify

### 💡 Why Multi-Agent?

* Handles complex interactions
* Allows autonomous data extraction
* Human or no-human supervision

### 🛠 Agents Used

#### 🧑‍💻 Web Scraper Agent

* Uses `Apify` tools
* GPT-3.5-turbo powered
* Terminates on task completion

#### 👤 User Proxy Agent

* Can be human-controlled or autonomous
* Terminates upon receiving `terminate` from peer agent

### 🌐 Apify API

Apify is a powerful, scalable platform for scraping dynamic and JS-heavy websites. It provides:

* Ready-made and custom scrapers
* Cloud infrastructure
* Proxy management
* Schedule and store scraped data

---

### 💬 Chat Flow Example

```markdown
UserProxy → WebScraper:
Can you scrape agentops.ai for me?

WebScraper:
Suggested tool call:
{
  "url": "https://www.agentops.ai"
}

>>> EXECUTING scrape_page...

WebScraper:
Sure, here's the information from the website agentops.ai:

- Fixes poor AI agent performance.
- Introduces `AgentOps`: tools for observability and evals.
- Easy integration with 3 lines of code.
- Offers generous free tier.

Summary Template Output:

---

*Company name*:
`AgentOps`

*Website*:
`agentops.ai`

*Description*:
`Compliant AI agents with debugging and observability.`

*Tags*:
`AI. Observability. Debugging. Compliance.`

*Takeaways*:
`Provides tools for better-performing AI agents.`

*Questions*:
`How does AgentOps integrate? What makes it compliant?`
```

---

## 📌 Conclusion

LLMs are revolutionizing the way web scraping is done:

* No need for brittle parsing scripts
* Easily adapt to HTML changes
* Semantic data extraction with function calling

Choose from tools like **Langchain**, **ScrapeGraphAI**, or **Multi-Agent Autogen** based on your requirements and technical preferences.

---

## 📚 References

* [Langchain](https://github.com/langchain-ai/langchain)
* [ScrapeGraphAI](https://github.com/Ventura-Technology/scrapegraph-ai)
* [Autogen](https://github.com/microsoft/autogen)
* [Apify](https://apify.com/)

---


