from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Tickers of interest
        self.tickers = ["AAPL"]
        self.sma14  # Length for SMA calculation
        self.rsi_length = 14  # Length for RSI calculation
        self.oversold_threshold = 30  # RSI threshold for oversold condition.overbought_threshold = 70  # RSI threshold for overbought condition

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        # Define the interval for the strategy. Adjust as per strategy requirement.
        return "1day"

    def run(self, data):
        # Initialize the allocation at 0 for the strategy start. Adjust according to the strategy logic.
        allocation = 0.0

        # Get the latest data for calculation
        ohlcv_data = data["ohlcv"]
        current_price = ohlcv_data["-L"]["close"]
        sma_values = SMA("AAPL", ohlcv_data, self.sma_length)
        rsi_values = RSI("AAPL", ohlcv_data, self.rsi_length)

        # Make sure we have enough data points for both SMA and RSI
        if sma_values is not None and rsi_values is not None and len(sma_values) > 0 and len(rsi_values) > 0:
            latest_sma = sma_values[-1]
            latest_rsi = rsi_values[-1]

            # Strategy logic: Enter or increase position if RSI is below oversold_threshold and price is above SMA
            if latest_rsi < self.oversold_threshold and current_price > latest_sma:
                allocation = 1.0  #
            # Exit or decreaseSI is above overbought_threshold
            elif latest_rsi > self_threshold:
                allocation = 0.0  # No allocation

        # Log for monitoring
        log(f"AAPL Strategy Allocation: {allocation}")
        # Return the allocation decision
        return TargetAllocation({"AAPL": allocation})