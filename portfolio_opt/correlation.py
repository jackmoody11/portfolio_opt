import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == '__main__':
    df = pd.read_excel("../data/returns.xlsx", parse_dates=True,
                       index_col="date", sheet_name="merged").sort_index(ascending=True)
    df_pct = df.pct_change()
    ax = sns.heatmap(df_pct.dropna().corr(), annot=True)
    ax.set_title("Correlation Heat Map")
    ax.figure.tight_layout()
    plt.show()
