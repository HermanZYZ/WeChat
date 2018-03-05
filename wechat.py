import itchat, time
import datetime as dt
from apscheduler.schedulers.background import BackgroundScheduler
import random
from itchat.content import *

'''自动回复'''
@itchat.msg_register([TEXT, PICTURE, MAP, CARD, NOTE, SHARING, RECORDING, ATTACHMENT, VIDEO])
def text_reply(msg):
    print(msg['Text'])
    if msg['Text'] == '在干嘛' or msg['Text'] == '你在干嘛呢' or msg['Text'] == '你在干嘛':
        itchat.send('在想你呢', toUserName=msg['FromUserName'])
    if msg['Text'] == '今天有点不舒服':
        itchat.send('多喝热水，早点休息，注意身体', toUserName=msg['FromUserName'])

'''定时问候'''
greetList = ['很晚了，快去睡觉，你熬夜我会心疼的','今天忙了一天，忙着想你一天','多喝热水','想你了求自拍']
def tick():
    users = itchat.search_friends(name=u'Eternal') # 女朋友昵称名字
    userName = users[0]['UserName']
    itchat.send(u'%s，晚安'%(random.sample(greetList,1)[0]),toUserName=userName) # 发送问候语给女朋友
    nextTickTime = now + dt.timedelta(days=1)
    nextTickTime = nextTickTime.strftime("%Y-%m-%d 00:00:00")
    my_scheduler(nextTickTime)

def my_scheduler(runTime):
    scheduler = BackgroundScheduler() # 请求生成任务对象
    scheduler.add_job(tick, 'date', run_date=runTime)  # 定时执行任务
    scheduler.start() #启动任务

if __name__ == '__main__':
    itchat.auto_login() # 默认展示的是图片二维码
    # itchat.auto_login(hotReload=True) # 调试用的，保留登录状态
    now = dt.datetime.now() # 获取当前时间
    nextTickTime = now + dt.timedelta(days=1) #下一个问候时间为明天的现在
    nextTickTime = nextTickTime.strftime("%Y-%m-%d 00:00:00") # 把下一个问候时间设定为明天的零点
    my_scheduler(nextTickTime) # 启用定时操作
    itchat.run() # 启动微信