from django.core.management.base import BaseCommand,CommandError
# from django.core import serializers
from ticket.models import AoyouTicket,Airport
import datetime
import pandas as pd
import matplotlib.pyplot as plt
# from .price_trend_pic import generate_price_picture

from django.conf import settings

# noramlly display chinese characters 
plt.rcParams["font.sans-serif"] = ["SimHei"]

class Command(BaseCommand):
  help = "Access the first ticket from the ticket table."
  def handle(self,*args,**options):
    '''
    Execute the command: python manage.py main
    :params args:
    :params options:
    :return:
    '''
    start = "北京"
    end = "深圳"
    date = datetime.date.today()

    # access data
    sql_table = AoyouTicket.objects.filter(start_airport__name__contains=start,end_airport__name__contains=end).values("date","price")

    # make data ordered
    data = pd.DataFrame(sql_table,columns=["date","price"])
    data["date"] = data["date"].astype("datetime64[ns]")
    result = data.groupby("date").agg({"price":["max","mean","min"]})

    # split data into three fractions
    x = result.index
    min_y = result[("price","min")].values
    mean_y = result[("price","mean")].values
    max_y = result[("price","max")].values

    base_path = settings.BASE_DIR
    
    min_path = base_path + "\\ticket\\static\\ticket\\images\\price_trend\\" + "lowest-price-%s-%s-%s.jpg"%(date.strftime("%Y-%m-%d"),start,end)
    generate_price_picture(x,min_y,min_path)

    mean_path = base_path + "\\ticket\\static\\ticket\\images\\price_trend\\" + "mean-price-%s-%s-%s.jpg"%(date.strftime("%Y-%m-%d"),start,end)
    generate_price_picture(x,mean_y,mean_path)

    max_path = base_path + "\\ticket\\static\\ticket\\images\\price_trend\\" + "highest-price-%s-%s-%s.jpg"%(date.strftime("%Y-%m-%d"),start,end)
    generate_price_picture(x,max_y,max_path)

    self.stdout.write("Program Ended!")

    # count = beijin_shanghai.count()
    # self.stdout.write(str(count))
    # json = serializers.serialize("json",beijin_shanghai)
    # self.stdout.write(json)

'''
self-defination of django-admin commands

Create management->commands->python modules in one application
Every module is corresponding to every command.

In the python module, define a Command class that inherits django.core.manage.base.BaseCommand

Note: "_" is not allowed in the begin of the module name, 
    otherwise the django system views it an invalid module.

'''


def month_and_day(x):
    '''
    横轴刻度标签精确到月日
    '''
    temp = []
    for one in x:
        temp.append(one.strftime("%m-%d"))
    return temp

def ytick(y):
    temp = []
    maxinum = y.max()
    increment = 100
    extra = 50
    i = 100
    if maxinum > 1000 and maxinum < 2000:
        increment = 200
        i = 200
        extra = 100
    elif maxinum < 3000:
        increment = 300
        i = 300
        extra = 200
    else:
        increment = 500
        i = 500
        extra = 400
        
    while i < maxinum:
        temp.append(i)
        i += increment
    
    temp.append(i)
    temp.append(int(y.min()))
    temp.append(int(maxinum)+50)
    return temp
                
def generate_color(y):
    '''
    每一个条形区域取定一个颜色
    '''
    teal = "#45a0a2" # 中间价格
    red = "#e87a59" # 最低价格
    blue_gray = "#4f6268" # 最高价格
    mininum = y.min()
    maxinum = y.max()
    temp = []
    for one in y:
        if one == mininum:
            temp.append(red)
        elif one == maxinum:
            temp.append(blue_gray)
        else:
            temp.append(teal)
    return temp

def top_price_list(x,y,date_range):
    '''
    在条形区域底部显示出价格
    空缺的价格标记为空缺，灰蓝色显示
    '''
    red = "#dc2624"
    grey = "#4f6268"
    color = []
    text = []
    price = []
    def get_price(someday):
        for i in range(x.shape[0]):
            if x[i].strftime("%Y-%m-%d") == someday.strftime("%Y-%m-%d"):
                return y[i]
        
    for d in date_range:
        if d in x:
            p = get_price(d)
            text.append("%.0d"%p)
            color.append(red)
            price.append(p)
        else:
            text.append("空缺")
            color.append(grey)
            price.append(0)
    return text,color,price
    
def generate_price_picture(x,y,saving_path):
    
    # 生成画布
    fig = plt.figure(figsize=(12,6),dpi=100)
    
    # 生成坐标轴
    ax = fig.add_subplot(1,1,1)
    
    # 绘出条形图
    color = generate_color(y)
    ax.bar(x,y,color=color,width=0.95)
    # 隐藏坐标轴的右边和上边的轴
    ax.spines["top"].set_visible(False) 
    ax.spines["right"].set_visible(False)
    # 表示最低价格的水平线
    ax.axhline(y=y.min(),ls=":",c="#dc8018")
    ax.axhline(y=y.max(),ls=":",c="#dc8018")
    
    # 确定日期的范围
    incr = datetime.timedelta(days=1)
    ax.set_xlim([datetime.date.today()-incr,datetime.date.today()+incr*10])
    # 日期的刻度标签
    date_range = pd.date_range(datetime.date.today(),periods=10,freq="D",closed="left")
    yticklabels = month_and_day(date_range)
    ax.set_xticks(date_range)
    ax.set_xticklabels(yticklabels,fontdict={"size":20})
    
    # 柱形区域顶部显示价格信息
    texts,text_colors,prices = top_price_list(x,y,date_range)
    for i in range(date_range.shape[0]):
        ax.text(date_range[i],prices[i]+10,texts[i],color=text_colors[i],fontsize=18,horizontalalignment='center')
    
    # 设置价格标签刻度
    y_ticks = ytick(y)
    ax.set_yticks(y_ticks[0:-1])
    ax.set_yticklabels(y_ticks[0:-1])
    ax.set_ylim([0,y_ticks[-1]+50])
    for text in ax.get_yticklabels():
        if text.get_text() == str(int(y.min())):
            text.set(fontsize=16,color="#dc8018")
        else:
            text.set(fontsize=20)
    fig.savefig(saving_path,bbox_inches = 'tight')
    

# generate_price_picture(x,y,"lowest-price-2021-03-22-beijin-shanghai.jpg")
    