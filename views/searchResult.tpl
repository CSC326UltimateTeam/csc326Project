%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<p>Search for {{keywords}}</p>
<table id="results">
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
<table id="history">
%for item in history:
   <tr>
     <td>{{item}}</td>
   </tr>
%end
</table>
