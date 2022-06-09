$(document).ready(function() {
    $("#createTable").on("click", function() {
        let columnsName = ["content", "type", "rate", "comment", "link"]
        let columnsType = ["text", "text", "number", "text", "url"]
        let cols = ["2", "1", "1", "7", "1"]
        
        // Criação dos elementos do HTML
        $("#spaceToCreate").append("<div></div>");
        $("#spaceToCreate div").append("<form></form>");
        $("#spaceToCreate div form").append("<span>Title:</span><input></input>");
        $("#spaceToCreate div form").append("<table></table>");
        $("#spaceToCreate div form").append("<span></span>")
        $("#spaceToCreate div form span:last-child").append("<button>Confirm</button>")
        
        // Criação dos atributos de todas as tags criadas anteriorment
        $("#spaceToCreate div form").attr({"method" : "post", "action" : "/addlist"});
        $("#spaceToCreate div form table").attr({"class" : "table rounded"});
        $("#spaceToCreate div form input").attr({"type" : "text", "name" : "table_name"});
        $("#spaceToCreate div form span button").attr({"type" : "submit", "class" : "ms-auto btn btn-primary d-flex"});
        
        let newTable = "#spaceToCreate div form table"
        let newBody = "#spaceToCreate div form table tbody tr"
    
        $(newTable).append("<thead></thead>")
        $(newTable).append("<tbody></tbody>")
    
        $(newTable + " thead").append("<tr></tr>")
        $(newTable + " tbody").append("<tr></tr>")
    
        // Construção do HEAD da tabela
        for (let i = 0; i < columnsName.length; i++) {
          $(newTable + " thead tr").append("<th>" + columnsName[i] + "</th>")
          $(newTable + " thead tr th:last-child").attr({"class" : "col-" + cols[i], "scope" : "col"})
        }
    
        // Construção do BODY da tabela
        for (let i = 0; i < columnsName.length; i++) {
          if (i == 3) {
            $(newBody).append("<td></td>");
            $(newBody + " td:last-child").addClass("align-top comments");
            $(newBody + " td:last-child").append("<textarea></textarea>");
            $(newBody + " td:last-child textarea").attr({
              "class" : "form-control",
              "type" : columnsType[i],
              "name" : columnsName[i],
              "maxlength" : "240",
              "id" : "comment"
            });
            $(newBody + " td:last-child").append("<span>240 Characters remaining</span>")
            $(newBody + " td:last-child span").attr({
              "class" : "char-remain",
              "style" : "font-size: 10px;"
            });
          } else {
            $(newBody).append("<td></td>");
            $(newBody + " td:last-child").addClass("align-top");
            $(newBody + " td:last-child").append("<input></input>");
            $(newBody + " td:last-child input").attr({
              "class" : "form-control",
              "type" : columnsType[i],
              "name" : columnsName[i]
            }); }
            
          $(newBody + " td:nth-child(3) input").attr({"step" : "0.01"});
        }
      });

    
      
      
    })