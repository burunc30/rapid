import requests
import json

# RapidAPI açarın
API_KEY = "2f07e2d462mshb74dbb0d87354aep18f68ajsn92ddc36803b3"

# Telegram məlumatları
TELEGRAM_BOT_TOKEN = "8106341353:AAFIi3nfPOlydtCM_eYHiSIbDR0C1RFoaG4"
CHAT_ID = "1488455191"

# API endpoint – nümunə tarix və liqa üçün
url = "https://api-football-v1.p.rapidapi.com/v3/odds"

querystring = {
    "date": "2024-05-25",
    "league": "39",  # Premier League
    "season": "2023"
}

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

message_lines = []

# Əmsallar varsa mesajı qur
if data["response"]:
    for match in data["response"]:
        fixture_id = match.get("fixture", {}).get("id", "Bilinmir")
        teams = match.get("teams", {})
        home = teams.get("home", {}).get("name", "Evsahibi")
        away = teams.get("away", {}).get("name", "Qonaq")

        for bookmaker in match.get("bookmakers", []):
            if bookmaker["name"].lower() in ["bet365", "1xBet", "bwin"]:  # İstəyə görə dəyişdir
                for bet in bookmaker["bets"]:
                    if bet["name"] == "Match Winner":
                        for val in bet["values"]:
                            message_lines.append(
                                f"{home} vs {away} ({val['value']}) -> Əmsal: {val['odd']}"
                            )
else:
    message_lines.append("Uygun oyun və əmsal tapılmadı.")

# Telegrama göndəriş
final_message = "\n".join(message_lines)
send_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
send_data = {"chat_id": CHAT_ID, "text": final_message}

send_response = requests.post(send_url, data=send_data)
print("Telegram status:", send_response.status_code)
