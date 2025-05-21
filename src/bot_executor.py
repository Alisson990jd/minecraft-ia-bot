# src/bot_executor.py

import json
import subprocess

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
        args = []

        if acao == "mover_para":
            args = list(map(str, passo["posicao"]))
        elif acao == "coletar":
            args = [passo["item"], str(passo.get("quantidade", 1))]
        elif acao == "craftar":
            args = [passo["item"], str(passo.get("quantidade", 1))]
        elif acao == "construir":
            args = [passo["estrutura"], *map(str, passo["tamanho"])]
        elif acao == "domar":
            args = [passo["animal"]]
        elif acao == "encantar":
            args = [passo["item"], passo["enchant"]]
        elif acao == "fazer_pocao":
            args = [passo["tipo"]]
        else:
            print(f"Ação desconhecida: {acao}")
            continue

        print(f"[Bot] Executando: {acao} {' '.join(args)}")
        subprocess.run(["node", "bot.js", acao, *args])

if __name__ == "__main__":
    comando_usuario = input("Digite um comando: ")
    plano = gerar_plano_acao(comando_usuario, estado_jogo)
    print("[Plano gerado]:\n", json.dumps(plano, indent=2))
    executar_plano(plano)
