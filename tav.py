from tavily import TavilyClient

tavily_client = TavilyClient(api_key="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")
response = tavily_client.search("maré e ondas na praia do recife")

print(response)