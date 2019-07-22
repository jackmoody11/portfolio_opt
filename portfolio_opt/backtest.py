import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from optimizer import Optimizer

plt.style.use('seaborn')


class Backtester:

    def __init__(self, prices, allocation, rebalance="m"):
        self.allocation = allocation
        self.prices = prices.dropna()
        self.prices.index = pd.to_datetime(
            self.prices.index, format="%m/%d/%y")
        self.prices = self.prices.sort_index(ascending=True)
        if rebalance == 'm':
            self.quarterly = False
            self._to_monthly()
        elif rebalance == 'q':
            self.quarterly = True
            self._to_quarterly()
        else:
            raise ValueError(
                "{0} is not a valid argument. The rebalance argument must be given either 'q' or 'm'.".format(rebalance))

    def _to_monthly(self):
        self.prices = self.prices.groupby(
            [self.prices.index.year, self.prices.index.month]).head(1).sort_index(ascending=True)

    def _to_quarterly(self):
        self.prices = self.prices.groupby(pd.Grouper(freq='Q')).head(
            1).sort_index(ascending=True)

    def calculate_return_history(self, start=100):
        """
        Args:
            start (int): Starting value of portfolio
            quarterly (bool): If portfolio should be rebalanced every quarter
            monthly (bool): If portfolio should be rebalanced every month
        """
        prices_pct_change = self.prices.pct_change()
        alloc = pd.DataFrame({
            asset: [self.allocation[asset]] * len(self.prices) for asset in self.allocation.keys()
        }, index=self.prices.index)
        alloc['return'] = np.sum(np.array(
            prices_pct_change[self.allocation.keys()].values * np.array(alloc.values)), axis=1)
        cumulative_return = (alloc['return'] + 1).cumprod()
        alloc['total'] = cumulative_return * start
        alloc['total'][0] = start
        self.return_history = alloc['total']

    def calculate_return_distribution(self, years):
        try:
            self.return_history
        except AttributeError:
            self.calculate_return_history()
        self.calculate_return_history()
        periods = years * 4 if self.quarterly else years * 12
        distribution = -1 * \
            self.return_history[::-1].diff(periods) / self.return_history
        return (distribution.dropna() + 1)**(1/years) - 1

    def plot_returns(self, label):
        self.calculate_return_history()
        self.return_history.plot(label=label)
        plt.xlabel("Time")
        plt.ylabel("Return")
        plt.title("Historical Performance with Rebalancing")

    def plot_return_distribution(self, years):
        distr = self.calculate_return_distribution(years)
        distr.hist()
        plt.xlabel("Annualized Return Rate")
        plt.ylabel("Count")
        plt.title("Distribution of Annualized Returns for {0} Year Period {1}-{2}".format(years,
                                                                                          distr.index[0].year, distr.index[-1].year))
        plt.axvline(distr.mean(), color='black', linestyle='dashed',
                    linewidth=1, label="Mean Return = {:.02%}".format(distr.mean()))
        plt.axvline(distr.median(), color='green', linestyle='solid',
                    linewidth=1, label="Median Return = {:.02%}".format(distr.median()))
        plt.legend()

if __name__ == "__main__":
    df = pd.read_excel('../data/returns.xlsx', parse_dates=True, index_col="date", sheet_name='merged').sort_index(ascending=True)
    optimizer = Optimizer([df], on='date')
    optimal_weights = optimizer.ef.efficient_return(0.09)
    optimizer.ef.portfolio_performance(verbose=True)
    bt = Backtester(optimizer.prices, allocation=optimal_weights, rebalance='m')
    bt.plot_returns(label="Allocation 1")
    plt.legend()
    plt.show()
