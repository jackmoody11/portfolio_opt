from optimizer import Optimizer
import matplotlib.pyplot as plt


if __name__ == "__main__":
    optimizer = Optimizer("../data/returns.xlsx", "merged")
    optimizer.plot_cov()
    plt.show()
