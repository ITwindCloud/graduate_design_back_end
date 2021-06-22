from rest_framework.response import Response
from rest_framework.decorators import api_view
# from django.views.csrf.decorators import csrf_exempt
import datetime

@api_view(["GET"])
def get_four_date(request):
  today_str = datetime.date.today()
  date_str = request.GET.get("date",today_str.strftime("%Y-%m-%d"))
  year = int(date_str[0:4])
  month = int(date_str[5:7])
  day = int(date_str[8:10])

  dates = []
  date_args = []

  date = datetime.date(year,month,day)
  # 输入过去的日期
  if date < datetime.date.today():
    date = datetime.date.today()

  start = 0
  end = 4
  select = 0
  if date > datetime.date.today():
    select = 1
    start = -1
    end = 3
    
  for i in range(start,end):
    cur_date = date+datetime.timedelta(days=i) 
    date_args.append(cur_date.strftime("%Y-%m-%d"))
    dates.append(str(cur_date.month)+"月"+str(cur_date.day)+"日")

  data = {
    "dates":dates,
    "date_args":date_args,
    "select":select,
    "start_date":date.strftime("%Y-%m-%d")
  }

  return Response({"data":data})