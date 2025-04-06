import json
import pandas as pd

def json_to_excel(json_file, excel_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract the list under the "things" key
    records = data.get("tokens", [])

    # Convert to DataFrame
    df = pd.DataFrame(records)

    # Export to Excel
    df.to_excel(excel_file, index=False)
    print(f"Successfully wrote '{excel_file}' with {len(df)} rows.")

json_to_excel('tokens.json', 'output.xlsx')