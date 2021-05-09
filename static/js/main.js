$('document').ready(function(){
    $('#search').on('keypress', function(e){
        if(e.which == 13)
            $('#search').click();
    });
    $('#searchQuery').on('keypress', function(e){
        if(e.which == 13)
            $('#search').click();
    });
    $('#search').on('click', function(e){
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
            }
        });
    });
});

function validateData()
{
    if($('#searchQuery').val().length === 0)
        return false;
    return true;
}