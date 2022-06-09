comment.on("keyup keypress change", function() {
    let comment = $("textarea");
    let maxlength = parseInt(comment.attr("maxlength"), 10);
    charCount = $(this).val().length;
    charRemain = maxlength - charCount;
    $(".char-remain").text(charRemain + " Characters remaining");
  });