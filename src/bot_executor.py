import json
import subprocess
from ollama_ia import gerar_plano_acao

# Estado inicial simulado
estado_jogo = {
    "inventario": [],
    "localizacao": "floresta",
    "ferramentas": []
}

def executar_plano(plano):
    """Envia cada ação do plano para o bot.js via linha de comando."""
    for passo in plano:
        acao = passo["acao"]
        if acao == "coletar":
            item = passo["item"]
            quantidade = passo.get("quantidade", 1)
            print(f"[Bot] Coletando {quantidade}x {item}...")
            subprocess.run(["node", "bot.js", "coletar", item, str(quantidade)])
        elif acao == "craftar":
            item = passo["item"]
            material = passo.get("material", "")
            print(f"[Bot] Craftando {item} com {material}...")
            subprocess.run(["node", "bot.js", "craftar", item, material])
        elif acao == "ir_para":
            pos = passo["posicao"]
            print(f"[Bot] Indo para posição {pos}...")
            subprocess.run(["node", "bot.js", "ir_para", *map(str, pos)])
        elif acao == "construir":
            estrutura = passo["estrutura"]
            tamanho = passo["tamanho"]
            print(f"[Bot] Construindo {estrutura} ({tamanho[0]}x{tamanho[1]}x{tamanho[2]})...")
            subprocess.run(["node", "bot.js", "construir", estrutura, *map(str, tamanho)])
        else:
            print(f"[Bot] Ação desconhecida: {acao}")

if __name__ == "__main__":
    comando_usuario = input("Digite um comando: ")
    plano = gerar_plano_acao(comando_usuario, estado_jogo)
    print("[Plano gerado]:", json.dumps(plano, indent=2))
    executar_plano(plano)
