import asyncio
import json
import sys
from typing import Any, Dict, List
import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

class SurfToolsMCPServer:
    def __init__(self):
        self.tavily = TavilyClient(api_key=os.getenv("TAVILY_KEY"))
        
    async def initialize(self) -> Dict[str, Any]:
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "SurfTools",
                "version": "1.0.0"
            }
        }
    
    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "query_shark_attack",
                "description": "Consulta ataques de tubarão em uma localização específica",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "localizacao": {
                            "type": "string",
                            "description": "Local, comumente uma praia e a cidade (ex: 'praia do pina, recife')"
                        }
                    },
                    "required": ["localizacao"]
                }
            },
            {
                "name": "query_weather",
                "description": "Consulta clima, maré e ondas de uma localização para análise de surf",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "localizacao": {
                            "type": "string",
                            "description": "Local, comumente uma praia e a cidade (ex: 'itacoatiara, niterói')"
                        }
                    },
                    "required": ["localizacao"]
                }
            }
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if name == "query_shark_attack":
            return await self._query_shark_attack(arguments["localizacao"])
        elif name == "query_weather":
            return await self._query_weather(arguments["localizacao"])
        else:
            raise ValueError(f"Ferramenta desconhecida: {name}")
    
    async def _query_shark_attack(self, localizacao: str) -> Dict[str, Any]:
        query = f"ataques de tubarão em {localizacao}"
        
        try:
            search_result = self.tavily.search(
                query=query,
                max_results=5,
                include_answer=True
            )
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Consulta de ataques de tubarão em {localizacao}:\n\n"
                               f"Resultados da busca:\n{json.dumps(search_result, ensure_ascii=False, indent=2)}"
                    }
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Erro ao consultar ataques de tubarão: {str(e)}"
                    }
                ]
            }
    
    async def _query_weather(self, localizacao: str) -> Dict[str, Any]:
        query = f"previsão de maré ondas surf {localizacao} condições do mar"
        
        try:
            search_result = self.tavily.search(
                query=query,
                max_results=5,
                include_answer=True
            )
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Consulta de condições de surf em {localizacao}:\n\n"
                               f"Resultados da busca:\n{json.dumps(search_result, ensure_ascii=False, indent=2)}"
                    }
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Erro ao consultar condições de surf: {str(e)}"
                    }
                ]
            }

async def handle_request(server: SurfToolsMCPServer, request: Dict[str, Any]) -> Dict[str, Any]:
    method = request.get("method")
    request_id = request.get("id")
    
    if method == "initialize":
        result = await server.initialize()
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
    
    elif method == "tools/list":
        tools = server.list_tools()
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": tools
            }
        }
    
    elif method == "tools/call":
        params = request.get("params", {})
        name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            result = await server.call_tool(name, arguments)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
    
    else:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32601,
                "message": f"Método não encontrado: {method}"
            }
        }

async def main():
    server = SurfToolsMCPServer()    
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line.strip())
            response = await handle_request(server, request)
            
            print(json.dumps(response, ensure_ascii=False), flush=True)
            
        except json.JSONDecodeError:
            # Enviar erro de JSON inválido
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                }
            }
            print(json.dumps(error_response), flush=True)
            
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    asyncio.run(main())