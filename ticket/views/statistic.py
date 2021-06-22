import pandas as pd
import datetime
def month_and_day(x):
    '''
    横轴刻度标签精确到月日
    '''
    temp = []
    for one in x:
        temp.append(one.strftime("%m-%d"))
    return temp

def top_price_list2(x,y,date_range):
    text = []
    def get_price(someday):
        for i in range(x.shape[0]):
            if x[i].strftime("%Y-%m-%d") == someday.strftime("%Y-%m-%d"):
                return y[i]
        
    for d in date_range:
        if d in x:
            p = get_price(d)
            text.append(float("%.0d"%p))
        else:
            text.append("-")
    return text

def statistic(x,y):
  date_range = pd.date_range(datetime.date.today(),periods=10,freq="D",closed="left")
  # date_range = pd.date_range(datetime.date(year=2021,month=5,day=5),periods=10,freq="D",closed="left")
  text = top_price_list2(x,y,date_range)
  return text

def get_labels():
  date_range = pd.date_range(datetime.date.today(),periods=10,freq="D",closed="left")
  # date_range = pd.date_range(datetime.date(year=2021,month=5,day=5),periods=10,freq="D",closed="left")
  yticklabels = month_and_day(date_range)
  return yticklabels