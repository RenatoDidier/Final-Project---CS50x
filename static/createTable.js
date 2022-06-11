$(document).ready(function() {
    $("#createTable").on("click", function() {
        let columnsName = ["content", "type", "rate", "comment", "link"]
        let columnsType = ["text", "text", "number", "text", "url"]
        let cols = ["2", "1", "1", "7", "1"]

        let insideForm = "#spaceToCreate div form";
        
        // Criação de todos elementos necessários 
        $("#spaceToCreate").append("<div></div>");
        $("#spaceToCreate div").append("<form></form>");
        $(insideForm).append("<span>Title:</span><input></input>");
        $(insideForm).append("<table></table>");
        $(insideForm).append("<span></span>")
        $(insideForm + " span:last-child").append("<button>Confirm</button>")
        
        // Criação dos atributos de todas as tags criadas anteriormente
        $(insideForm).attr({"method" : "post", "action" : "/addlist"});
        $(insideForm + " table").attr({"class" : "table rounded"});
        $(insideForm + " input").attr({"type" : "text", "name" : "table_name"});
        $(insideForm + " span button").attr({"type" : "submit", "class" : "ms-auto btn btn-primary d-flex"});
        
        let newTable = "#spaceToCreate div form table"
        let newData = "#spaceToCreate div form table tbody tr td:last-child"

        // Criação dos elementos primários da nossa table
        $(newTable).append("<thead></thead>")
        $(newTable).append("<tbody></tbody>")

        $(newTable + " thead").append("<tr></tr>")
        $(newTable + " tbody").append("<tr></tr>")
    
        // Construção do tHEAD da tabela
        for (let i = 0; i < columnsName.length; i++) {
          $(newTable + " thead tr").append("<th>" + columnsName[i] + "</th>")
          $(newTable + " thead tr th:last-child").attr({"class" : "col-" + cols[i], "scope" : "col"})
        }
    
        // Construção do tBODY da tabela
        for (let i = 0; i < columnsName.length; i++) {
          // A data "comment" possui vários campos diferentes do padrão
          if (columnsName[i] == "comment") {
            $("#spaceToCreate div form table tbody tr").append("<td></td>");
            $(newData).addClass("align-top comments");

            $(newData).append("<textarea></textarea>");
            $(newData + " textarea").attr({
              "class" : "form-control",
              "type" : columnsType[i],
              "name" : columnsName[i],
              "maxlength" : "240",
              "id" : "comment"
            });

            $(newData).append("<span>240 Characters remaining</span>")
            $(newData + " span").attr({
              "id" : "char-remain",
              "style" : "font-size: 10px;"
            });
          } else {
            $("#spaceToCreate div form table tbody tr").append("<td></td>");
            $(newData).addClass("align-top");

            $(newData).append("<input></input>");
            $(newData + " input").attr({
              "class" : "form-control",
              "type" : columnsType[i],
              "name" : columnsName[i]
            }); }
            
          $("#spaceToCreate div form table tbody tr td:nth-child(3) input").attr({"step" : "0.01"});
        }
        comment = $("#comment")

        comment.on("keyup keypress change", function() {
            let comment = $("#comment");
            let maxlength = parseInt(comment.attr("maxlength"), 10);
            charCount = $(this).val().length;
            charRemain = maxlength - charCount;
            $("#char-remain").text(charRemain + " Characters remaining");
          });
      });

    

      
})