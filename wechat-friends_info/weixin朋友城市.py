# -*- coding: utf-8 -*-
import itchat
import pandas as pd


def get_info():
    itchat.login()
    friends = itchat.get_friends(update=True)
    df_friends = pd.DataFrame(friends)
    City = df_friends.City
    City_count = City.value_counts()
    # 有一些好友地理信息为空，过滤掉这一部分人。
    City_count = City_count[City_count.index != '']
    print(City_count)


if __name__ == '__main__':
    # 运行程序后，扫码登录即可
    get_info()
