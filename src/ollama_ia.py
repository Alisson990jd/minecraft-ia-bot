import ollama
import json

def gerar_plano_acao(comando_usuario, estado_jogo):
    prompt = f"""
Você é um jogador humano no Minecraft 1.20.4.
Seu objetivo é interpretar comandos e criar planos com os comandos abaixo:

### Comandos válidos:
1. mover_para <x> <y> <z>
2. coletar <item> [quantidade]
3. domar <animal>

### Comando da live:
"{comando_usuario}"

Responda apenas com o plano em JSON, sem explicações.
"""

    try:
        response = ollama.generate(model="llama3", prompt=prompt)
        return json.loads(response["response"])
    except Exception as e:
        print(f"[Erro] Falha ao gerar plano: {e}")
        return []
