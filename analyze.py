import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import glob

def get_csv_files(extension):
    snake_dfs = []
    random_dfs = []
    for file_path in glob.glob(os.path.join("save/", f'*{extension}*snake*.csv')):
        if os.path.isfile(file_path):
            df = pd.read_csv(file_path)
            snake_dfs.append(df.iloc[:, 1:])
    for file_path in glob.glob(os.path.join("save/", f'*{extension}*random*.csv')):
        if os.path.isfile(file_path):
            df = pd.read_csv(file_path)
            random_dfs.append(df.iloc[:, 1:])
    return snake_dfs, random_dfs

def ab_boxplot():
    # Get CSV dataframes
    snake_dfs, random_dfs = get_csv_files('epochMetrics')

    snake_final_fitness = []
    random_final_fitness = []
    
    for df in snake_dfs:
        for col in df.columns:
            snake_final_fitness.append(-df[col].iloc[-1])
    for df in random_dfs:
        for col in df.columns:
            random_final_fitness.append(-df[col].iloc[-1])
    
    # Create a figure and plot box plots for the final values of each column from the two arrays
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.boxplot(snake_final_fitness,
               positions=[0],
               labels=["snake start"],
               widths=0.4,
               boxprops=dict(color='blue'),
               whiskerprops=dict(color='blue'), 
               capprops=dict(color='blue'),
               medianprops=dict(color='blue'), 
               meanprops=dict(color='blue'), 
               flierprops=dict(marker='o', markersize=5))
    ax.boxplot(random_final_fitness,
               positions=[1],
               labels=["random start"],
               widths=0.4,
               boxprops=dict(color='green'),
                whiskerprops=dict(color='green'), 
                capprops=dict(color='green'),
                medianprops=dict(color='green'), 
                meanprops=dict(color='green'), 
                flierprops=dict(marker='o', markersize=5))
    ax.set_title('Distrubution of Final Fitness for Different Starting Morphologies')
    ax.set_xlabel('Starting Morphology')
    ax.set_ylabel('Final Fitness (avg. x position)')


    # Display the plot
    plt.show()    
    
def ab_linechart():
    # Get CSV dataframes
    snake_dfs, random_dfs = get_csv_files('epochMetrics')

    # Plot the blue lines
    plt.plot([0], [0], color='blue', label='snake start')
    plt.plot([0], [0], color='green', label='random start')
    for df in snake_dfs:
        for col in df.columns:
            plt.plot(df.index, -df[col], color='blue')

    # Plot the green lines
    for df in random_dfs:
        for col in df.columns:
            plt.plot(df.index, -df[col], color='green')

    # Customize the plot
    plt.title('Fitness over Time - Snake vs. Random Start')
    plt.xlabel('Generation')
    plt.ylabel('Fitness (Avg x position)')
    plt.legend()

    # Show the plot
    plt.show()

def scatter_plot(x_metric, y_metric):
    # Get CSV dataframes
    snake_dfs, random_dfs = get_csv_files('bodySizeMetrics')

    snake_data = pd.concat(snake_dfs)
    random_data = pd.concat(random_dfs)
    data = pd.concat([snake_data, random_data])
    
    # Extract the initial size and final fitness columns from the dataframes
    x1 = data[x_metric.lower()]
    y1 = data[y_metric.lower()] * -1
    x_ticks = np.array(range(max(x1)))
    m1, b1 = np.polyfit(x1, y1, 1)
    
    # Create the scatter plot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x1, y1, c="black")
    ax.plot(x_ticks, m1 * x_ticks + b1, c='red')

    
    # Set the axis labels and title
    ax.set_xlabel(x_metric)
    ax.set_ylabel(y_metric)
    ax.set_title(f'{x_metric} x {y_metric}')
    
    # Show the plot
    plt.show()

def stats_table():
    # Get CSV dataframes
    snake_dfs, random_dfs = get_csv_files('epochMetrics')
    snake_final_fitness = []
    random_final_fitness = []
    arrays = [snake_final_fitness, random_final_fitness]
        
    for df in snake_dfs:
        for col in df.columns:
            snake_final_fitness.append(-df[col].iloc[-1])
    for df in random_dfs:
        for col in df.columns:
            random_final_fitness.append(-df[col].iloc[-1])

    # Initialize lists to store the statistics for each array
    names = ["Snake Start", "Random Start"]
    means = []
    stds = []
    medians = []
    
    # Calculate the mean, standard deviation, and median for each array
    for array in arrays:
        means.append(np.mean(array))
        stds.append(np.std(array))
        medians.append(np.median(array))
    
    # Combine the statistics into a table
    table = '| Morphology | Mean | Median | Std Dev |\n| --- | --- | --- | --- |\n'
    for i in range(len(arrays)):
        table += f'| {names[i]} | {means[i]:.5f} | {medians[i]:.5f} | {stds[i]:.5f} |\n'
    
    # Print the table
    print(table)

stats_table()