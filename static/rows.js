$(document).ready(function () {
    $("#createRow").on("click", function() { 
    
        let names = ["content", "type", "rate", "comment", "link"];
        let type = ["text", "text", "number", "text", "url"];
    
        $(".confirmRow").append("<button>Confirm</button>");
        $(".confirmRow button").attr({ "type": "submit", "class": "ms-auto btn btn-primary d-flex" });
        $(".table tbody").append("<tr></tr>");
    
        for (let i = 0; i < names.length; i++) {
            if (names[i] == "comment") {
                $(".table tbody tr:last-child").append("<td></td>");
                $(".table tbody tr:last-child td:last-child").addClass("align-top comments");
                $(".table tbody tr:last-child td:last-child").append("<textarea></textarea>");
                $(".table tbody tr:last-child td:last-child textarea").attr({
                    "class": "form-control",
                    "type": type[i],
                    "name": names[i],
                    "maxlength": "240",
                    "id": "comment"
                });
                $(".table tbody tr:last-child td:last-child").append("<span>240 Characters remaining</span>");
                $(".table tbody tr:last-child td:last-child span").attr({
                    "class": "char-remain",
                    "style": "font-size: 10px;"
                });
            } else {
                $(".table tbody tr:last-child").append("<td></td>");
                $(".table tbody tr:last-child td:last-child").addClass("align-top");
                $(".table tbody tr:last-child td:last-child").append("<input></input>");
                $(".table tbody tr:last-child td:last-child input").attr({
                    "class": "form-control",
                    "type": type[i],
                    "name": names[i]
                });
            }
    
            $(".table tbody tr:last-child td:nth-child(3) input").attr({ "step": "0.01" });
        }
    
    });     
})

$("#dropdownMenuButton1").dropdown();