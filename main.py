import requests

url = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"

querystring = {
    "market": "classic",
    "federation": "UEFA",
    "iso_date": "2025-05-24"
}

headers = {
    "X-RapidAPI-Key": "2f07e2d462mshb74dbb0d87354aep18f68ajsn92ddc36803b3",
    "X-RapidAPI-Host": "football-prediction-api.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

if response.status_code == 200:
    data = response.json()
    predictions = data.get("data", [])
    
    filtered_matches = []
    for match in predictions:
        home_team = match['home_team']
        away_team = match['away_team']
        odds = match.get('odds', {})

        home_odds = odds.get('home_win')
        if home_odds and float(home_odds) > 2.0:
            filtered_matches.append(f"{home_team} vs {away_team} — Home odds: {home_odds}")

    if filtered_matches:
        print("Filtrə uyğun oyunlar:")
        for m in filtered_matches:
            print(m)
    else:
        print("Filtrə uyğun oyun tapılmadı.")
else:
    print("Xəta baş verdi:", response.status_code, response.text)
