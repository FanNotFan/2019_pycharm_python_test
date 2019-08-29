#!/usr/bin/env python
# encoding: utf-8
'''
@author: lennon
@license: (C) Copyright 2019-2020, Node Supply Chain Manager Corporation Limited.
@contact: v-lefan@expedia.com
@software: pycharm
@file: room_distance_compare.py
@time: 2019-08-20 16:05
@desc:
'''

import re
import numpy as np
import pandas as pd
from pandas import DataFrame
from scipy.ndimage import filters
import scipy.spatial.distance as dis
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import CountVectorizer


def gaussian_filter(X):
    filtered_data = filters.gaussian_filter(X, sigma=20)


def getDistance(abp_df, level):
    try:
        col_cfg = pd.DataFrame(
            np.array(
                [['RoomName', 'Dice', 1],
                 ['RoomType', 'Dice', 1],
                 ['RoomClass', 'Dice', 1],
                 ['RoomSize', 'cityblock', 0.5],
                 ['BedType', 'Dice', 1],
                 ['Wheelchair', 'Dice', 1],
                 ['Smoking', 'Dice', 1],
                 ['View', 'Dice', 1]
                 ]),
            columns=['name', 'algo', 'weight'])
        col_cfg = col_cfg.set_index('name')

        rows = abp_df.drop(['URL'], axis=1)

        rows['RoomSize'] = rows['RoomSize'].apply(lambda x: re.search("([0-9])+", str(x)).group(0))

        d_list = []

        for c in rows.columns:
            algo = col_cfg.loc[c]['algo']
            if algo == 'Dice':
                one_hot = MultiLabelBinarizer()
                d_list.append(pd.DataFrame(
                    dis.pdist(one_hot.fit_transform(rows[c].apply(lambda x: tuple(str(x).split(',')))), algo)))
            elif algo == 'cityblock':
                ud = dis.pdist(rows[c].values.reshape(-1, 1), algo).reshape(-1, 1)
                scaler = MinMaxScaler()
                scaler.fit(ud)
                d_list.append(pd.DataFrame(scaler.transform(ud)))
            elif algo == 'ngram':
                corpus = rows[c]
                v = CountVectorizer(ngram_range=(1, 3), binary=True, lowercase=True)
                d_list.append(pd.DataFrame(dis.pdist(v.fit_transform(corpus).toarray(), 'Dice')))
            else:
                print('error')

        dm = pd.concat(d_list, ignore_index=True, axis=1)
        dm.columns = rows.columns

        d_weight = col_cfg['weight'].values.astype(np.float)
        test = dm.values * d_weight
        ag1 = (dm.values * d_weight).mean(axis=1)
        ag1_sq = dis.squareform(ag1)
        gaussian_filter(ag1_sq)
        np.fill_diagonal(ag1_sq, 1)

        #     ag1_sq[ag1_sq==0] = 1
        distance_df = pd.DataFrame(ag1_sq)
        # print(distance_df)
        result = []
        for row_index, row in distance_df.iterrows():
            for col_index, distance in row.iteritems():
                if distance > level:
                    result.append(
                        [str(abp_df.loc[row_index].URL), str(abp_df.loc[col_index].URL), distance])
        return result
    except ValueError as e:
        print(e)
        raise Exception("Calculate failed!")


if __name__ == '__main__':
    SHEET_NAME_RESULT = 'Sheet1'
    EXCEL_PATH_RESULT = '../source/result_20190820.xlsx'

    SHEET_NAME_ONE = 'Source'
    EXCEL_PATH_ONE = '../source/RoomSource0815.xlsx'

    dataFrame_One = pd.read_excel(EXCEL_PATH_ONE, sheet_name=SHEET_NAME_ONE)
    dataFrame_Result = pd.read_excel(EXCEL_PATH_RESULT, sheet_name=SHEET_NAME_RESULT)

    dataFrame_One['RoomSize'].replace('', 0, inplace=True)
    dataFrame_One['RoomSize'].replace(np.nan, 0, inplace=True)
    dataFrame_Result['RoomSize'].replace('', 0, inplace=True)
    dataFrame_Result['RoomSize'].replace(np.nan, 0, inplace=True)
    dataFrame_Result.drop(['ExtraAttributes', 'NumberOfRoomType'], axis=1, inplace=True)

    distance_result_list = list()
    for index, row in dataFrame_One.iterrows():
        for indexr, rowr in dataFrame_Result.iterrows():
            if row['URL'].strip() == rowr['URL'].strip():
                df = pd.DataFrame(columns=['URL', 'RoomName', 'RoomType', 'RoomClass', 'RoomSize', 'BedType', 'Wheelchair', 'Smoking', 'View'])
                df.loc[0] = row
                df.loc[1] = rowr
                distance_result_list.extend(getDistance(df, 0))
                break
    df_distance_result = pd.DataFrame(np.array(distance_result_list), columns=['root', 'child', 'distance'])
    print(df_distance_result)
    pass