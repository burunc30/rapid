import requests
import json
import time

# RAPIDAPI MƏLUMATLARI
RAPID_API_KEY = "2f07e2d462mshb74dbb0d87354aep18f68ajsn92ddc36803b3"
RAPID_API_HOST = "odds.p.rapidapi.com"

# TELEGRAM MƏLUMATLARI
BOT_TOKEN = "8106341353:AAFIi3nfPOlydtCM_eYHiSIbDR0C1RFoaG4"
CHAT_ID = "1488455191"

# TELEGRAMA MESAJ GÖNDƏRƏN FUNKSIYA
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message[:4000]  # Telegram limiti
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Telegrama göndərilə bilmədi:", e)

# RAPID API-DƏN ƏMSAL MƏLUMATLARINI AL
def fetch_odds_from_rapidapi():
    url = "https://odds.p.rapidapi.com/v4/sports/soccer_epl/odds"

    querystring = {
        "regions": "eu",      # Avropa əmsalları
        "markets": "h2h",     # 1X2 bazarı (home/draw/away)
        "oddsFormat": "decimal",
        "dateFormat": "iso"
    }

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": RAPID_API_HOST
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        if not data:
            send_to_telegram("RapidAPI: Heç bir data gəlmədi.")
        else:
            # JSON formatında Telegrama göndər
            formatted = json.dumps(data, indent=2)[:4000]
            send_to_telegram("📊 RapidAPI Cavabı:\n\n" + formatted)
    except Exception as e:
        send_to_telegram(f"RapidAPI xəta verdi: {e}")

# İCRA
if __name__ == "__main__":
    fetch_odds_from_rapidapi()
