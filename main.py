import requests
import json

# Sənin RapidAPI açarın
API_KEY = "2f07e2d462mshb74dbb0d87354aep18f68ajsn92ddc36803b3"

# API endpoint – 25 may 2024 üçün nümunə olaraq İngiltərə Premier League (league id 39)
url = "https://api-football-v1.p.rapidapi.com/v3/odds"

querystring = {
    "date": "2024-05-25",
    "league": "39",
    "season": "2023"
}

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

# Formatlı çap – test məqsədilə
print(json.dumps(data, indent=2))

# Əmsallar varsa göstər
if data["response"]:
    print("\n--- Əmsallar ---\n")
    for match in data["response"]:
        fixture = match.get("fixture", {}).get("id", "Bilinmir")
        print(f"Fixture ID: {fixture}")
        bookmakers = match.get("bookmakers", [])
        for bookmaker in bookmakers:
            print(f"Bookmaker: {bookmaker['name']}")
            for bet in bookmaker["bets"]:
                print(f"  Market: {bet['name']}")
                for val in bet["values"]:
                    print(f"    {val['value']} -> {val['odd']}")
else:
    print("Uygun matç və ya əmsal tapılmadı.")
