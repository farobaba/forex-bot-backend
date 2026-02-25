import numpy as np
import logging
from datetime import datetime
from typing import Dict, List
import json

logger = logging.getLogger(__name__)


class SignalGenerator:
    """AI Signal Generator for trading signals"""
    
    def __init__(self, model_path: str = None):
        self.model_path = model_path
        self.confidence_threshold = 70
        
    def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate Relative Strength Index"""
        if len(prices) < period:
            return 50.0
        
        deltas = np.diff(prices[-period:])
        seed = deltas[:1]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        
        rs = up / down if down != 0 else 1.0
        rsi = 100.0 - (100.0 / (1.0 + rs))
        
        return float(rsi)
    
    def calculate_macd(self, prices: List[float]) -> Dict[str, float]:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        if len(prices) < 26:
            return {"macd": 0, "signal": 0, "histogram": 0}
        
        ema12 = self._ema(prices, 12)
        ema26 = self._ema(prices, 26)
        
        macd = ema12 - ema26
        signal = self._ema([macd], 9)
        histogram = macd - signal
        
        return {
            "macd": float(macd),
            "signal": float(signal),
            "histogram": float(histogram)
        }
    
    def calculate_moving_averages(self, prices: List[float]) -> Dict[str, float]:
        """Calculate Moving Averages"""
        sma20 = np.mean(prices[-20:]) if len(prices) >= 20 else np.mean(prices)
        sma50 = np.mean(prices[-50:]) if len(prices) >= 50 else np.mean(prices)
        ema12 = self._ema(prices, 12)
        
        return {
            "sma20": float(sma20),
            "sma50": float(sma50),
            "ema12": float(ema12)
        }
    
    def _ema(self, prices: List[float], period: int) -> float:
        """Calculate Exponential Moving Average"""
        prices_array = np.array(prices)
        ema = prices_array[-1]
        multiplier = 2 / (period + 1)
        
        for i in range(len(prices_array) - 2, -1, -1):
            ema = prices_array[i] * multiplier + ema * (1 - multiplier)
        
        return float(ema)
    
    def generate_signal(self, candle_data: List[Dict], current_price: float) -> Dict:
        """Generate trading signal based on technical analysis"""
        if len(candle_data) < 50:
            return {
                "signal_type": "HOLD",
                "confidence": 0,
                "indicators": {},
                "reason": "Insufficient data"
            }
        
        # Extract prices
        prices = [float(c["close"]) for c in candle_data]
        
        # Calculate indicators
        rsi = self.calculate_rsi(prices)
        macd = self.calculate_macd(prices)
        mas = self.calculate_moving_averages(prices)
        
        indicators = {
            "rsi": rsi,
            "macd": macd,
            "moving_averages": mas,
            "current_price": current_price
        }
        
        # Generate signal logic
        confidence = 50  # Base confidence
        signals = []
        
        # RSI signals
        if rsi < 30:
            signals.append(("BUY", 20))
            confidence += 10
        elif rsi > 70:
            signals.append(("SELL", 20))
            confidence += 10
        
        # MACD signals
        if macd["histogram"] > 0 and macd["macd"] > macd["signal"]:
            signals.append(("BUY", 15))
            confidence += 5
        elif macd["histogram"] < 0 and macd["macd"] < macd["signal"]:
            signals.append(("SELL", 15))
            confidence += 5
        
        # Moving Average signals
        if current_price > mas["sma20"] > mas["sma50"]:
            signals.append(("BUY", 10))
            confidence += 5
        elif current_price < mas["sma20"] < mas["sma50"]:
            signals.append(("SELL", 10))
            confidence += 5
        
        # Determine final signal
        buy_signals = sum(1 for s in signals if s[0] == "BUY")
        sell_signals = sum(1 for s in signals if s[0] == "SELL")
        
        if buy_signals > sell_signals:
            signal_type = "BUY"
        elif sell_signals > buy_signals:
            signal_type = "SELL"
        else:
            signal_type = "HOLD"
        
        # Cap confidence at 100
        confidence = min(confidence, 100)
        
        return {
            "signal_type": signal_type,
            "confidence": confidence,
            "indicators": indicators,
            "is_valid": confidence >= self.confidence_threshold
        }
    
    def calculate_position_size(self, account_balance: float, risk_percent: float,
                              entry_price: float, stop_loss_pips: float) -> float:
        """Calculate position size based on risk management"""
        risk_amount = account_balance * (risk_percent / 100)
        pip_value = 0.01  # For XAUUSD
        stop_loss_amount = stop_loss_pips * pip_value
        
        if stop_loss_amount == 0:
            return 0.01  # Minimum position
        
        position_size = risk_amount / stop_loss_amount
        return round(position_size, 2)
