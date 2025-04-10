from utils import gravar_audio, transcrever_audio, responder_chat, sintetizar_fala, tocar_audio

def main():
    while True:
        caminho_audio = gravar_audio()
        texto = transcrever_audio(caminho_audio)
        print(f"🗣️ Você disse: {texto}")

        resposta = responder_chat(texto)
        print(f"🤖 Resposta: {resposta}")

        caminho_resposta_audio = sintetizar_fala(resposta)
        tocar_audio(caminho_resposta_audio)

        print("\n🟢 Pronto para nova interação (SPACE para gravar, ESC para sair)...")

if __name__ == "__main__":
    main()