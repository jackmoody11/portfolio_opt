import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from functools import reduce
from pypfopt import expected_returns, risk_models
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.cla import CLA


class Optimizer:
    def __init__(self, dfs, on='date', rf=0.02):
        df = reduce(lambda left,right: pd.merge(left,right,on=on), dfs)
        df_pct = df.pct_change()
        self.prices = df
        self.mu = expected_returns.mean_historical_return(df)
        self.rf = rf
        self.S = risk_models.sample_cov(df)
        self.ef = EfficientFrontier(self.mu, self.S)
        self.ef.max_sharpe(risk_free_rate=rf)

    def _get_efficient_weights(self):
        cla = CLA(self.mu, self.S)
        cla.max_sharpe()
        (mu, sigma, weights) = cla.efficient_frontier()
        return mu, sigma, weights

    def plot_efficient_frontier(self):
        mu, sigma, weights = self._get_efficient_weights()
        plt.plot(sigma, mu)
        plt.xlabel("Expected Volatility")
        plt.ylabel("Expected Return")
        plt.title("Markowitz Efficient Frontier Model")

    def plot_random_portfolios(self, num_portfolios=10000):
        num_assets = len(self.mu)
        port_returns, port_volatility, stock_weights = [], [], []
        sharpe_ratio = []
        for portfolio in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            port_return = np.dot(weights, self.mu)
            volatility = np.sqrt(
                np.dot(weights.T, np.dot(self.S, weights)))
            port_returns.append(port_return)
            port_volatility.append(volatility)
            stock_weights.append(weights)
            sharpe_ratio.append((port_return - self.rf) / volatility)
        plt.scatter(port_volatility, port_returns, alpha=0.5, c=sharpe_ratio)
        clb = plt.colorbar()
        clb.set_label('Sharpe Ratio', labelpad=0, y=1.05, rotation=0)
        return port_returns, port_volatility, stock_weights
