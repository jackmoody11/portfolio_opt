from optimizer import Optimizer
import matplotlib.pyplot as plt


if __name__ == "__main__":
    optimizer = Optimizer("../data/returns.xlsx", "merged")
    optimizer.ef.portfolio_performance(verbose=True)
    optimizer.plot_efficient_frontier()
    optimizer.plot_random_portfolios()
    plt.show()
