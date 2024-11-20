import yfinance as yf
from datetime import datetime


def calculate_absolute_momentum(ticker, start_date=None, end_date=None, period=None):

    if (start_date is None or end_date is None) and period is None:
        print('Provide either period or both start date and end date')
        return None

    try:
        if period:
            stock = yf.Ticker(ticker).history(period=period)
        else:
            stock = yf.Ticker(ticker).history(start=start_date, end=end_date)

        if not stock.empty:
            start_price = stock['Close'].iloc[0]
            last_price = stock['Close'].iloc[-1]
            absolute_momentum_score = last_price/start_price
            print(f'{ticker} has absolute momentum score of {
                  absolute_momentum_score}')
            return round(float(absolute_momentum_score), 4)
        else:
            print(f'{ticker} does not have enough data')
            return None

    except Exception as e:
        print(f"Error calculating absolute momentum: {str(e)}")
        return None


def calculate_relative_momentum(ticker, market_cap, start_date=None, end_date=None, period=None):
    if (start_date is None or end_date is None) and period is None:
        print('Provide either period or both start date and end date')
        return None

    market_cap_ticker = {
        'Large Cap': '^NSEI',
        'Mid Cap': 'NIFTYMIDCAP150.NS',
        'Small Cap': 'NIFTYSMLCAP250.NS',
        'Micro Cap': 'NIFTY_MICROCAP250.NS'
    }

    if market_cap not in market_cap_ticker:
        print("Invalid market cap category. Choose from: 'Large Cap', 'Mid Cap', 'Small Cap', 'Micro Cap'.")
        return None

    try:
        index_ticker = market_cap_ticker[market_cap]

        if period:
            stock_data = yf.Ticker(ticker).history(period=period)
            index_data = yf.Ticker(index_ticker).history(period=period)
        else:
            stock_data = yf.Ticker(ticker).history(
                start=start_date, end=end_date)
            index_data = yf.Ticker(index_ticker).history(
                start=start_date, end=end_date)

        if stock_data.empty or index_data.empty:
            print(f"Data is not available for {ticker} or {
                  index_ticker} in the given period.")
            return None

        stock_start_price = stock_data['Close'].iloc[0]
        stock_end_price = stock_data['Close'].iloc[-1]
        stock_return = ((stock_end_price - stock_start_price) /
                        stock_start_price) * 100

        index_start_price = index_data['Close'].iloc[0]
        index_end_price = index_data['Close'].iloc[-1]
        index_return = ((index_end_price - index_start_price) /
                        index_start_price) * 100

        if index_return == 0:
            print("Warning: Index return is zero, cannot calculate relative momentum")
            return None

        relative_momentum = stock_return/index_return
        print(f'{ticker} has relative momentum score of {relative_momentum}')
        return round(float(relative_momentum), 4)

    except Exception as e:
        print(f"Error calculating relative momentum: {str(e)}")
        return None


def calculate_dual_momentum(ticker, market_cap, start_date=None, end_date=None, period=None,
                            absolute_momentum_weightage=50, relative_momentum_weightage=50):
    if absolute_momentum_weightage + relative_momentum_weightage != 100:
        print(f"Error: The weightages must sum to 100. Given: {
              absolute_momentum_weightage + relative_momentum_weightage}")
        return None

    try:
        relative_momentum = calculate_relative_momentum(
            ticker, market_cap, start_date, end_date, period)
        absolute_momentum = calculate_absolute_momentum(
            ticker, start_date, end_date, period)

        if relative_momentum is None or absolute_momentum is None:
            return None

        dual_momentum = (absolute_momentum * absolute_momentum_weightage) / 100 + \
            (relative_momentum * relative_momentum_weightage) / 100

        print(f'{ticker} has a dual momentum score of {dual_momentum}')
        return round(dual_momentum, 4)

    except Exception as e:
        print(f"Error calculating dual momentum: {str(e)}")
        return None
