import time
import yfinance as yf

class TradingProgram:
    def __init__(self, initial_investment, target_return, stop_loss):
        self.stocks = []
        self.initial_investment = initial_investment
        self.available_funds = initial_investment
        self.target_return = target_return
        self.stop_loss = stop_loss

    def add_stock(self, stock):
        self.stocks.append(stock)

    def start_trading(self):
        while True:
            for stock in self.stocks:
                current_price = stock.get_current_price()
                buy_price = current_price * 0.95  # 5% lower than current price
                sell_price = current_price * 1.05  # 5% higher than current price

                if current_price <= buy_price and self.available_funds > buy_price:
                    self.buy_stock(stock, buy_price)

                if current_price >= sell_price and stock.num_shares_owned > 0:
                    self.sell_stock(stock, sell_price)

                if self.available_funds <= self.initial_investment * (1 - self.stop_loss):
                    print("Stop loss triggered. Exiting trading program...")
                    return

                if self.available_funds >= self.initial_investment * (1 + self.target_return):
                    print("Target return achieved. Exiting trading program...")
                    return

            time.sleep(5)  # wait for 5 seconds before trading again

    def buy_stock(self, stock, price):
        num_shares = int(self.available_funds / price)
        stock.buy(num_shares)
        self.available_funds -= num_shares * price

    def sell_stock(self, stock, price):
        num_shares = stock.num_shares_owned
        stock.sell(num_shares)
        self.available_funds += num_shares * price

class Stock:
    def __init__(self, symbol, initial_price):
        self.symbol = symbol
        self.current_price = initial_price
        self.num_shares_owned = 0

    def get_current_price(self):
        # Implement logic to get current price of stock
        ticker = yf.Ticker(self.symbol)
        self.current_price = ticker.history(period="1d")['Close'][0]
        return self.current_price

    def buy(self, num_shares):
        self.num_shares_owned += num_shares

    def sell(self, num_shares):
        self.num_shares_owned -= num_shares

if __name__ == '__main__':
    trading_program = TradingProgram(10000.00, 0.05, 0.10)
    trading_program.add_stock(Stock("AAPL", 100.00))
    trading_program.add_stock(Stock("GOOG", 500.00))
    trading_program.start_trading()
