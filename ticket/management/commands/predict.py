from django.core.management.base import CommandError,BaseCommand
from ticket.models import AoyouTicket
from sklearn.externals import joblib
from ticket.views.order import get_one_ticket_info
import datetime

class Command(BaseCommand):
  help = "Get transferring cases from Beijin to Shanghai"
  def handle(self,*args,**option):
    date = datetime.date(year=2021,month=5,day=24)
    tickets = AoyouTicket.objects.filter(date=date,start_airport__name__contains="武汉",end_airport__name__contains="上海")

    log = open("predict.log","a+")
    for t in tickets:
      data = get_one_ticket_info(t.id,"12345678910")
      model = joblib.load("rfc.joblib")

      # traits = ["id","price","price_rate","day_in_month","day_in_week","is_weekday"]
      # 整理需要训练的数据
      user_id = data["user_info"]["id"]
      price = data["ticket"]["price"]
      price_rate = 99
      day_in_month = data["ticket"]["date"].day
      day_in_week = data["ticket"]["date"].weekday() + 1
      is_weekday = 0
      if day_in_week == 7:
        is_weekday = 1
      train_data = [[user_id,price,price_rate,day_in_month,day_in_week,int(is_weekday)]]
      # 折扣小到大遍历，找到吸引用户购票的最小折扣
      self.stdout.write(str(train_data))
      i = 99
      while i >= 10:
        train_data[0][2] = i
        if model.predict(train_data)[0] == 1:
          self.stdout.write(str(model.predict(train_data)[0]))
          break
        i -= 1

      is_discounted = 0
      discount = 100
      if i >= 10:
        is_discounted = 1
        discount = i
        log.write(str(train_data[0][0])+","+str(train_data[0][1])+","+str(date)+"\n")
      self.stdout.write(str(is_discounted))
      self.stdout.write(str(i))

      log.close()

