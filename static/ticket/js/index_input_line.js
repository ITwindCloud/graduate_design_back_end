new Vue({
  delimiters:["[[","]]"],
  el:"#order",
  data:{
    start:"",
    end:"",
    start_date:"",
    test:"",
    dates:[],
    date_args:[],
    num:-1,
    date_num:0,
  },
  mounted(){
    this.today_date_format()
  },
  methods:{
    today_date_format(){
      var today = new Date();
      var year = today.getFullYear(),month = today.getMonth(),day = today.getDate();
      month+=1;
      if(month<10){
        month = "0"+month;
      }
      if(day<10){
        day = "0"+day;
      }
      var str_date = year + "-" + month + "-" + day;
      this.start_date = str_date;
      this.start_date_change();
    },//today_date_format
    start_date_change(){
      axios({
        // url:"{% url 'ticket:four-dates' %}",
        url:"/ticket/four-dates/",
        method:"get",
        params:{
          "date":this.start_date
        }
      }).then(res=>{
        console.log(res.data.data);
        this.dates = res.data.data.dates;
        this.date_args = res.data.data.date_args;
        this.date_num = res.data.data.select;
        this.start_date = res.data.data.start_date;
      },function(){
        console.log("Failure");
      })
    },//start_date_change
    change_num(num){
      this.num = num;
    },//change_num
    click_start_date(x){
      this.start_date = x;
      this.start_date_change();
    },//click_start_date
    click_end_city(x){
      this.end = x;
    },//click_end_city
  }
})

