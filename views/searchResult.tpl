%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)

<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>MouZhiA Result</title>
    <link href="/static/css/bootstrap.css" rel="stylesheet">
     <link href="/static/css/bootstrap-responsive.css" rel="stylesheet">
     <link rel="stylesheet" href="/static/css/MouZhiAStyle.css">
  </head>
  <body onload="loadLanguage();">
<div class="container-narrow">
<div class="masthead">
  <ul class="nav nav-pills pull-right">
     <li><a href="index.php" class="lang" key="about">About</a></li>
     <li><a href="manage.php" class="lang" key="account">Account</a></li>
  </ul>
  <h3 > <a href="/" class="muted nav lang" key="productName">MouZhiA</a></h3>
  <form class="searchResultSearchBar " action="/" method="GET">
    <input type="text" name="keywords" value="{{keywords}}">
    <input type="submit" name="searchButton" value="Search" class="searchButton btn btn-primary btnInSearchResultSearch ">
  </form>
</div>
</div>

    <div class="row-fluid marketing resultTables">
      <p>Search for {{keywords}}</p>
      <table id="results" class="table table-striped">
        <tr>
        <td><b>Word</b></td>
        <td><b>Count</b></td>
      </tr>
      %for row in dictionary:
        <tr>
          <td >{{row}} </td>
          <td > {{dictionary[row]}}</td>
        </tr>
      %end
      </table>

      <p>Top 20 Keywords in History</p>
      <table id="history" class="table table-striped">
        <tr>
          <th>Word</th>
          <th>Count</th>
        </tr>
      %for item in history:
         <tr>
           <td>{{item}}</td>
           <td>{{history[item]}}</td>
         </tr>
      %end
      </table>


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
