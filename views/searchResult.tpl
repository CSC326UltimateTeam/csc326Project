%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<p>Search for {{keywords}}</p>
<table id="results">
  <tr>
  <td><b>Word</b></td>
  <td><b>Count</b></td>
</tr>
  <tr>
%for row in dictionary:
  <tr>
    <td >{{row}} </td>
    <td > {{dictionary[row]}}</td>
  %end
  </tr>
%end
</table>
