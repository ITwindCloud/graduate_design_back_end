var active_images = document.getElementById("advertisement").getElementsByTagName("img");
var image_count = active_images.length;
var cur_index = 0;
window.setInterval(function(){
  var i = 0;
  for(;i<image_count;i++){
    if(i == (cur_index+1)%image_count){
      active_images[i].className = "";
    }
    else{
      active_images[i].className = "image_hidden";
    }
  }
  cur_index++;
},5000);