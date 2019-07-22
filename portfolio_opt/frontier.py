from optimizer import Optimizer
import matplotlib.pyplot as plt
import pandas as pd


if __name__ == "__main__":
    df = pd.read_excel('../data/returns.xlsx', parse_dates=True, index_col="date", sheet_name='merged').sort_index(ascending=True)
    optimizer = Optimizer([df], on='date')
    optimizer.ef.portfolio_performance(verbose=True)
    optimizer.plot_efficient_frontier()
    optimizer.plot_random_portfolios(num_portfolios=10000)
    plt.show()
