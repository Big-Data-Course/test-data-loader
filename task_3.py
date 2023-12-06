import pandas as pd
from matplotlib import pyplot as plt
import os

def process_data(inputDir, outputDir):
    parts = []
    for filename in os.listdir(inputDir):
        fin = os.path.join(inputDir, filename)
        parts.append(pd.read_csv(fin, sep=" "))
    df = pd.concat(parts, ignore_index=True)
    parts.clear()
    plt.hist(df["dist"], bins=100)
    plt.title("Distribution of distance")
    plt.xlabel("Distance[pc]")
    plt.ylabel("Count")
    plt.yscale("log")
    plt.grid(True)
    plt.savefig(os.path.join(outputDir, "distribution_of_distance_log_scale.png"))
    plt.figure()
    plt.hist(df["dist"], bins=100)
    plt.title("Distribution of distance")
    plt.xlabel("Distance[pc]")
    plt.ylabel("Count")
    plt.grid(True)
    plt.savefig(os.path.join(outputDir, "distribution_of_distance.png"))
        
if __name__ == "__main__":
    if not os.path.exists("task_3_result"):
        os.makedirs("task_3_result")
    process_data("task_3_data", "task_3_result")