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

### Comandos válidos:
1. mover_para <x> <y> <z>
2. coletar <item> [quantidade]
3. craftar <item> [quantidade]
4. construir <estrutura> <largura> <altura> <profundidade>
5. domar <animal>
6. encantar <item> <enchant>
7. fazer_pocao <tipo>

### Exemplo de formato:
[
  {{ "acao": "mover_para", "posicao": [100, 64, 100] }},
  {{ "acao": "coletar", "item": "madeira", "quantidade": 10 }},
  {{ "acao": "domar", "animal": "cavalo" }}
]

Responda apenas com o plano em JSON, sem explicações.
"""

    try:
        response = ollama.generate(model="llama3", prompt=prompt)
        return json.loads(response["response"])
    except Exception as e:
        print(f"[Erro] Falha ao gerar plano: {e}")
        return []
