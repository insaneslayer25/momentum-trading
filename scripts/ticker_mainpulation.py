from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf

'''
Validate Tickers and create CSV file
'''


def ticker_validation(stock):
    '''
    Check Validity of Ticker in Yahoo finance by adding '.NS' at end of symbol.
    '.NS' represents National Stock Exchange of India
    '''
    ticker = stock + '.NS'
    try:
        checker = yf.Ticker(ticker)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        df = checker.history(start=start_date, end=end_date)

        if df.empty:
            print(f'{stock} does not valid symbol')
            return None
        else:
            return ticker

    except Exception as e:
        print(f"{stock} is facing data error")
        return None


def ticker_to_csv_converter(data, csv_file_name):
    '''
    Using ticker validation checks validity if valid adds Company Name, Ticker Symbol and NSE Symbol
    in dataframe and converts it to a CSV file
    '''
    rows = []

    for i in range(len(data)):
        stock = data['Symbol'].iloc[i]
        ticker = ticker_validation(stock)

        if ticker is not None:
            nse_symbol = 'NSE:' + stock
            row = {
                'Company Name': data['Company Name'].iloc[i],
                'Ticker': ticker,
                'NSE Symbol': nse_symbol
            }

            rows.append(row)

    df = pd.DataFrame(rows)
    # df.to_csv(csv_file_name, index=False)

    return df
