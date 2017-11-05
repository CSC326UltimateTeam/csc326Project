%#about page

<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Error Page</title>
    <link href="/static/css/bootstrap.css" rel="stylesheet">
     <link href="/static/css/bootstrap-responsive.css" rel="stylesheet">
     <link  rel="stylesheet" href="/static/css/MouZhiAStyle.css">
     <style type="text/css">
       body {
         padding-top: 20px;
         padding-bottom: 40px;
       }

       /* Custom container */
       .container-narrow {
         margin: 0 auto;
         max-width: 100%;
       }
       .container-narrow > hr {
         margin: 30px 0;
       }

       /* Main marketing message and sign up button */
       .jumbotron {
         margin: 60px 0;
         text-align: center;
       }
       .jumbotron h1 {
         font-size: 72px;
         line-height: 1;
       }
       .jumbotron .btn {
         font-size: 21px;
         padding: 14px 24px;
       }

       /* Supporting marketing content */
       .marketing {
         margin: 60px 0;
       }
       .marketing p + h4 {
         margin-top: 28px;
       }
       .masthead {
     padding-bottom: 15px;
     border-bottom: 1px solid #eeeeee ;
     display:block;
     position:fixed;
     background:#fff;
     width:100%;
     top:0;
 }

 .muted{
     color: #999999;
     margin-left: 10%;
     margin-top: 23px;
 }

 ul.nav.nav-pills.pull-right {
     margin-right: 10%;
     margin-top: 29px;
     margin-bottom: 0;
 }

 .footer {
     padding-left: 10%;
     padding-right: 10%;
 }
 span.langsetting {
     float: right;
 }
 .contact-main {
     width: 30%;
     margin: 0 auto;
     margin-top: 15%;
     margin-bottom: 15%;
 }
 div.contact-main blockquote {
     font-size: 20px;
     line-height: 2;
 }
     </style>
  </head>
  <body onload="loadLanguage()">
<div class="container-narrow">
  <div class="masthead">
    <ul class="nav nav-pills pull-right">
       <li><a href="/about" class="lang" key="about">About</a></li>
    </ul>
    <h3 > <a href="/" class="muted nav lang" key="productName">MouZhiA</a></h3>
  </div>


</div>
<div class="errorContainer">
  <a href="/"><img class="errorIcon" src="static/images/searchEngineLogo.png" alt="" style="margin-top:2%"></a>
  <img class="teapot" src="static/images/error500.png" alt="">
  <p class="errorMessage" style="margin-top:-10%" ><strong style="font-size:30px;">500</strong>. <span style="color: grey;">I'm a teapot.  </span> <br> <br><span style="font-size:16px; padding-top=-10%;">Oops. Something went wrong.</span></p>
</div>

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

  </p>
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

  </body>
</html>
