# src/ollama_ia.py

import ollama
import json

def gerar_plano_acao(comando_usuario, estado_jogo):
    """
    Envia o comando e o estado do jogo para o Ollama e retorna um plano em JSON.
    """
    prompt = f"""
Você é um jogador humano no Minecraft 1.20.4.
Seu objetivo é interpretar comandos e criar um plano de ação passo a passo.

### Estado atual do jogo:
- Inventário: {estado_jogo['inventario']}
- Localização: {estado_jogo['localizacao']}
- Ferramentas disponíveis: {estado_jogo['ferramentas']}

### Comando da live:
"{comando_usuario}"

### Tarefas:
1. Entenda o que o usuário deseja.
2. Crie um plano de ação passo a passo (em JSON).
3. Exemplo de formato:
[
  {{ "acao": "mover_para", "posicao": [100, 64, 100] }},
  {{ "acao": "coletar", "item": "madeira", "quantidade": 10 }},
  {{ "acao": "craftar", "item": "picareta_pedra", "quantidade": 1 }},
  {{ "acao": "construir", "estrutura": "casa", "tamanho": [5, 3, 5] }}
]

Responda apenas com o plano em JSON, sem explicações.
"""

    try:
        response = ollama.generate(model="llama3", prompt=prompt)
        return json.loads(response["response"])
    except Exception as e:
        print(f"[Erro] Falha ao gerar plano: {e}")
        return []
