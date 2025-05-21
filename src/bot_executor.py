import os
import json
import subprocess
from ollama_ia import gerar_plano_acao

estado_jogo = {
    "inventario": [],
    "localizacao": "floresta",
    "ferramentas": []
}

def executar_plano(plano):
    for passo in plano:
        acao = passo["acao"]
        args = []

        if acao == "mover_para":
            args = list(map(str, passo["posicao"]))
        elif acao == "coletar":
            args = [passo["item"], str(passo.get("quantidade", 1))]
        elif acao == "domar":
            args = [passo["animal"]]
        else:
            print(f"[Ignorando] Ação desconhecida: {acao}")
            continue

        print(f"[Bot] Executando: {acao} {' '.join(args)}")
        try:
            subprocess.run(["node", "bot.js", acao, *args])
        except Exception as e:
            print(f"[Erro ao executar ação {acao}]: {e}")

if __name__ == "__main__":
    comando_usuario = os.getenv("MINECRAFT_COMMAND", "Domar um cavalo")
    print(f"[Comando Automático]: {comando_usuario}")

    plano = gerar_plano_acao(comando_usuario, estado_jogo)
    print("[Plano gerado]:\n", json.dumps(plano, indent=2))
    executar_plano(plano)
