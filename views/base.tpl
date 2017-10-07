<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>MouZhiA</title>
<!-- Load bootstrap and mouzhia style -->
    <link href="/static/css/bootstrap.css" rel="stylesheet">
     <link href="/static/css/bootstrap-responsive.css" rel="stylesheet">
     <link rel="stylesheet" href="/static/css/MouZhiAStyle.css">

  </head>
  <body onload="loadLanguage()">
    <div class="container-narrow">
      <div class="masthead">
        <ul class="nav nav-pills pull-right">
           <li><a href="/about" class="lang" key="about" >About</a></li>
           <li><a href="" class="lang" key="account">Account</a></li>
        </ul>
        <h3 class="muted lang" key="productName">MouZhiA</h3>
      </div>
      <div class="jumbotron">
        <img class="engineIcon" src="static/images/searchEngineLogo.png" alt="">
        <form class="" action="/" method="GET">
        <input type="text" name="keywords" value=""   class="searchBar">
        <input type="submit" name="searchButton" value="Search" class="btn btn-primary searchButton">
        </form>
        <!--<button class="btn btn-small btn-info lang" name="button" key="searchButton" onclick="queryHandler">Search</button>-->
        <!--  <a class="btn btn-large btn-success lang" href="addques.php" key="addNewQuestion">Search</a>-->
      </div>

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
  </span>
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
<script src="/static/js/bootstrap-carousel.jss"></script>
<script src="/static/js/bootstrap-typeahead.js"></script>
<script type="text/javascript" src="/static/js/languageHandler.js"?v=1></script>
<script type="text/javascript" src="/static/js/cookieHandler.js"></script>

  </body>
</html>
