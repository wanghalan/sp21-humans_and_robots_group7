import seaborn as sns
import pandas as pd
import os
from datetime import datetime
import pickle
import matplotlib.pyplot as plt


def pre_process():
    df = pd.DataFrame()
    data_dir = 'analysis_txt_edited/'
    for dir in os.listdir(data_dir):
        print(dir)
        comb_path = os.path.join(data_dir, dir)
        if os.path.isdir(comb_path):
            id = dir
            for file in os.listdir(comb_path):
                filepath = os.path.join(comb_path, file)
                trial = file.split('.')[0]
                if os.path.isfile(filepath):
                    with open(filepath, 'r') as f:
                        lines = f.readlines()
                    for line in lines[:-3]:
                        try:
                            l = line.strip()
                            time = datetime.strptime(
                                l.split(': ')[0], '%Y%m%d_%H%M%S')  # 20210502_115618
                            event = l.split(': ')[-1].strip()
                            df = df.append(
                                {'pid': id, 'trial': trial, 'time': time, 'event': event}, ignore_index=True)
                        except:
                            pass
            print('id: %s' % id)
    print('-' * 80)
    # print(df)
    return df


def process(df):
    df = df.sort_values(by='time')
    print(df)
    df['delta'] = (df['time'] - df['time'].shift()
                   ).fillna(pd.Timedelta(seconds=0))
    print(df)
    # pdf = df[df['pid'] == '1']
    # # sns.lineplot(x='time', y='delta', hue='trial', data=pdf)
    plt.show()
    return df


def main():
    pickle_file = 'data_set.pickle'

    if not os.path.isfile(pickle_file):
        df = pre_process()
        with open(pickle_file, 'wb') as f:
            pickle.dump(df, f)
    else:
        with open(pickle_file, 'rb') as f:
            df = pickle.load(f)
    print(df)
    df = process(df)



    return df


if __name__ == '__main__':
    df = main()
