# 🏆 FIFA Club World Cup Statistics Bot

Este projeto coleta e envia automaticamente **estatísticas de partidas do Mundial de Clubes da FIFA 2025** via **WhatsApp**, a cada 5 minutos.

---

## 📌 Funcionalidades

- 🔎 Rastreia partidas do site [Lance!](https://www.lance.com.br/temporeal/agenda).
- 📊 Coleta estatísticas como:
  - Posse de bola
  - Chutes no gol
  - Passes certos e errados
  - Escanteios
  - Impedimentos
- ⏱ Atualizações automáticas a cada 5 minutos (se o jogo já tiver começado).
- 💬 Envio das informações via serviço de WhatsApp.

---

## 📦 Instalação

# Clone o repositório
git clone https://github.com/goulartandrey/rpa_challenge.git

cd fifa-club-WC

# Crie e ative o ambiente virtual (opcional)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

## ⚙️ Configuração
Para o envio de mensagens com a api do Callmebot (https://www.callmebot.com/blog/free-api-whatsapp-messages/), seguir os passos abaixo:
1. Adicionar aos seus contatos o número +34 644 33 66 63
2. Enviar a seguinte e exata mensagem: "I allow callmebot to send me messages" para permitir o envio de mensagens para o seu número
3. Você receberá uma chave de api numérica
4. Renomeio o arquivo **.env.example** para **.env** e coloque seu número de telefone no formato +555199999999 (sem o costumerio "9" adicional) na variável CALLME_BOT_WHATSAPP_NUMBER
5. Adicione a chave de api recebida no passo 3 da api Callmebot no .env na variável CALLME_BOT_API_KEY
6. Pronto, é só executar o arquivo main.py and the fun has started 😉
