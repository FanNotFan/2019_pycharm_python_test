import requests
import re
import urllib
import os

# 使用pypud 需要依赖库  ffmpeg
# from pydub import AudioSegment


class QQDownLoader(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
        }

        # 搜索需要下载的歌曲信息
        self.searchUrl = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.top&searchid=34725291680541638&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w={}&g_tk=5381&jsonpCallback=MusicJsonCallback703296236531272&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
        self.fcg_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&jsonpCallback=MusicJsonCallback9239412173137234&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&callback=MusicJsonCallback9239412173137234&uin=0&songmid={}&filename={}.m4a&guid=8208467632'
        self.downloader_url = 'http://dl.stream.qqmusic.qq.com/{}.m4a?vkey={}&guid=8208467632&uin=0&fromtag=66'

    def getSingInfo(self, name, num):
        print('正在获取歌曲信息。。。')
        # 查询的歌的名字
        singurl = self.searchUrl.format(name)
        singData = requests.get(singurl, headers=self.headers).text
        self.analysisData(singData, num)

    def analysisData(self, res, num):
        # media_mid
        media_mid_temp = re.findall('"media_mid":"(.*?)"', res)
        media_mid = []

        for i in range(len(media_mid_temp)):
            media_mid.append('C400' + media_mid_temp[i])

        # songmid
        songmid = re.findall('"lyric_hilight":".*?","mid":"(.*?)","mv"', res)

        # singer
        singer_temp = re.findall('"singer":\[.*?\]', res)
        singer = []

        for s in singer_temp:
            singer.append(re.findall('"name":"(.*?)"', s)[0])

        # songname
        songname = re.findall('},"name":"(.*?)","newStatus"', res)

        # print(media_mid)

        # print(songmid)

        # print(singer)

        # print(songname)
        self.getDownloaderUrl(media_mid, songmid, singer, songname, num)

    def getDownloaderUrl(self, media_mid, songmid, singer, songname, num):
        urls = []
        songname_keep = []
        singer_keep = []
        for m in range(len(media_mid)):
            try:
                fcg_res = requests.get(self.fcg_url.format(songmid[m], media_mid[m]), headers=self.headers)

                # print(fcg_res.text)
                vkey = re.findall('"vkey":"(.*?)"', fcg_res.text)[0]

                urls.append(self.downloader_url.format(media_mid[m], vkey))
                songname_keep.append(songname[m])
                singer_keep.append(singer[m])

            except:
                print('[Warning]:One song lost...')

            # time.sleep(0.5)

        # print(songname_keep)

        # print(singer_keep)
        self.downloadMp3(urls, songname_keep, singer_keep, num)

    def downloadMp3(self, urls, songname_keep, singer_keep, num=1):

        # print(urls)
        if num > len(urls):
            print('[Warning]:Only find %d songs...' % len(urls))
            num = len(urls)
        if not os.path.exists('./MP3'):
            os.mkdir('./MP3')

        for n in range(num):
            print('正在下载第 %d 第一首歌...' % (n + 1))
            filepath = './MP3/{}'.format(songname_keep[n] + '_' + singer_keep[n] + '.m4a')
            urllib.request.urlretrieve(urls[n], filepath)
            self.changeFormate(filepath)

        print('下载完成')

    def changeFormate(self, filepath):
        print('正在转码。。。')
        '''
            mp3与wav格式进行互转
        '''
        # song = AudioSegment.from_mp3(filepath)
        # song.export("now.wav", format="wav")
        # 讲m4a 转成 MP3
        os.system("ffmpeg -i " + filepath + " " + filepath[:filepath.rfind('.')] + ".mp3")
        os.remove(filepath)

    def run(self, name, num):
        self.getSingInfo(name, num)


if __name__ == '__main__':
    qq = QQDownLoader()
    qq.run('爱你', 2)
