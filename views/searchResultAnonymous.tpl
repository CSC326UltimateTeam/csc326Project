%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)

<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="Expires" CONTENT="0">
   <meta http-equiv="Cache-Control" CONTENT="no-cache">
   <meta http-equiv="Pragma" CONTENT="no-cache">
    <title>MouZhiA Result</title>
    <link href="/static/css/bootstrap.css" rel="stylesheet">
     <link href="/static/css/bootstrap-responsive.css" rel="stylesheet">
     <link rel="stylesheet" href="/static/css/MouZhiAStyle.css">
     <link rel="icon"  type="image/png" href="/static/images/searchEngineLogo.png">
  </head>
  <body onload="loadLanguage();">
<div class="container-narrow">
<div class="masthead" style="height:13%" >
  <ul class="nav nav-pills pull-right">
     <li><a href="/about" class="lang" key="about" >About</a></li>
     <li class="dropdown">
        <a href="http://www.jquery2dotnet.com" class="dropdown-toggle" data-toggle="dropdown">{{!accountText}} <b class="caret"></b></a>
        <ul class="dropdown-menu" style="padding-left: 5px; padding-right:5px; min-width: 200px; min-height: 30px; margin-left:-120px; text-align:center;font-size:13px;">

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

  <h3 style="margin-top:2%; margin-left:-1%" > <a href="/" class="muted nav lang" key="productName" >MouZhiA</a></h3>
   <span class="dropdownSearchBar">
  <form class="searchResultSearchBar " action="/" method="GET" style="width:70%; margin-left:-2%">
    <input type="text" name="keywords" value="{{keywords}}"  class="dropdown-toggl searchBar" id="keywords" data-toggle="dropdown" style="width:22%; font-size:17px; position: relative;" >
    <ul  class="dropdown-menu" style="top: 65px;  right: 0;text-align:left; width:220px; font-size:13px; margin-left:18%; font-size:13px; position: absolute; font-family:'Courier New', Courier, monospace;">
      {{ !historyBarHtml}}
    </ul>
</span>
      <input type="submit" id="searchButton"  value="Search" class="searchButton btn btn-primary btnInSearchResultSearch "  style="margin-top:-1%; margin-left:1%">


  </form>
  <form class="imagenet" name="imagenetForm" action="/imagenet" method="POST" style="display:none" enctype="multipart/form-data">
    <input id="imagenet-upload"  name="imageSearch" type="file" style="display:none" onchange="dim(); this.form.submit();" accept="image/*" >
  </form>

    </div>

</div>

<div class="center" style=" position: fixed;
    /* center the element */
    right: 0;
    left: 0;
    top:-100px;
    margin-right: auto;
    margin-left: auto;
    /* give it dimensions */
    min-height: 10em;
    width: 80%; display :none ;   z-index: 100;" id="loadingAnimation"></div>





  <div class="resultTables" >
  <p style="color:grey; margin-left :10.2%; margin-top:1%; margin-bottom: 1%"> <span class="lang" key="Aboutresult">About</span> {{resultNumber}} <span class="lang" key="aboutResult">results</span> </p>
<!--
  <div class="" style="margin-left: 13%; margin-top: 5%; font-size:16px;">
    <p>Your search - <strong>blablabla</strong> - did not match any documents</p>
    <br>
    <p>Suggestions:</p>
    <li>Make sure that all words are spelled correcly</li>
    <li>Try different keywords</li>
    <li>Try more general keywords</li>
    <li>Try fewer keywords</li>
    <img style="margin-left:45%; width:20%; margin-top:-15%"  src="static/images/noResult.png" alt="">
  </div>
