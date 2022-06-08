$('.dropdown-toggle').dropdown()

$(document).ready(function() {
    let comment = $("#comment");
    let maxlength = parseInt(comment.attr("maxlength"), 10);
    let row = $("#createRow")
    let table = $("#createTable")
    
    row.on("click", function() {
      let names = ["content", "type", "rate", "comment", "link"]
      let type = ["text", "text", "number", "text", "url"]

      $(".confirmRow").append("<button>Confirm</button>");
      $(".confirmRow button").attr({"type" : "submit", "class" : "ms-auto btn btn-primary d-flex"});

      for (let i = 0; i < names.length; i++) {
        if (i == 3) {
          $(".newRow").append("<td></td>");
          $(".newRow td:last-child").addClass("align-top comments");
          $(".newRow td:last-child").append("<textarea></textarea>");
          $(".newRow td:last-child textarea").attr({
            "class" : "form-control",
            "type" : type[i],
            "name" : names[i],
            "maxlength" : "240",
            "id" : "comment"
          });
          $(".newRow td:last-child").append("<span>240 Characters remaining</span>")
          $(".newRow td:last-child span").attr({
            "class" : "char-remain",
            "style" : "font-size: 10px;"
          });
        } else {
          $(".newRow").append("<td></td>");
          $(".newRow td:last-child").addClass("align-top");
          $(".newRow td:last-child").append("<input></input>");
          $(".newRow td:last-child input").attr({
            "class" : "form-control",
            "type" : type[i],
            "name" : names[i]
          }); }
          
        $(".newRow td:nth-child(3) input").attr({"step" : "0.01"});
        }    
      });

      comment.on("keyup keypress change", function() {
        charCount = $(this).val().length;
        charRemain = maxlength - charCount;
        $(".char-remain").text(charRemain + " Characters remaining");
      });

      table.on("click", function() {
        let columns = ["content", "type", "rate", "comment", "link"]
        let type = ["text", "text", "number", "text", "url"]
        let newTable = ".content div form table"
        let newBody = ".content div form table tbody tr"
        let cols = ["2", "1", "1", "7", "1"]

        $(".content").prepend("<div></div>");
        $(".content div").append("<form></form>");
        $(".content div form").append("<span>Title:</span><input></input>");
        $(".content div form").append("<table></table>");
        $(".content div form").append("<span></span>")
        $(".content div form span:last-child").append("<button>Confirm</button>")

        $(".content div form").attr({"method" : "post", "action" : "/mylist"});
        $(newTable).attr({"class" : "table rounded"});
        $(".content div form input").attr({"type" : "text", "name" : "table_name"});
        $(".content div form span button").attr({"type" : "submit", "class" : "ms-auto btn btn-primary d-flex"});
        

        $(newTable).append("<thead></thead>")
        $(newTable).append("<tbody></tbody>")

        $(newTable + " thead").append("<tr></tr>")
        $(newTable + " tbody").append("<tr></tr>")

        for (let i = 0; i < columns.length; i++) {
          $(newTable + " thead" + " tr").append("<th>" + columns[i] + "</th>")
          $(newTable + " thead" + " tr" + " th:last-child").attr({"class" : "col-" + cols[i], "scope" : "col"})
        }

        for (let i = 0; i < columns.length; i++) {
          if (i == 3) {
            $(newBody).append("<td></td>");
            $(newBody + " td:last-child").addClass("align-top comments");
            $(newBody + " td:last-child").append("<textarea></textarea>");
            $(newBody + " td:last-child textarea").attr({
              "class" : "form-control",
              "type" : type[i],
              "name" : columns[i],
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
              "type" : type[i],
              "name" : columns[i]
            }); }
            
          $(newBody + " td:nth-child(3) input").attr({"step" : "0.01"});
        }
      });

            
});

