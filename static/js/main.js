$(document).ajaxStart(function() { Pace.restart(); console.log('hello')});

Pace.on("done", function(){
    console.log("pace stops.");
    // $('.page_overlay').css("display", "hidden");
    $('.page_overlay').delay(300).fadeOut(600);
    // $(".nlp-section").fadeIn(300);
});

Pace.on("start", function(){
    console.log("Pace starts.")
    // $('.page_overlay').show();
    // $('.page_overlay').css("display", "none");
    $('.page_overlay').delay(50).fadeIn(150);
    $('.nlp-section').fadeIn(300);
});

$('document').ready(function(){
    $('form').on('submit', function(e){
        e.preventDefault();
        console.log('123');
        if(validateData()==false)
        {
            window.alert("Nothing to search for.");
            return;
        }
        Pace.track(function(){
            $.ajax({
                global: true,
                url: '/',
                data: $('form').serialize(),
                type: 'POST',
                success: function(response) {
                    console.log(response);
                    var parsed_json = JSON.parse(response);
                    $('#newsURL').html(parsed_json.newsURL);
                    $('#articleTitle').html(parsed_json.articleTitle);
                    $('#articleContent').html(parsed_json.articleContent);
                },
                error: function(error) {
                    console.log(error);
                },
            });
        });
    });
});

function validateData()
{
    if($('#searchQuery').val().length === 0)
        return false;
    return true;
}
