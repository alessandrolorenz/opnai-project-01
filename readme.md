# AI Voice Assistant

Este projeto é um assistente de voz com inteligência artificial que permite aos usuários interagir com um modelo de IA por meio de comandos de voz. Ele grava áudio, transcreve, gera respostas usando o modelo GPT da OpenAI e sintetiza as respostas em fala.

## Funcionalidades

- **Gravação de Áudio**: Grava áudio usando o microfone.
- **Reconhecimento de Fala**: Transcreve o áudio gravado em texto usando o modelo Whisper da OpenAI.
- **Chat com IA**: Gera respostas para os prompts do usuário usando o modelo GPT-3.5-turbo da OpenAI.
- **Texto para Fala**: Converte as respostas geradas pela IA em áudio.
- **Reprodução de Áudio**: Reproduz o áudio sintetizado.

## Pré-requisitos

- Python 3.10 ou superior
- Chave de API da OpenAI
- Pacotes Python necessários (veja abaixo)

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/your-username/ai-voice-assistant.git
   cd ai-voice-assistant
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Crie um arquivo `.env` no diretório raiz do projeto e adicione suas chaves de API:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

## Uso

1. Execute o aplicativo:
   ```bash
   python main.py
   ```

2. Siga as instruções exibidas na tela:
   - Pressione `SPACE` para começar a gravar.
   - Pressione `ENTER` para parar a gravação.
   - Pressione `ESC` para sair do aplicativo.

3. O assistente transcreverá sua fala, gerará uma resposta e reproduzirá a resposta como áudio.

## Visão Geral das Funções

### Arquivo `utils.py`

- **`gravar_audio(samplerate=16100)`**  
  Grava áudio do microfone e salva como um arquivo `.wav`.

- **`transcrever_audio(caminho_arquivo)`**  
  Transcreve o áudio gravado usando o modelo Whisper da OpenAI.

- **`responder_chat(prompt)`**  
  Envia o prompt do usuário para o modelo GPT da OpenAI e retorna a resposta da IA.

- **`sintetizar_fala(texto)`**  
  Converte o texto da resposta da IA em fala e salva como um arquivo `.mp3`.

- **`tocar_audio(caminho_arquivo)`**  
  Reproduz o arquivo de áudio sintetizado.

### Arquivo `main.py`

- O script principal orquestra a interação entre o usuário e o assistente de voz, chamando as funções utilitárias.

## Dependências

Os seguintes pacotes Python são necessários:

- `openai`
- `sounddevice`
- `soundfile`
- `python-dotenv`
- `keyboard`

Instale-os com:
```bash
pip install openai sounddevice soundfile python-dotenv keyboard
```

## Notas

- Certifique-se de que seu microfone esteja configurado corretamente e acessível.
- O aplicativo foi projetado para Windows, mas pode ser adaptado para macOS e Linux.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

## Agradecimentos

- [OpenAI](https://openai.com/) por suas APIs.
- [SoundDevice](https://python-sounddevice.readthedocs.io/) e [SoundFile](https://pysoundfile.readthedocs.io/) para manipulação de áudio.
- [Python-Keyboard](https://github.com/boppreh/keyboard) para manipulação de entrada do teclado.