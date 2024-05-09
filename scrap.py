import os
from datetime import datetime
import pandas as pd

BASE_URL = "https://www.zse.co.zw/price-sheet/"


def fetch_data_from_url(url):
    try:
        response = pd.read_html(url, skiprows=1)
        dataframe = response[0][3:]

        dataframe.columns = [
            " ",
            "Name",
            "Opening_Price",
            "Closing_Price",
            "Volume_Traded",
        ]
        # print(dataframe)

        df_trades = dataframe[["Name", "Opening_Price", "Closing_Price", "Volume_Traded"]].copy()
        # print(df_trades)

        df_trades.dropna(inplace=True)
        return df_trades.set_index("Name")
    except Exception as e:
        print("Error fetching data:", e)
        return None


def current_date():
    now = datetime.now()
    return now.strftime("%m-%d-%Y")


def check_or_create_directory(dataframe, current_date):
    try:
        os.makedirs("daily-price-sheets/csv", exist_ok=True)
        os.makedirs("daily-price-sheets/excel", exist_ok=True)
        csv_path = os.path.join("daily-price-sheets/csv", f"{current_date}.csv")
        excel_path = os.path.join("daily-price-sheets/excel", f"{current_date}.xlsx")
        dataframe.to_csv(csv_path)
        dataframe.to_excel(excel_path)
        print("Files saved successfully.")
    except Exception as e:
        print("Error saving files:", e)


def main():
    dataframe = fetch_data_from_url(BASE_URL)
    if dataframe is not None:
        date = current_date()
        check_or_create_directory(dataframe, date)


if __name__ == "__main__":
    main()
