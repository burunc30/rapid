import requests
from datetime import datetime

# 🔐 RapidAPI açarın (sənin verdiyin açar artıq əlavə olunub)
API_KEY = "7fe03acd62mshe42ef629a8f7768p1d8621jsn57b3d87aa3dd"

# 📅 Bugünkü tarix
today = datetime.now().strftime("%Y-%m-%d")

# 📡 API ünvanı və parametrlər
url = "https://api-football-v1.p.rapidapi.com/v3/odds"
querystring = {"date": today}

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

# 🛰️ Sorğunu göndər
response = requests.get(url, headers=headers, params=querystring)

# ✅ Cavabı oxu
data = response.json()

# 📋 Nəticəni göstər
for match in data.get("response", []):
    teams = match.get("teams", {})
    home = teams.get("home", {}).get("name", "Unknown")
    away = teams.get("away", {}).get("name", "Unknown")
    league = match.get("league", {}).get("name", "Unknown")
    time = match.get("fixture", {}).get("date", "Time?")[:16]

    print(f"🏟️ {league}")
    print(f"🕒 {time}")
    print(f"⚽ {home} vs {away}")

    bookmakers = match.get("bookmakers", [])
    for bookmaker in bookmakers:
        if bookmaker["name"] == "Bet365":  # Seçdiyin bukmeker
            for bet in bookmaker["bets"]:
                if bet["name"] == "Match Winner":
                    print("🔢 1X2 əmsalları:")
                    for value in bet["values"]:
                        print(f"  {value['value']}: {value['odd']}")
                if bet["name"] == "Over/Under":
                    print("🔼 Over/Under 2.5:")
                    for value in bet["values"]:
                        if value["value"] in ["Over 2.5", "Under 2.5"]:
                            print(f"  {value['value']}: {value['odd']}")
    print("-" * 40)
