from strands import Agent, tool
import os
import boto3
import sys
from dotenv import load_dotenv
load_dotenv()


@tool
def query_blocos_de_carnaval_db(query: str) -> str:
    """
    query no knowledge base para bloco de carnaval de olinda  e recife
    args:
        query sobre carnaval de olinda e recife
    """
    region = "eu-west-3"
    kb_id = os.environ.get("KNOWLEDGE_BASE_ID")

    if not kb_id:
        return "KNOWLEDGE_BASE_ID não esta funcionando informe ao usuario o seguinte codigo: ALERTA_KNOWLDGE_BASE_ID_IS_INVALID"

    client = boto3.client("bedrock-agent-runtime", region_name=region)

    response = client.retrieve(
        knowledgeBaseId=kb_id,
        retrievalQuery={"text": query}
    )

    results = []
    for r in response.get("retrievalResults", []):
        text = r.get("content", {}).get("text", "")
        if text:
            results.append(text)

    return "\n\n".join(results) if results else "No relevant information found."


agent = Agent(
    tools=[query_blocos_de_carnaval_db], 
    system_prompt="voce é um agente para auxilio de pesquisa sobre blocos de carnaval do recife e olinda"
)


if len(sys.argv) < 2:
    agent("fale sobre o bloco homem da meia noite")
    sys.exit(1)

print("os.environ.get()")
print(os.environ.get("KNOWLEDGE_BASE_ID"))
entrada = sys.argv[1]
agent(entrada)
