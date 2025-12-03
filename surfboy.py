from strands import Agent
from tavily import TavilyClient
from dotenv import load_dotenv
import sys
import os

load_dotenv()

TAVILY_KEY = os.getenv("TAVILY_KEY")

class Surfboy:
    
    def __init__(self):
        self.agent  = None
        self.tavily = TavilyClient(api_key=TAVILY_KEY)
        self.userInput = ""
        self.formatedInput = ""
        self.tavResponse = ""
        self.forecasting = ""

        self.initAgent()

    def initAgent(self):
        self.agent = Agent(
            system_prompt=(
                "você deve receber dados sobre condições maré, ondas e tempo de uma praia ou localidade"
                "depois faça uma analise se as condições estão proprias para a pratica do surf no local"
                "retire dos inputs informações sobre localidades especificas quando for pedido"
                "faça analises sobre condições de surf baseada nos dados que receber quando for pedido"
            )
        )


    def formatToValidBeachInput(self, userInput):
        self.userInput = userInput
        prompt = (
            "retire do seguinte input informações sobre a localização como praia e cidade e apresente de forma breve na forma: nome da praia, nome da cidade.\nO input é:  "

            + self.userInput
        )
        self.formatedInput = self.agent(prompt).message["content"][0]["text"]
        print("formated output" + self.formatedInput)

    def retrieveTavData(self):
        query = "previsão de maré e ondas para " + self.formatedInput
        self.tavResponse = self.tavily.search(query)

    def retrieveForecasting(self):
        prompt = (
            "baseado nas seguintes informações faça uma analise das condições de maré e ondas para surf: "
            + str(self.tavResponse)
        )

        self.forecasting = self.agent(prompt)

    def forecast(self, userInput):
        self.formatToValidBeachInput(userInput)
        self.retrieveTavData()
        self.retrieveForecasting()
        return self.forecasting


surfboy = Surfboy()
prompt = sys.argv[1]

if prompt == None:
    result = surfboy.forecast("como tá praia do pina, recife")
else:
    result = surfboy.forecast(prompt)

print(result)