from pathlib import Path
import pandas as pd
import requests
import fastf1

# Állítsd át arra a szezonra és futamra, amit elemzel
YEAR = 2022
EVENT = "Mexico"
SESSION_TYPE = "R"

OUTPUT_DIR = Path("pictures/drivers")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Csak a session.results részt töltjük be, így gyorsan lefut
session = fastf1.get_session(YEAR, EVENT, SESSION_TYPE)
session.load(laps=False, telemetry=False, weather=False, messages=False)

headers = {"User-Agent": "Mozilla/5.0"}

for _, row in session.results.iterrows():
    abbr = row.get("Abbreviation")
    url = row.get("HeadshotUrl")

    if pd.isna(abbr) or pd.isna(url) or not str(url).strip():
        print(f"Kihagyva (hiányzó URL): {abbr}")
        continue

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            file_path = OUTPUT_DIR / f"{abbr}.png"
            file_path.write_bytes(response.content)
            print(f"Mentve: {file_path}")
        else:
            print(f"Sikertelen ({response.status_code}): {abbr} -> {url}")
    except requests.RequestException as e:
        print(f"Hiba ({abbr}): {e}")