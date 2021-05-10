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
                    $('#elapsedTimeScraping').html(parsed_json.elapsedTimeScraping);
                    $('#elapsedTimeCategorizing').html(parsed_json.elapsedTimeCategorizing);
                    $('#elapsedTimeFeatures').html(parsed_json.elapsedTimeFeatures);
                    $('#elapsedTimeNewsAPI').html(parsed_json.elapsedTimeNewsAPI);
                    $('#totalExecutionTime').html(parsed_json.totalExecutionTime);
                    $('#newsURL').html(parsed_json.newsURL);
                    $('#articleTitle').html(parsed_json.articleTitle);
                    $('#articleContent').html(parsed_json.articleContent);
                    $('#sentimentScore').html(parsed_json.sentimentScore['sentiment_score']);
                    $('#sentimentMagnitude').html(parsed_json.sentimentScore['sentiment_magnitude']);

                    var articleCategories = parsed_json.articleCategories;
                    $.each(articleCategories,function(index, entry){
                        currentCategoryName = entry['category'];
                        currentCategoryConfidence = entry['confidence'];
                        refactoredHTMLContent = make_html_for_category(currentCategoryName, currentCategoryConfidence);
                        $('#articleCategories').append(refactoredHTMLContent);
                    });

                    var articleEntities = parsed_json.articleEntities;
                    $.each(articleEntities, function(index, entry){
                        currentEntityText = entry['text'];
                        currentEntityLabel = entry['label'];
                        currentEntityDescription = entry['description'];
                        refactoredHTMLContent = make_html_for_entity(index, currentEntityText, currentEntityLabel, currentEntityDescription);
                        $('#articleEntities').append(refactoredHTMLContent);
                    });
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

function make_html_for_category(category, confidence)
{
    return '<pre><code class="plaintext hljs">'+category+
    '<br/>' +
    'Confidence: ' + confidence +
    '</code></pre>';
}


function make_html_for_entity(serialNumber, text, label, description)
{
    return '<tr>' +
              '<td>'+serialNumber+'</td>' +
              '<td>'+text+'</td>' +
              '<td>'+label+'</td>' +
              '<td>'+description+'</td>' +
            '</tr>';
}