$(document).ajaxStart(function() { Pace.restart(); });

$('document').ready(function(){
    $('form').on('submit', function(e){
        e.preventDefault();
        console.log('123');
        if(validateData()==false)
        {
            window.alert("Nothing to search for.");
            return;
        }
        $.ajax({
            url: '/',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            },
        });
    });
});

function validateData()
{
    if($('#searchQuery').val().length === 0)
        return false;
    return true;
}
