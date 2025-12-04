from strands import Agent, tool
from tavily import TavilyClient
from dotenv import load_dotenv
import sys
import os

load_dotenv()
TAVILY_KEY = os.getenv("TAVILY_KEY")
tavily = TavilyClient(api_key=TAVILY_KEY)

@tool
def querySharkAtackTool(localizacao: str) -> str:
    """
    devolve uma tupla com resultado de crawl das paginas do florida museum sobre ataques de tubarão  e resultado de uma query sobre ataques de tubarão dada uma localização
    Args:
        localizacao: local, comumente uma praia e a cidade da praia
    """
    query = "noticias de ataque de tubarao em " + localizacao
    
    tavResponse = (
        tavily.crawl(url="https://www.floridamuseum.ufl.edu/shark-attacks/"),
        tavily.search(query)
    )

    return tavResponse

@tool
def queryWeatherTool(localizacao: str) -> str:
    """
    devolve um resultado de buscas do tavily pelo clima, maré e ondas de uma localizacao
    Args:
        localizacao: local, comumente uma praia e a cidade da praia
    """
    query = "previsão de maré e ondas para " + localizacao
    tavResponse = tavily.search(query)
    return tavResponse

agent = Agent(
    system_prompt=(
        "você deve receber dados sobre condições maré, ondas e tempo de uma praia ou localidade"
        "depois faça uma analise se as condições estão proprias para a pratica do surf no local"
        "retire dos inputs informações sobre localidades especificas quando for pedido"
        "faça analises sobre condições de surf baseada nos dados que receber quando for pedido"
    ),
    tools=[queryWeatherTool, querySharkAtackTool]
)

prompt = sys.argv[1]

if prompt == None:
    result = agent("como tá praia do pina, recife")
else:
    result = agent(prompt)

print(result)