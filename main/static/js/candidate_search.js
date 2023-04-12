function filterCandidate() {
    let input, filter, table, tr, td, i, j, txtValue, flag=false;
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    table = document.getElementById("candidates");
    tr = table.getElementsByTagName('tr');
    for (i = 1; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td");
        for (j=0; j<td.length; j++) {
            if (td[j]) {
                txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    flag = true
                  break
                }
                else{
                    flag = false
                }
              }
        }
        if(flag) {
            tr[i].style.display = "";
        }
        else{
            tr[i].style.display = "none";
        }
    }
  }