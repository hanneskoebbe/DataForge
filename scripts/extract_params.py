import pandas as pd

def extract_params(data):
    params = set()
    for df in data.values():
        try:
            for val in df.iloc[12:, 0]:  # Erste Spalte ab Zeile 12
                if pd.notna(val):
                    params.add(str(val))
        except Exception as e:
            print(f"Fehler beim Auslesen von Parametern: {e}")
    return sorted(params)
