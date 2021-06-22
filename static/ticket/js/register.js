new Vue({
  delimiters:["[[","]]"],
  el:"#user_info",
  data:{
    //昵称
    name:"",
    is_name_error:false,
    name_error:"此项为必填项",
    //电话号码
    tel:"",
    is_tel_error:false,
    tel_error:"此项为必填项",
    //邮箱
    email:"",
    is_email_error:false,
    email_error:"邮箱格式有误",

    gender:"男",

    pd1:"",
    is_pd1_error:false,
    pd1_error:"此项不能为空",

    pd2:"",
    is_pd2_error:false,
    pd2_error:"此项不能为空",

    is_pd12_error:false,
    pd12_error:"两次密码不一致",

    abbr:"",
  },
  mounted(){

  },
  methods:{
    check_name(){
      if(!this.name.trim()){
        this.is_name_error = true;
      }
      else{
        this.is_name_error = false;
      }
    },//check_name
    check_tel(){
      var trim_tel = this.tel.trim()
      if(!trim_tel){
        this.is_tel_error = true;
        this.tel_error = "此项为必填项"
      }
      else if(trim_tel.search(/^1\d*$/) == -1 || trim_tel.length != 11){
        this.is_tel_error = true;
        this.tel_error = "电话格式有误";
      }
      else{
        this.is_tel_error = false;
      }
    },//check_tel
    check_email(){
      if(!this.email.trim()){
        this.is_email_error = true;
        this.email_error = "此项为必填项";
      }
      else if(this.email.trim().search(/^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/) == -1){
        this.is_email_error = true;
        this.email_error = "邮箱格式有误";
      }
      else{
        this.is_email_error = false;
      }
    },//check_email
    check_pd12(){
      if(!this.pd1){
        this.is_pd1_error = true;
        this.pd1_error = "此项为必填项";
        this.is_pd12_error = false;
      }
      else if(this.pd1.search(/^[0-9a-zA-Z_]*$/) == -1){
        this.is_pd1_error = true;
        this.pd1_error = "密码包含不合法字符，只能包含数组、字母和下划线";
      }
      else if(this.pd1.length <6){
        this.is_pd1_error = true;
        this.pd1_error = "密码至少由6个字符组成";
      }
      else{
        this.is_pd1_error = false;
      }
      
      if(!this.pd2){
        this.is_pd2_error = true;
        this.pd2_error = "此项为必填项";
        this.is_pd12_error = false;
      }
      else{
        this.is_pd2_error = false;
      }

      if(!this.is_pd1_error && !this.is_pd2_error){
        if(this.pd1 != this.pd2){
          this.is_pd12_error = true;
        }
        else{
          this.is_pd12_error = false;
        }
      }
      
    },//check_pd12
    submit(){
      this.check_name();
      this.check_tel();
      this.check_email();
      this.check_pd12();

      if(!this.is_name_error && !this.is_tel_error && !this.is_email_error &&
        !this.is_pd1_error && !this.is_pd2_error && !this.is_pd12_error){
          axios({
            url:"/ticket/register/",
            method:"post",
            data:{
              name:this.name,
              tel:this.tel,
              email:this.email,
              password:this.pd1,
              gender:this.gender,
              abbr:this.abbr
            },
            transformRequest:[function(data){
              let ret = ""
              for(let it in data){
                ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
              }
              return ret
            }],
            headers:{
              "Content-Type":"application/x-www-form-urlencoded"
            }
          }).then(res=>{
            console.log(res.data.data);
            if(res.data.data){
              this.is_tel_error = res.data.data.is_tel_error;
              this.is_email_error = res.data.data.is_email_error;
              this.tel_error = res.data.data.tel_error;
              this.email_error = res.data.data.email_error;
            }
            if(res.data.success){
              window.location.href = "/ticket/login/"
            }
          },function(){
            console.log("Failing Request!");
          })
      }

      // 待加入与后台的交互
    }

  },
})