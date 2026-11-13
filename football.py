
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://v3.football.api-sports.io/fixtures"


def fetch_past_matches(league_id, season):

    if not API_KEY:
        print("API key not found. Check your .env file.")
        return

    headers = {
        "x-apisports-key": API_KEY
    }

    params = {
        "league": league_id,
        "season": season,
        "from": f"{season}-01-01",
        "to": f"{season}-12-31"
    }

    try:
        response = requests.get(
            BASE_URL,
            headers=headers,
            params=params,
            timeout=15
        )

        response.raise_for_status()
        data = response.json()

        if data.get("errors"):
            print("API Error:", data["errors"])
            return

        matches = data.get("response", [])

        if not matches:
            print("No matches found.")
            return

        print(f"\nFOOTBALL MATCHES - SEASON {season}\n")

        for match in matches:

            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]

            date = match["fixture"]["date"]

            home_score = match["score"]["fulltime"]["home"]
            away_score = match["score"]["fulltime"]["away"]

            status = match["fixture"]["status"]["long"]

            print(f"Match: {home} vs {away}")
            print(f"Date: {date}")
            print(f"Score: {home_score} - {away_score}")
            print(f"Status: {status}")
            print("-" * 40)

        print(f"\nTotal matches found: {len(matches)}")

    except requests.exceptions.Timeout:
        print("Request timed out. Please try again.")

    except requests.exceptions.ConnectionError:
        print("Network error. Check your internet connection.")

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)

    except (ValueError, KeyError, TypeError):
        print("Unable to process API response.")


# Main program
print("===== FOOTBALL MATCH TRACKER =====")

league_id = input("Enter league ID: ").strip()
season = input("Choose season (2022, 2023, 2024): ").strip()

if not league_id.isdigit():
    print("Invalid league ID.")

elif season not in ["2022", "2023", "2024"]:
    print("Please select a valid season.")

else:
    fetch_past_matches(int(league_id), int(season))
