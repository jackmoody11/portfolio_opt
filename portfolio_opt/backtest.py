from pypfopt.cla import CLA
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from optimizer import Optimizer


if __name__ == "__main__":
    target_return = 0.08
    opt = Optimizer("../data/returns.xlsx", "merged")
    port_weight = opt.ef.efficient_return(target_return=target_return)
    print(port_weight)
