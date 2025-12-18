from strands import Agent, tool
import os
import boto3


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
        return "KNOWLEDGE_BASE_ID is not set"

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

agent("fale sobre o bloco homem da meia noite")