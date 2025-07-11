# %% [markdown]

# essential installation

# %%

pip install apify_client

pip install pyautogen

pip install -U ipywidgets

# %%

import os

from dotenv import load_dotenv

load_dotenv()

# %% [markdown]

# config list of llm and apify

# %%

import os

config_list= [

{

"model": "",

"api_type": "azure",

"api_key": "",

"base_url": "",

"api_version":""

}

]

apify_api_key = apify_api_key

# %%

from apify_client import ApifyClient

from typing_extensions import Annotated

def scrape_page(url: Annotated[str, "The URL of the web page to scrape"]) -> Annotated[str, "Scraped content"]:

# Initialize the ApifyClient with your API token

client = ApifyClient(token=apify_api_key)

# Prepare the Actor input

run_input = {

"startUrls": [{"url": url}],

"useSitemaps": False,

"crawlerType": "playwright:firefox",

"includeUrlGlobs": [],

"excludeUrlGlobs": [],

"ignoreCanonicalUrl": False,

"maxCrawlDepth": 0,

"maxCrawlPages": 1,

"initialConcurrency": 0,

"maxConcurrency": 200,

"initialCookies": [],

"proxyConfiguration": {"useApifyProxy": True},

"maxSessionRotations": 10,

"maxRequestRetries": 5,

"requestTimeoutSecs": 60,

"dynamicContentWaitSecs": 10,

"maxScrollHeightPixels": 5000,

"removeElementsCssSelector": """nav, footer, script, style, noscript, svg,

[role=\"alert\"],

[role=\"banner\"],

[role=\"dialog\"],

[role=\"alertdialog\"],

[role=\"region\"][aria-label*=\"skip\" i],

[aria-modal=\"true\"]""",

"removeCookieWarnings": True,

"clickElementsCssSelector": '[aria-expanded="false"]',

"htmlTransformer": "readableText",

"readableTextCharThreshold": 100,

"aggressivePrune": False,

"debugMode": True,

"debugLog": True,

"saveHtml": True,

"saveMarkdown": True,

"saveFiles": False,

"saveScreenshots": False,

"maxResults": 9999999,

"clientSideMinChangePercentage": 15,

"renderingTypeDetectionPercentage": 10,

}

# Run the Actor and wait for it to finish

run = client.actor("aYG0l9s7dbB7j3gbS").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)

text_data = ""

for item in client.dataset(run["defaultDatasetId"]).iterate_items():

text_data += item.get("text", "") + "\n"

average_token = 0.75

max_tokens = 2000  # slightly less than max to be safe 32k

text_data = text_data[: int(average_token * max_tokens)]

return text_data

# %% [markdown]

# created two agents webscrapper and user proxy

# %%

from autogen import ConversableAgent, register_function

# Create web scrapper agent.

scraper_agent = ConversableAgent(

"WebScraper",

llm_config={"config_list": config_list},

system_message="You are a web scrapper and you can scrape any web page using the tools provided. "

"Returns 'TERMINATE' when the scraping is done.",

)

# Create user proxy agent.

user_proxy_agent = ConversableAgent(

"UserProxy",

llm_config=False,  # No LLM for this agent.

human_input_mode="NEVER",

code_execution_config=False,  # No code execution for this agent.

is_termination_msg=lambda x: x.get("content", "") is not None and "terminate" in x["content"].lower(),

default_auto_reply="Please continue if not finished, otherwise return 'TERMINATE'.",

)

# Register the function with the agents.

register_function(

scrape_page,

caller=scraper_agent,

executor=user_proxy_agent,

name="scrape_page",

description="Scrape a web page and return the content.",

)

# %% [markdown]

# intiated the chat between both agent

# %%

chat_result = user_proxy_agent.initiate_chat(

scraper_agent,

message="Can you scrape https://en.wikipedia.org/wiki/PhonePe for me?",

max_turns = 2,

summary_method="reflection_with_llm",

summary_args={

"summary_prompt": """Summarize the scraped content and format summary EXACTLY as follows:

- --
- Company name*:

`Acme Corp`

- --
- Website*:

`acmecorp.com`

- --
- Description*:

`Company that does things.`

- --
- Tags*:

`Manufacturing. Retail. E-commerce.`

- --
- Takeaways*:

`Provides shareholders with value by selling products.`

- --
- Questions*:

`What products do they sell? How do they make money? What is their market share?`

- --

"""

},

)