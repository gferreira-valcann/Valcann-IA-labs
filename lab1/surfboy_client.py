import asyncio
import json
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from strands import Agent

async def create_mcp_agent():
    """Cria um agente Strands com ferramentas MCP"""
    
    # Configurar servidor MCP
    server_params = StdioServerParameters(
        command="python",
        args=["surfboy_server.py"]
    )
    
    # Conectar ao servidor MCP
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Inicializar sessão
            await session.initialize()
            
            # Listar ferramentas disponíveis
            tools_response = await session.list_tools()
            print(f"Ferramentas disponíveis: {[t.name for t in tools_response.tools]}")
            
            # Criar wrappers de ferramentas para o Strands
            mcp_tools = []
            
            for tool_info in tools_response.tools:
                # Criar função wrapper para cada ferramenta
                async def create_tool_wrapper(tool_name):
                    async def wrapper(**kwargs):
                        response = await session.call_tool(tool_name, arguments=kwargs)
                        # Extrair texto da resposta
                        text_parts = []
                        for content in response.content:
                            if content.type == "text":
                                text_parts.append(content.text)
                        return "\n".join(text_parts)
                    return wrapper
                
                wrapper = await create_tool_wrapper(tool_info.name)
                wrapper.__name__ = tool_info.name
                wrapper.__doc__ = tool_info.description
                mcp_tools.append(wrapper)
            
            # Criar agente Strands com as ferramentas MCP
            agent = Agent(
                system_prompt=(
                    "Você é um especialista em condições de surf. "
                    "Analise condições de maré, ondas e tempo para prática de surf. "
                    "Use as ferramentas disponíveis para obter informações atualizadas. "
                    "Sempre que o usuário mencionar uma localização, use as ferramentas "
                    "para buscar informações sobre condições de surf e ataques de tubarão."
                ),
                tools=mcp_tools
            )
            
            return agent

async def main():
    """Função principal"""
    
    # Obter prompt
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = "Como estão as condições de surf na praia do pina, recife?"
    
    try:
        # Criar agente com ferramentas MCP
        agent = await create_mcp_agent()
        
        # Executar agente
        print(f"Prompt: {prompt}")
        print("\n" + "="*50 + "\n")
        
        result = await agent(prompt)
        print(result)
        
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())