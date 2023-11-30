import os.path
import requests,re,json

gotNumber = 0
bilibiliSearchAPI = 'https://api.bilibili.com/x/space/wbi/arc/search?mid='
userID = ""
headers = {
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
		"referer":"https://www.bilibili.com/",
        "Cookie":""
}

# proxy = {
#     "http" : "127.0.0.1:7890",
#     "https" : "127.0.0.1:7890"
# }

# 1为首页 2为单个作品
def getQueryType(queryUrl):
    if "space" in queryUrl:
        return 1
    else:
        return 2

class VideoInfo:
    def __init__(self,name,bv):
        name = name.replace('“','')
        name = name.replace('”','')
        self.name = name
        self.bv = bv


    def __str__(self):
        return f"name: {self.name}  bv: {self.bv}"

def parseSpaceData():

    videoUrlDatas = []

    strData = requests.get(url=bilibiliSearchAPI + userID,headers=headers).text
    jsonData = json.loads(strData)
#    pprint.pprint(jsonData)
    videoList = jsonData['data']['list']['vlist']

    for videoData in videoList:
        videoInfoItem = VideoInfo(videoData['title'],videoData['bvid'])
        videoUrlDatas.append(videoInfoItem)

    return videoUrlDatas

def getBilibiliUrl(queryUrl, title):
    res = requests.get(url = queryUrl, headers=headers)

    play_info = re.findall('<script>window.__playinfo__=(.*?)</script>',res.text)[0]

    json_data = json.loads(play_info)

    audioUrl = json_data['data']['dash']['audio'][0]['baseUrl']
    videoUrl = json_data['data']['dash']['video'][0]['baseUrl']

    return audioUrl,videoUrl

def saveVideoContent(videoUrl,name):

    with open('video/' + name + '.mp4',mode = 'wb') as f:
        f.write(requests.get(url = videoUrl,headers=headers).content)


def saveAudioContent(audioUrl,name):
    with open('video/' + name + '.mp3',mode = 'wb') as f:
        f.write(requests.get(url = audioUrl,headers=headers).content)

def createBilibiliFolder():
    if not os.path.exists('video/'):
        os.mkdir('video/')

if __name__ == '__main__':
    url = input("请输入链接（主页链接）：")

    queryType = getQueryType(url)
    userID = url.split('/')[3]
    createBilibiliFolder()
    videoDataList = parseSpaceData()


    print(f"你xin大爹一共给你找到了{len(videoDataList)}个视频文件")
    for video in videoDataList:
        audioUrl, videoUrl = getBilibiliUrl(queryUrl='https://www.bilibili.com/video/' + video.bv,title=video.name)
        saveAudioContent(audioUrl,video.name)
        saveVideoContent(videoUrl,video.name)
        gotNumber = gotNumber + 1
        print(f"你xin大爹帮你下好了第{gotNumber}个视频")