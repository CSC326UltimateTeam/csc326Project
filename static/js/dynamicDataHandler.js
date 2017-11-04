$(window).scroll(function(){
if ($(window).scrollTop() == $(document).height() - $(window).height()){
if($(".pagenum:last").val() <= $(".rowcount").val()) {
var pagenum = parseInt($(".pagenum:last").val()) + 1;
getresult('/?page='+pagenum);
}
}
});


function getresult(url) {
$.ajax({
url: url,
type: "GET",
data:  {rowcount:$("#rowcount").val()},
beforeSend: function(){
$('#loader-icon').show();
},
complete: function(){
$('#loader-icon').hide();
},
success: function(data){
$("#faq-result").append(data);
},
error: function(){}
});
}
