import os
import requests
from dotenv import load_dotenv


load_dotenv()


class WhatsAppService:
    def __init__(self):
        self.__whatsapp_url = 'https://api.callmebot.com/whatsapp.php'
        self.__whatsapp_number = os.getenv('CALLME_BOT_WHATSAPP_NUMBER')
        self.__api_key = os.getenv('CALLME_BOT_API_KEY')

    def send_message(self, message, team_a, team_b, finished):
        response = requests.get(
            url=f"{self.__whatsapp_url}?phone={self.__whatsapp_number}&text={message}&apikey={self.__api_key}")

        if response.status_code == 200:
            return_message = 'Mensagem enviada com sucesso.'
            if not finished:
                return_message += ' Próxima atualização em 5 minutos'
            print(f"{team_a} x {team_b}: {return_message}")
        else:
            print(
                f"Erro ao enviar mensagem: {response.status_code} - {response.text}")
        return response.text
