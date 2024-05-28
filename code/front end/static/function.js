function generate_href(next_page_name, student_id) {
    return next_page_name + '?student_id=' + student_id;
}

function generate_href_with_operator_id(next_page_name, student_id, operator_id) {
    return next_page_name + '?student_id=' + student_id + '&operator_id=' + operator_id;
}

function sortTable(n) {
      var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
      table = document.getElementById("myTable");
      switching = true;
      dir = "asc";

      while (switching) {
        switching = false;
        rows = table.rows;

        for (i = 1; i < (rows.length - 1); i++) {
          shouldSwitch = false;
          x = rows[i].getElementsByTagName("TD")[n];
          y = rows[i + 1].getElementsByTagName("TD")[n];

          if (dir == "asc") {
            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
              shouldSwitch = true;
              break;
            }
          } else if (dir == "desc") {
            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
              shouldSwitch = true;
              break;
            }
          }
        }

        if (shouldSwitch) {
          rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
          switching = true;
          switchcount++;
        } else {
          if (switchcount == 0 && dir == "asc") {
            dir = "desc";
            switching = true;
          }
        }
      }

      // 切换排序图标样式
      var headers = table.getElementsByTagName("TH");
      for (i = 0; i < headers.length; i++) {
        headers[i].classList.remove("asc", "desc");
      }
      headers[n].classList.add(dir);
    }