<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>MouZhiA</title>
<!-- Load bootstrap and mouzhia style -->
    <link href="/static/css/bootstrap.css" rel="stylesheet">
     <link href="/static/css/bootstrap-responsive.css" rel="stylesheet">
     <link rel="stylesheet" href="/static/css/MouZhiAStyle.css">
     <link rel="icon"  type="image/png" href="/static/images/searchEngineLogo.png">
  </head>
  <body onload="loadLanguage()">
      <div id="dimmer" style="background:#000; opacity:0.5; position:fixed;   top:0; left:0; width:100%; height:100%; display:none; z-index:9999;"></div>
    <div class="container-fluid">
    <div class="container-narrow">
      <div class="masthead">
        <ul class="nav nav-pills pull-right">
           <li><a href="/about" class="lang" key="about" >About</a></li>
           <li>
              <a href="http://www.jquery2dotnet.com" class="dropdown-toggle" data-toggle="dropdown">{{!accountText}} <b class="caret"></b></a>
              <ul class="dropdown-menu" style="margin-top:-2%;min-width: 200px; margin-left:80%; min-height: 30px; text-align:center;font-size:13px;">

              <br>

              <div class="image-upload">
              <label for="file-input">
              <img class="profilePhoto rounded" src={{userImage}} alt="">
               </label>
               <form class="changeProfilePhoto" action="/changeProfilePhoto" method="POST" enctype="multipart/form-data">
                 {{!changePhotoHtml}}
                <!-- <input id="file-input"  name="profilePhoto" type="file" style="display:none" onchange="javascript:this.form.submit()" accept="image/*" >-->
               </form>

                </div>

                   {{!userInfoHtml}}
                   {{!LogInOffHtml}}
                  <!--li><a href="/account" class="lang" key="account"> Log In With Google </a></li>-->
              </ul>
           </li>


           <!-- drop down feature -->


        </ul>


        <h3 class="muted lang" key="productName">MouZhiA</h3>
      </div>

      <div class="jumbotron">
<div id="engineLogo" style="width:40% ;margin-left:30%; padding-top:3%; "  >    </div>
<div id="loadingAnimation" style="width:80% ;margin-left:10%; margin-bottom:-23%; display:none; margin-top:-18%"  >    </div>
<p id="analyzing" class="lang" key="loadingText" style="font-size:30px; text-align:center; color: #999999; font-weight:bold;display:none">A N A L Y Z I N G</p>

        <!--<img class="engineIcon" src="static/images/searchEngineLogo.png" alt="">-->
        <form class="" action="/" method="GET" id="searchForm" style="display:true">
          <div class="dropdown">
    <input type="text" name="keywords" value=""   class="searchBar dropdown-toggle"  data-toggle="dropdown" onkeyup="">
    <ul  class="dropdown-menu" style="margin-left: 32%; width:36%; margin-top: -0.7%; font-size:19px;  font-family:'Courier New', Courier, monospace;">
    {{ !historyBarHtml}}

    </ul>
          </div>
        <input type="submit" id="searchButton" value="Search" class="btn btn-primary searchButton">
        </div>
        </form>
        <form class="imagenet" name="imagenetForm" action="/imagenet" method="POST" style="display:none" enctype="multipart/form-data">
          <input id="imagenet-upload"  name="imageSearch" type="file" style="display:none" onchange="dim(); this.form.submit();" accept="image/*" >
        </form>
        <!--<button class="btn btn-small btn-info lang" name="button" key="searchButton" onclick="queryHandler">Search</button>-->
        <!--  <a class="btn btn-large btn-success lang" href="addques.php" key="addNewQuestion">Search</a>-->
      </div>

    </div>
<hr>
<div class="container-fluid">
<div class="footer">
  <p>&copy;
    <span class="lang" key="copyRight">2017 CSC326UltimateTeam</span>
  <span class="langsetting">
    <span class="lang" key="languageText"> Language:</span>
    <select id="changeLang" onchange="languageChange();">
       <option  class="lang" value="en" key="langEnglish" >English</option>
       <option class="lang" value="zh" key="langChinese">中文</option>
    </select>
  </span>
  </p>
</div>
</div>
<!-- load all javascript from here -->
<script src="/static/js/jquery.js"></script>
<script src="/static/js/bootstrap-transition.js"></script>
<script src="/static/js/bootstrap-alert.js"></script>
<script src="/static/js/bootstrap-modal.js"></script>
<script src="/static/js/bootstrap-dropdown.js"></script>
<script src="/static/js/bootstrap-scrollspy.js"></script>
<script src="/static/js/bootstrap-tab.js"></script>
<script src="/static/js/bootstrap-tooltip.js"></script>
<script src="/static/js/bootstrap-popover.js"></script>
<script src="/static/js/bootstrap-button.js"></script>
<script src="/static/js/bootstrap-collapse.js"></script>
<script src="/static/js/bootstrap-carousel.js"></script>
<script src="/static/js/bootstrap-typeahead.js"></script>
<script src="/static/js/bodymovin.js" type="text/javascript"></script>
<script src="/static/js/engineAnimation.js"></script>
<script src="/static/js/searchHandler.js"></script>
<script type="text/javascript" src="/static/js/languageHandler.js"?v=1></script>
<script type="text/javascript" src="/static/js/cookieHandler.js"></script>
<script>
var loadingAnimation = bodymovin.loadAnimation({
  container: document.getElementById('loadingAnimation'), // Required
  path: 'static/js/loadingResult.json', // Required
  renderer: 'svg', // Required
  loop: true, // Optional
  autoplay: false, // Optional
  name: "loadingAnimation", // Name for future reference. Optional.
});

loadingAnimation.play();
 $(document).ready(function(){

      $('.searchBar').keyup(function(){
           var query = $(this).val();
           if(query != '')
           {
                $.ajax({
                     url:"/suggestion",
                     method:"POST",
                     data:{query:query},
                     success:function(data)
                     {
                          $('.dropdown ul').empty()
                          $('.dropdown ul').append(data)
                     }
                });
           }
           else{
                $('.dropdown ul').empty()
                if(language == 'en'){
                  $('.dropdown ul').append('<label for="imagenet-upload"> <li style="font-size: 19px;text-align:left;margin-left:4%" class="lang" key="searchImage"">Search with Image </li></label>')
                }else{
                  $('.dropdown ul').append('<label for="imagenet-upload"> <li style="font-size: 19px;text-align:left;margin-left:4%" class="lang" key="searchImage"">使用图片搜索 </li></label>')
                }


           }
      });
 });
 </script>
<script>
// When the user clicks on div, open the popup
function myFunction() {
    var popup = document.getElementById("myPopup");
    popup.classList.toggle("show");
}

function dim()
{
  console.log("dim");
  animation.stop();
  animation.destroy();
  document.getElementById("loadingAnimation").style.display = "";
  document.getElementById("searchForm").style.display = "none";
  document.getElementById("analyzing").style.display = "";
}

</script>
  </body>
</html>
