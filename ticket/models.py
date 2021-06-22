from django.db import models

# Create your models here.

# build an airport model
class Airport(models.Model):
  flag = models.CharField("flag",db_column="flag",db_index=True,max_length=6,unique=True,primary_key=True)
  name = models.CharField("name",db_column="name",max_length=20,unique=True)
  city = models.CharField("city",db_column="city",max_length=20)
  pinyin = models.CharField("pinyin",db_column="pinyin",max_length=40)

  def __str__(self):
    return self.name
  class Meta:
    db_table = "airport"
    verbose_name_plural = "机场表"
    verbose_name = "机票表"

# create a ticket model
class AoyouTicket(models.Model):
  date = models.DateField("date",db_column="date")
  start_time = models.TimeField("start_time",db_column="start_time")
  end_time = models.TimeField("end_time",db_column="end_time")

  # note: Because both start_airport and related_name are foreign keys to Ariport,
  # order to ensure explicit reversing query, difference of related_name is necessary.
  start_airport = models.ForeignKey(Airport,verbose_name="start_airport",db_column="start_airport",\
    related_name="start_tickets",on_delete=models.SET_NULL,null=True,blank=True)
  end_airport = models.ForeignKey(Airport,verbose_name="end_airport",db_column="end_airport",\
    related_name="end_tickets",on_delete=models.SET_NULL,null=True,blank=True)

  airline = models.CharField("airline",db_column="airline",max_length=20)
  catagory = models.CharField("catagory",db_column="catagory",max_length=10)

  price = models.IntegerField("price",db_column="price")
  discount = models.DecimalField("discount",db_column="discount",max_digits=4,decimal_places=2)

  def __str__(self):
    return "Date:%s, Starting Time:%s, %s-->%s"%\
      (self.date,self.start_time,self.start_airport.city,self.end_airport.city)

  class Meta:
    db_table = "ticket"
    ordering = ["date","start_time","price"]
    get_latest_by = ["date","start_time"]
    verbose_name = "机票表"
    verbose_name_plural = "机票表"
  

# define an user model
class User(models.Model):
  name = models.CharField("name",max_length=20,db_column="name")
  password = models.CharField("password",max_length=20,db_column="password")
  email = models.EmailField("email",max_length=40,blank=True,null=True,db_column="email")
  tel = models.CharField("tel",max_length=12,db_column="tel")
  gender = models.BooleanField("gender",choices=((True,"male"),(False,"female")),db_column="gender")
  addr = models.CharField("address",db_column="address",max_length=100,blank=True,null=True)
  money = models.IntegerField("money",db_column="money",default=10000)

  user_tickets = models.ManyToManyField(AoyouTicket,db_table="user_tickets",related_name="users",verbose_name="tickets",blank=True,null=True)


  def __str__(self):
    return "%s,%s"%(self.name,self.tel)

  class Meta:
    db_table = "user"
    verbose_name = "用户表"
    verbose_name_plural = "用户表"

# define an advertisement model
class Advertisement(models.Model):
  title = models.CharField("title",db_column="title",max_length=50)
  price = models.IntegerField("price",db_column="price")
  link = models.CharField("link",db_column="link",max_length=200)
  city = models.CharField("city",db_column="city",max_length=20)

  def __str__(self):
    return "(%s)%s"%(self.city,self.title)
  class Meta:
    db_table = "advertisement"

    verbose_name = "广告表"
    verbose_name_plural = "广告表"