-->
<!--
  <div class="" style="margin-left:12%">
    <h3><a href="#" style="color: #1C1BA8">Feiran is handsome</a></h3>
    <p style="margin-top:-1.2%; "><a href="#" style=" color:green;">https://feiranishandsome.com</a></p>
    <p style="margin-top:-0.5%;">blabablablalbalblalblalblablalbl</p>
    <p></p>
  </div>
  <div class="" style="margin-left:12%">
    <h3><a href="#" style="color: #1C1BA8">Feiran is handsome</a></h3>
    <p style="margin-top:-1.2%; "><a href="#" style=" color:green;">https://feiranishandsome.com</a></p>
    <p style="margin-top:-0.5%;">blabablablalbalblalblalblablalbl</p>
    <p></p>
  </div>
-->
{{!urlHtml}}

<!-- Modal -->
<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title lang" id="exampleModalLabel" key="preview">Preview</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <img id="modalImage" src="" alt="">
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary lang" data-dismiss="modal" key="closeBtn">Close</button>
      </div>
    </div>
  </div>
</div>






  </div>

<!--
 <div class="paging-nav">

      <a href="" class="pagenav">1</a>
      <a href="" class="pagenav">2</a>
      <a href="" class="pagenav">3</a>
      <a href="" class="pagenav">4</a>
      <a href="" class="pagenav">5</a>
      <a href="" class="pagenav">6</a>
      <a href="" class="pagenav">7</a>

  </div>-->




  {{!navUrl}}

     <hr>
      <div class="footer">
        <p>&copy;
          <span class="lang" key="copyRight">2017 CSC326UltimateTeam</span>
        <span class="langsetting">
          <span class="lang" key="languageText"> Language:</span>
          <select id="changeLang" onchange="languageChange();">
             <option  class="lang" value="en" key="langEnglish" >English</option>
             <option class="lang" value="zh" key="langChinese">中文</option>
          </select>
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
      <script type="text/javascript" src="/static/js/languageHandler.js"?v=1></script>
      <script type="text/javascript" src="/static/js/cookieHandler.js"></script>
      <script src="/static/js/bodymovin.js" type="text/javascript"></script>
      <script type="text/javascript">
      var animation = bodymovin.loadAnimation({
        container: document.getElementById('emojiAnimation'), // Required
        path: 'static/js/emojiAnimation.json', // Required
        renderer: 'svg', // Required
        loop: true, // Optional
        autoplay: true, // Optional
        name: "Emoji Animation", // Name for future reference. Optional.
      })

      var loadingAnimation = bodymovin.loadAnimation({
        container: document.getElementById('loadingAnimation'), // Required
        path: 'static/js/loadingResult.json', // Required
        renderer: 'svg', // Required
        loop: true, // Optional
        autoplay: true, // Optional
        name: "loadingAnimation", // Name for future reference. Optional.
      });


      </script>
      <script src="/static/js/searchHandler.js"></script>
      <script>
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
                                $('.dropdownSearchBar ul').empty()
                                $('.dropdownSearchBar ul').append(data)
                           }
                      });
                 }
                 else{
                      $('.dropdownSearchBar ul').empty()
                      if(language == 'en'){
                        $('.dropdownSearchBar ul').append('<label for="imagenet-upload"> <li style="font-size:13px; text-align:left;margin-left:4%" class="lang" key="searchImage" >Search with Image </li></label>')
                      }else{
                        $('.dropdownSearchBar ul').append('<label for="imagenet-upload"> <li style="font-size:13px; text-align:left;margin-left:4%" class="lang" key="searchImage" >使用图片搜索 </li></label>')
                      }

                 }
            });

           $('.screenshotBtn').click(function(){
             $('#loadingAnimation').show()
             $('#modalImage').attr('src','')
             console.log("screenShot");
            url = $(this).attr('key')
            if(url != ''){
            $.ajax({
              url: "/screenshot",
              method:"POST",
              data: {url:url},
              success:function(data){
              $('#loadingAnimation').hide()
              $('#modalImage').attr('src',data)
              $('#myModal').modal('show');

              }
            });
            }
           });


        });

        function dim()
        {
          document.getElementById("loadingAnimation").style.display = "";
        }


       </script>
       <script type="text/javascript">
         function linkTools() {
         console.log("clicked");
         }
       </script>
  </body>
</html>
