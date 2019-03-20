import requests

url = "https://www.lesaintsulpice.com/en/"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/xxxxxxxxx Safari/537.36'}

res = requests.get(url, headers=header)
content = res.content

# 假设content为已经拿到的html

# Ctext取周围k行(k<5),定为3
blocksWidth = 3
# 每一个Cblock的长度
Ctext_len = []
# Ctext
lines = content.split('n')
# 去空格
for i in range(len(lines)):
    if lines[i] == ' ' or lines[i] == 'n':
        lines[i] = ''
# 计算纵坐标，每一个Ctext的长度
for i in range(0, len(lines) - blocksWidth):
    wordsNum = 0
    for j in range(i, i + blocksWidth):
        lines[j] = lines[j].replace("\s", "")
        wordsNum += len(lines[j])
    Ctext_len.append(wordsNum)
# 开始标识
start = -1
# 结束标识
end = -1
# 是否开始标识
boolstart = False
# 是否结束标识
boolend = False
# 行块的长度阈值
max_text_len = 88
# 文章主内容
main_text = []
# 没有分割出Ctext
if len(Ctext_len) < 3:
    print('没有正文')
    exit(-1)
for i in range(len(Ctext_len) - 3):
    # 如果高于这个阈值
    if (Ctext_len[i] > max_text_len and (not boolstart)):
        # Cblock下面3个都不为0，认为是正文
        if (Ctext_len[i + 1] != 0 or Ctext_len[i + 2] != 0 or Ctext_len[i + 3] != 0):
            boolstart = True
            start = i
            continue
    if (boolstart):
        # Cblock下面3个中有0，则结束
        if (Ctext_len[i] == 0 or Ctext_len[i + 1] == 0):
            end = i
            boolend = True
    tmp = []

    # 判断下面还有没有正文
    if (boolend):
        for ii in range(start, end + 1):
            if (len(lines[ii]) < 5):
                continue
            tmp.append(lines[ii] + "n")
        str = "".join(list(tmp))
        # 去掉版权信息
        if ("Copyright" in str or "版权所有" in str):
            continue
        main_text.append(str)
        boolstart = boolend = False

# 返回主内容
result = "".join(list(main_text))
