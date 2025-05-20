import ollama
import json

# Configuração do Ollama
MODEL = "llama3"  # ou "phi3", "mistral", etc.

def gerar_plano_acao(comando_usuario, estado_jogo):
    """
    Envia o comando e o estado do jogo para o Ollama e recebe um plano de ações.
    """
    prompt = f"""
Você é um jogador humano no Minecraft versão 1.19.1.
Seu objetivo é interpretar comandos da live e criar um plano de ação passo a passo.

### Estado atual do jogo:
- Inventario: {estado_jogo['inventario']}
- Localização: {estado_jogo['localizacao']}
- Ferramentas disponíveis: {estado_jogo['ferramentas']}

### Comando da live:
"{comando_usuario}"

### Tarefas:
1. Entenda o que o usuário deseja.
2. Crie um plano de ação passo a passo (em JSON).
3. Exemplo de formato:
[
  {{ "acao": "coletar", "item": "madeira", "quantidade": 10 }},
  {{ "acao": "craftar", "item": "picareta", "material": "pedra" }},
  {{ "acao": "ir_para", "posicao": [x, y, z] }},
  {{ "acao": "construir", "estrutura": "casa", "tamanho": [5, 3, 5] }}
]

Responda apenas com o plano em JSON, sem explicações.
"""

    try:
        response = ollama.generate(model=MODEL, prompt=prompt)
        plano = json.loads(response["response"])
        return plano
    except Exception as e:
        print(f"[Erro] Falha ao gerar plano: {e}")
        return []
        
