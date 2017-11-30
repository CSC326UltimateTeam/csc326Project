%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)

<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>MouZhiA Result</title>
    <link href="/static/css/bootstrap.css" rel="stylesheet">
     <link href="/static/css/bootstrap-responsive.css" rel="stylesheet">
     <link rel="stylesheet" href="/static/css/MouZhiAStyle.css">
     <link rel="icon"  type="image/png" href="/static/images/searchEngineLogo.png">
  </head>
  <body onload="loadLanguage();">
<div class="container-narrow">
<div class="masthead">
  <ul class="nav nav-pills pull-right">
     <li><a href="/about" class="lang" key="about">About</a></li>
     <li class="dropdown">
        <a href="http://www.jquery2dotnet.com" class="dropdown-toggle" data-toggle="dropdown">{{accountText}} <b class="caret"></b></a>
      <ul class="dropdown-menu" style="padding-left: 5px; padding-right:5px; min-width: 200px; margin-left:-120px; text-align:center;font-size:13px;">
        <div class="image-upload">
        <label for="file-input">
        <img class="profilePhoto rounded" src={{userImage}} alt="">
         </label>
         <form class="changeProfilePhoto" action="/changeProfilePhoto" method="POST" enctype="multipart/form-data">
           {{!changePhotoHtml}}
          <!-- <input id="file-input"  name="profilePhoto" type="file" style="display:none" onchange="javascript:this.form.submit()" accept="image/*" >-->
         </form>

          </div>
        <br>
             {{!userInfoHtml}}
             {{!LogInOffHtml}}
            <!--li><a href="/account" class="lang" key="account"> Log In With Google </a></li>-->
        </ul>
     </li>
  </ul>
  <h3 > <a href="/" class="muted nav lang" key="productName">MouZhiA</a></h3>
  <form class="searchResultSearchBar " action="/" method="GET">
    <input type="text" name="keywords" value="{{keywords}}" id="keywords" >
    <input type="submit" id="searchButton"  value="Search" class="searchButton btn btn-primary btnInSearchResultSearch ">
  </form>
</div>
</div>
  <div class="resultTables" >
  <p style="color:grey; margin-left :10.2%; margin-top: -1%; margin-bottom: 1%"> About {{resultNumber}} results </p>
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

<div class="relatedSearch">
  <h1 style="font-size:20px; margin-left: 10%">Searches related to</h1>
  <table style="margin-left: 10%">
<tr>
  <td>blablabla</td>

  <td>blablabla</td>
</tr>
  </table>

</div>


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
      <script src="/static/js/searchHandler.js"></script>

  </body>
</html>
