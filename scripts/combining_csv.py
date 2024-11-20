import pandas as pd


def combining_csv(*args, csv_file_name: str, columns: list):
    combined_data = []
    for i in args:
        for index, row in i.iterrows():
            combined_data.append(row.tolist())

    combined_df = pd.DataFrame(combined_data, columns=columns)

    combined_df.drop_duplicates(subset=['Ticker'], inplace=True)
    combined_df.reset_index(drop=True, inplace=True)
    combined_df.to_csv(csv_file_name, index=False)
