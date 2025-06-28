import time
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo

from clients.whatsapp_service import WhatsAppService

load_dotenv()


class MatchService:
    def __init__(self):
        self.__matches_url = []
        self.__matches_data = []

    def start_fun(self):
        while True:
            self.__matches_url.clear()
            self.__matches_data.clear()

            self.get_current_matches()
            self.get_match_data()

            for match in self.__matches_data:
                try:
                    if not self.has_match_started(match):
                        continue
                    stats = self.extract_statistics(match)
                    self.display_statistics(stats)
                except Exception as e:
                    print(f"Erro ao processar partida: {e}")

            print("Próxima atualizacao em 5 minutos\n")
            time.sleep(300)

    def get_current_matches(self):
        url = "https://www.lance.com.br/temporeal/agenda#2025-06-27"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.find_all("a", href=True):
            if "/partida/" in link["href"]:
                slug = link["href"].split("/partida/")[-1].replace("/", "")
                if slug.startswith("mundial-de-clubes-fifa-2025-"):
                    json_url = f"https://temporeal.lance.com.br/storage/matches/{slug}.json"
                    self.__matches_url.append(json_url)
                else:
                    print("Nenhuma partida do mundial de clubes no dia de hoje.")

    def get_match_data(self):
        for url in self.__matches_url:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    self.__matches_data.append(response.json())
                else:
                    print(
                        f"Falha ao acessar: {url} (Status {response.status_code})")
            except Exception as e:
                print(f"Erro ao acessar {url}: {e}")

    def has_match_started(self, match):
        start_time_utc = datetime.fromisoformat(
            match["match"]["start_in"].replace("Z", "+00:00"))
        start_time_brt = start_time_utc.astimezone(
            ZoneInfo("America/Sao_Paulo"))
        now = datetime.now(ZoneInfo("America/Sao_Paulo"))

        team_a = match['match']['team_a']['name']
        team_b = match['match']['team_b']['name']

        if now < start_time_brt:
            print(f"\nO jogo {team_a} x {team_b} ainda não começou.")
            print(
                f"Início previsto: {start_time_brt.strftime('%d/%m/%Y às %H:%M')} (horário de Brasília)\n")
            return False
        return True

    def extract_statistics(self, match_data):
        stats = match_data['match']['statistics']
        team_a = match_data['match']['team_a']['name']
        team_a_goals = match_data['match']['team_a_score_goals']
        team_b = match_data['match']['team_b']['name']
        team_b_goals = match_data['match']['team_b_score_goals']
        match_period = match_data['match']['match_period']['period']

        labels = {
            "Posse de bola": 0,
            "Chutes no gol": 1,
            "Passes certos": 4,
            "Passes errados": 5,
            "Impedimentos": 6,
            "Escanteios": 7
        }

        statistics = {
            "teams": {
                "team_a": team_a,
                "team_b": team_b
            },
            "data": {},
            "score": {
                "team_a": team_a_goals,
                "team_b": team_b_goals
            },
            "match_period": match_period
        }

        for label, index in labels.items():
            try:
                value_a = stats[index].get('team_a', 0)
                value_b = stats[index].get('team_b', 0)

                if label == "Posse de bola":
                    total = value_a + value_b or 1
                    value_a = round((value_a / total) * 100, 1)
                    value_b = round((value_b / total) * 100, 1)
                    statistics["data"][label] = {
                        team_a: f"{value_a}%",
                        team_b: f"{value_b}%"
                    }
                else:
                    statistics["data"][label] = {
                        team_a: value_a,
                        team_b: value_b
                    }
            except IndexError:
                statistics["data"][label] = {
                    team_a: 0,
                    team_b: 0
                }

        return statistics

    def display_statistics(self, statistics):
        team_a = statistics["teams"]["team_a"]
        gol_team_a = statistics["score"]["team_a"]
        gol_team_b = statistics["score"]["team_b"]
        team_b = statistics["teams"]["team_b"]
        match_period = statistics["match_period"]

        message = f"Estatísticas de {team_a} {gol_team_a} x {gol_team_b} {team_b} - {match_period}:\n"

        for stat_name, values in statistics["data"].items():
            stat_line = f"{stat_name}:\n  {team_a}: {values[team_a]}\n  {team_b}: {values[team_b]}\n"
            message += stat_line + "\n"
            message += "Próxima atualização em 5 minutos."

        whats_service = WhatsAppService()
        whats_service.send_message(
            message=message.strip(), team_a=team_a, team_b=team_b)
