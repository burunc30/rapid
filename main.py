import requests
import time

# RapidAPI məlumatları
RAPIDAPI_KEY = "2f07e2d462mshb74dbb0d87354aep18f68ajsn92ddc36803b3"
RAPIDAPI_HOST = "odds.p.rapidapi.com"

# Telegram məlumatları
TELEGRAM_BOT_TOKEN = "8106341353:AAFIi3nfPOlydtCM_eYHiSIbDR0C1RFoaG4"
CHAT_ID = "1488455191"

# RapidAPI'den məlumat al
def get_odds_data():
    url = "https://odds.p.rapidapi.com/v4/sports/soccer_epl/odds"

    querystring = {
        "regions": "eu",          # Avropa bukmekerləri
        "oddsFormat": "decimal",
        "markets": "h2h",
        "dateFormat": "iso"
    }

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()
    else:
        print("RapidAPI xətası:", response.status_code, response.text)
        return []

# Filtrlər
def filter_matches(data):
    filtered = []
    for match in data:
        try:
            teams = match['teams']
            home_team = match['home_team']
            bookmakers = match['bookmakers']

            for bm in bookmakers:
                for market in bm['markets']:
                    if market['key'] == 'h2h':
                        outcomes = market['outcomes']
                        odds_dict = {o['name']: o['price'] for o in outcomes}

                        home_odds = odds_dict.get(home_team)
                        away_team = [t for t in teams if t != home_team][0]
                        away_odds = odds_dict.get(away_team)
                        draw_odds = odds_dict.get("Draw")

                        # 4 sadə filtr
                        if (
                            home_odds and away_odds and draw_odds and
                            1.8 < home_odds < 2.4 and
                            away_odds > 3.0 and
                            draw_odds > 3.2 and
                            abs(home_odds - away_odds) > 1.0
                        ):
                            filtered.append({
                                "home": home_team,
                                "away": away_team,
                                "home_odds": home_odds,
                                "away_odds": away_odds,
                                "draw_odds": draw_odds,
                                "start_time": match.get("commence_time", "N/A")
                            })
        except Exception as e:
            print("Xəta:", e)
            continue
    return filtered

# Telegrama göndər
def send_to_telegram(matches):
    if not matches:
        message = "Uyğun oyun tapılmadı."
    else:
        message = "Filtrə uyğun oyunlar:\n\n"
        for m in matches:
            message += (
                f"{m['home']} vs {m['away']}\n"
                f"Başlama: {m['start_time']}\n"
                f"Home: {m['home_odds']} | Draw: {m['draw_odds']} | Away: {m['away_odds']}\n\n"
            )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

# Əsas axın
def main():
    data = get_odds_data()
    matches = filter_matches(data)
    send_to_telegram(matches)

if __name__ == "__main__":
    main()
