import pandas as pd

# pandas 读取csv 文件
rows = pd.read_csv('cpa.csv', sep=',', engine='python', header=0)