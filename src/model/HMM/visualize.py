import os
import sys
import argparse
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
# os.chdir('..')
sys.path.append("./src/model/HMM")
from HMM import HMM
from data import train_test_split, get_dataset
# print(sys.path)
sys.path.remove("./src/model/HMM")
# print(sys.path)
# from .src.model.HMM.HMM import HMM
# from .src.model.HMM.data import train_test_split, get_dataset

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", help="relative path to the data file to be visualized")
    args = parser.parse_args()
    if args.file_path:
        exe_path = args.file_path
    else:
        exe_path = 'data/processed/exe.csv'

    # Get the path to the data file
    os.chdir('..')
    os.chdir('..')
    os.chdir('..')
    curr_dir = os.getcwd()
    path = os.path.join(curr_dir, exe_path)
    # print(curr_dir, path)

    # Load the data
    X, y = get_dataset(exe_path)
    X_train, y_train, X_test, y_test = train_test_split(X, y)
    model = HMM()
    model.fit(X_train, y_train)

    # Get the counts matrix from the model and sort it by the counts
    cts = model.get_counts_matrix()
    cts = sorted(cts.items(), key = lambda x: x[1], reverse = True)

    # Grab the data for the ten most frequent apps
    top_10 = cts[:11]
    top_10 = [cts[z] for z in range(11) if cts[z][0] != 'ApplicationFrameHost.exe']
    if len(top_10) > 10:
        del top_10[10]
    top_10_list = [x[0] for x in top_10]

    # Get the top 4 posterior probability of these ten apps
    t = model.get_transition_matrix()
    most_frequent_apps = dict()
    for exe in top_10_list:
        top_4_prob = []
        i = 0
        for p in t[exe].items():
            if i == 4:
                break
            top_4_prob.append(p)
            i += 1
        most_frequent_apps[exe] = dict(top_4_prob)

    # Plot the heatmap for the ten most frequent apps
    y_axis = list(set([y for x in most_frequent_apps.values() for y in x.keys()]))
    x_axis = most_frequent_apps.keys()
    df = pd.DataFrame(index = y_axis, data = most_frequent_apps)
    df = df.fillna(0)
    sns.set(rc={'figure.figsize':(11.7,8.27)})
    ax = sns.heatmap(df, cmap = 'Blues', annot=True, fmt='.2f')
    x_labels = ax.get_xticklabels()
    plt.setp(x_labels, rotation=45, horizontalalignment='right')
    plt.xlabel('Prior app')
    plt.ylabel('Next app')
    plt.tight_layout()
    plt.savefig('frequent_app_prob.png')

    # Repeat the process for the ten highest posterio probability
    for exe2, probs in t.items():
        t[exe2]['max_prob'] = max(probs.values())
    t_sorted = sorted(t.items(), key = lambda x: x[1]['max_prob'], reverse=True)
    x2_axis = [t_sorted[z][0] for z in range(10)]
    for app, prob in t_sorted:
        del prob['max_prob']
    most_frequent_apps2 = dict()
    for exe3 in x2_axis:
        top_4_prob = []
        i = 0
        for p in t[exe3].items():
            if i == 4:
                break
            top_4_prob.append(p)
            i += 1
        most_frequent_apps2[exe3] = dict(top_4_prob)
    y2_axis = list(set([y for x in most_frequent_apps2.values() for y in x.keys()]))

    df2 = pd.DataFrame(index = y2_axis, data = most_frequent_apps2)
    df2 = df2.fillna(0)
    sns.set(rc={'figure.figsize':(12,8)})
    ax2 = sns.heatmap(df2, cmap = 'Blues', annot=True, fmt='.2f')
    x2_labels = ax2.get_xticklabels()
    plt.setp(x2_labels, rotation=45, horizontalalignment='right')
    plt.xlabel('Prior app')
    plt.ylabel('Next app')
    plt.tight_layout()

    # Save the graphs in outputs
    plt.savefig('highest_prob.png')
    
    print('Done')