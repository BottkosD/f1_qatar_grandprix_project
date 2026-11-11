#############
# Test 1:
#############

#import os
#import fastf1
#from pathlib import Path
#
#
#USERNAME = 'david.bottkos@gmail.com'
#PASSWORD = 'Almasajt-0721+'
#
#os.environ["F1_USERNAME"] = USERNAME
#os.environ["F1_PASSWORD"] = PASSWORD
#
#fastf1.Cache.enable_cache('data/cache')
#session = fastf1.get_session(2023, 'Qatar', "R")
#session.load(telemetry=False, weather=False)
#
#
#check_path = r'data/cache'
#
#dir = os.listdir(check_path)
#if len(dir) > 0:
#    print("Van cache")
#
#
#
#laps = session.laps
#
#ver_laps = laps.pick_driver("VER")
#data_example = ["LapNumber", "LapTime", "Compound", "Stint", "TyreLife", "TrackStatus", "PitOutTime", "PitInTime"]
#print(ver_laps[data_example].head(20).to_string())


##############
## Test 2:
##############
#
#import pandas as pd
#from data_management.data import load_f1_data
#from data_management.data_cleaner import cleaned_laps_data
#from data_management.pace_data import calculate_pace
#
#
#def run_test():
#    print(">>> 1. Adatok betöltése folyamatban (load_f1_data)...")
#    # Feltételezzük, hogy a load_f1_data visszaadja a nyers adatokat és a JSON konfigurációt
#    laps, observed_data = load_f1_data()
#
#    print("\n>>> 2. Adatok tisztítása (cleaned_laps_data)...")
#    cleaned_df = cleaned_laps_data(laps, observed_data)
#
#    print("\n>>> 3. Tempó statisztikák számítása (calculate_pace)...")
#    # Szimuláljuk a JSON-ből beolvasott pilótákat
#    picked_drivers = ["VER", "NOR", "PIA"]
#
#    # Mivel te tettél a calculate_pace függvénybe # test: print() sorokat,
#    # ezek automatikusan ki fognak íródni a konzolra futás közben.
#    laps_df, stats_with_compound = calculate_pace(cleaned_df, picked_drivers)
#
#    print("\n" + "=" * 50)
#    print(" TESZT SIKERESEN LEFUTOTT ")
#    print("=" * 50)
#
#    print("\nA visszaadott statisztikai tábla (stats_with_compound) végeredménye:")
#    # A to_string(index=False) eltünteti a bal szélső, felesleges sorszámozást
#    print(stats_with_compound.to_string(index=False))
#
#    print("\nA visszaadott körönkénti adatok (laps_df) első 10 sora a grafikonokhoz:")
#    # Csak a legfontosabb oszlopokat mutatjuk, hogy kiférjen a képernyőre
#    cols_to_print = ['Driver', 'LapNumber', 'Compound', 'LapTime_in_sec', 'Field_Lap_Median', 'Tdelta_to_Field']
#    print(laps_df[cols_to_print].head(10).to_string(index=False))
#
#
#if __name__ == "__main__":
#    run_test()


import pandas as pd
from data_management.data import load_f1_data
from data_management.data_cleaner import cleaned_laps_data
from data_management.tdegradation_data import calculate_degradation


def run_degradation_test():
    print(">>> 1. Adatok betöltése folyamatban (load_f1_data)...")
    # A te data.py-od a laps dataframe-et és az oszlopok LISTÁJÁT adja vissza
    laps, observed_cols = load_f1_data()

    print("\n>>> 2. Adatok tisztítása (cleaned_laps_data)...")
    # Itt most közvetlenül a listát adjuk át
    cleaned_df = cleaned_laps_data(laps, observed_cols)

    print("\n>>> 3. Gumikopás számítása (calculate_degradation)...")
    # Mivel a te data.py fájlod (jogosan, hogy ne bonyolítsuk) nem olvassa ki
    # és adja vissza a pilótákat a JSON-ből, a teszthez itt megadjuk őket:
    picked_drivers = ["VER", "PIA", "NOR"]

    plot_data, stats_data = calculate_degradation(cleaned_df, picked_drivers)

    print("\n" + "=" * 50)
    print(" TESZT SIKERESEN LEFUTOTT ")
    print("=" * 50)

    print("\n--- STATISZTIKAI ADATOK (stats_data) ---")
    print("Ezt használjuk a kopás mértékének elemzésére (meredekség):")
    if not stats_data.empty:
        display_stats = stats_data.copy()
        display_stats['Slope_steepness'] = display_stats['Slope_steepness'].round(4)
        print(display_stats.to_string(index=False))
    else:
        print("Nincs elég adat a statisztika kiszámításához.")

    print("\n--- VIZUALIZÁCIÓS ADATOK (plot_data) ---")
    print("Az első 15 sor a tiszta (outlier-mentes) adatokból a grafikonhoz:")
    if not plot_data.empty:
        cols_to_print = ['Driver', 'Compound', 'Stint', 'TyreLife', 'LapTime_in_sec']
        print(plot_data[cols_to_print].head(15).to_string(index=False))
    else:
        print("Nincs elég megtisztított adat a vizualizációhoz.")


if __name__ == "__main__":
    run_degradation_test()