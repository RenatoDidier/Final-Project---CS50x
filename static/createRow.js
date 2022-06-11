$(document).ready(function () {
    $("#createRow").on("click", function() { 
    
        /* Cada data da tabela possui o atributo name & type diferente entre si */
        let names = ["content", "type", "rate", "comment", "link"];
        let type = ["text", "text", "number", "text", "url"];
        
        let rowCreated = ".table tbody tr:last-child"
        let dataCreated = ".table tbody tr:last-child td:last-child"
        
        $(".table tbody").append("<tr></tr>");
        /* Criação de todos elementos do HTML e seus atributos */
        for (let i = 0; i < names.length; i++) {
            /* o TD comment possui elementos bem diversos das outras datas */
            if (names[i] == "comment") {
                $(rowCreated).append("<td></td>");

                $(dataCreated).addClass("align-top comments");
                $(dataCreated).append("<textarea></textarea>");
                $(dataCreated + " textarea").attr({
                    "class": "form-control",
                    "type": type[i],
                    "name": names[i],
                    "maxlength": "240",
                    "id": "comment"
                });
                $(dataCreated).append("<span>240 Characters remaining</span>");
                $(dataCreated + " span").attr({
                    "id": "char-remain",
                    "style": "font-size: 10px;"
                });
            } else {
                $(rowCreated).append("<td></td>");

                $(dataCreated).addClass("align-top");
                $(dataCreated).append("<input></input>");
                $(dataCreated + " input").attr({
                    "class": "form-control",
                    "type": type[i],
                    "name": names[i]
                });
            }
    
            $(".table tbody tr:last-child td:nth-child(3) input").attr({ "step": "0.01" });
        }

        $(".confirmRow").append("<button>Confirm</button>");
        $(".confirmRow button").attr({ "type": "submit", "class": "ms-auto btn btn-primary d-flex" });

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
