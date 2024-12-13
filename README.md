# Bot de Música para Discord 🎵

## Funcionalidades

- Tocar músicas diretamente do YouTube.
- Adicionar músicas a uma fila de reprodução.
- Limpar a fila de reprodução.
- Pausar, resumir e parar a música.
- Exibir a lista atual de músicas na fila.

## Pré-requisitos

Certifique-se de que você tenha o seguinte instalado em seu sistema:

- Python 3.8 ou superior
- [FFmpeg](https://ffmpeg.org/) (inclua o caminho do executável em seu sistema)
- Bibliotecas Python necessárias (detalhadas abaixo)
- Um bot registrado no Discord Developer Portal com seu token

## Instalação

1. **Clone este repositório:**

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <PASTA_DO_PROJETO>
   ```

2. **Crie um ambiente virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**

   Crie um arquivo `.env` na pasta principal do projeto com o seguinte conteúdo:

   ```env
   discord_token=SEU_TOKEN_DO_DISCORD
   ```

5. **Configure o caminho do FFmpeg:**

   Certifique-se de que o FFmpeg esteja instalado e configure o caminho no script, na variável `ffmpeg_options`.

## Execução

1. **Inicie o bot:**

   Execute o script `main.py`:

   ```bash
   python main.py
   ```

2. **Adicione o bot ao seu servidor:**

   Use o link de convite gerado no Discord Developer Portal para adicionar o bot ao seu servidor.

## Comandos Disponíveis

- **Tocar música:**  
  `zeros play <nome ou link>`  
  Toca uma música do YouTube. Se já estiver tocando, adiciona a música à fila.

- **Limpar fila:**  
  `zeros clear_queue`  
  Limpa toda a fila de músicas.

- **Pausar música:**  
  `zeros pause`  
  Pausa a música atual.

- **Retomar música:**  
  `zeros resume`  
  Retoma a música pausada.

- **Parar música:**  
  `zeros stop`  
  Para a música atual e desconecta o bot.

- **Exibir fila:**  
  `zeros fila`  
  Mostra as músicas na fila.

## Tecnologias Utilizadas

- [discord.py](https://discordpy.readthedocs.io/) - Biblioteca para interagir com a API do Discord.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Biblioteca para buscar e reproduzir músicas do YouTube.
- [FFmpeg](https://ffmpeg.org/) - Ferramenta para processamento de áudio e vídeo.

