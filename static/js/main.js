$(document).ajaxStart(function() { Pace.restart(); console.log('Pace restart.')});

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
    $('#nlp-section').fadeIn(300);
});

$('document').ready(function(){
    $('#content-item-url').click(function(){
        $('#content-type').val('url');
        $('#content-type').html('URL');
    });
    $('#content-item-raw').click(function(){
        $('#content-type').val('raw');
        $('#content-type').html('Raw Text');
    });
});

$('document').ready(function(){
    $('li').quickfit(min=16);
});
$('document').ready(function(){
    $('form').on('submit', function(e){
        e.preventDefault();
        if(validateData()==false)
        {
            window.alert("Make sure the search box and the dropdown both have been filled in.");
            return;
        }
        Pace.track(function(){
            var raw = {
                searchQuery: $('#searchQuery').val(),
                contentType: $('#content-type').val()
            };
            var data = JSON.stringify(raw);
            $.ajax({
                global: true,
                url: '/',
                data: data,
                dataType: "json",
                type: 'POST',
                success: function(response) {
                    var parsed_json = response;
                    var scrapingModuleHtml = scrapingModule(raw.contentType, parsed_json);
                    $('#scraping-module').append(scrapingModuleHtml);
                    $('#elapsedTimeJudgment').html(parsed_json.elapsedTimeJudgment);
                    $('#elapsedTimeCategorizing').html(parsed_json.elapsedTimeCategorizing);
                    $('#elapsedTimeFeatures').html(parsed_json.elapsedTimeFeatures);
                    $('#elapsedTimeNewsAPI').html(parsed_json.elapsedTimeNewsAPI);
                    $('#elapsedTimeSimilarity').html(parsed_json.elapsedTimeSimilarity);
                    $('#totalExecutionTime').html(parsed_json.totalExecutionTime);
                    $('#sentimentScore').html(parsed_json.sentimentScore['sentiment_score']);
                    $('#sentimentMagnitude').html(parsed_json.sentimentScore['sentiment_magnitude']);

                    var articleCategories = parsed_json.articleCategories;
                    $.each(articleCategories,function(index, entry){
                        currentCategoryName = entry['category'];
                        currentCategoryConfidence = entry['confidence'];
                        refactoredHTMLContent = make_html_for_category(currentCategoryName, currentCategoryConfidence);
                        $('#categorizing-module').append(refactoredHTMLContent);
                    });

                    var articleEntities = parsed_json.articleEntities;
                    $.each(articleEntities, function(index, entry){
                        currentEntityText = entry['text'];
                        currentEntityLabel = entry['label'];
                        currentEntityDescription = entry['description'];
                        refactoredHTMLContent = make_html_for_entity(index, currentEntityText, currentEntityLabel, currentEntityDescription);
                        $('#articleEntities').append(refactoredHTMLContent);
                    });

                    fetchNews(parsed_json.newsSources, parsed_json.similarityFactors);
                },
                error: function(error) {
                    console.log(error);
                },
            });
        });
    });
});

function fetchNews(labels, data)
{
    console.log(labels);
    console.log(data);
    var ctx = document.getElementById('fetch-news').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Similarity %\'s',
                data: data,
                backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function validateData()
{
    if($('#searchQuery').val().length === 0 || $('#content-type').val() == "null")
        return false;
    return true;
}

function scrapingModule(contentType, response)
{
    var scrapingModuleHtml = "";
    if (contentType == "raw")
        scrapingModuleHtml = make_html_for_scrapingModuleRaw(response.elapsedTimeScraping, response.articleContent, response.articleContentJudgment['result'], response.articleContentJudgment['score']);
    if (contentType == "url")
        scrapingModuleHtml = make_html_for_scrapingModuleUrl(response.elapsedTimeScraping, response.newsURL, response.articleTitle, response.articleContent, response.articleTitleJudgment['result'], response.articleTitleJudgment['score'], response.articleContentJudgment['result'], response.articleContentJudgment['score']);
    return scrapingModuleHtml;
}


function make_html_for_scrapingModuleRaw(elapsedTimeScraping, articleContent, articleContentResult, articleContentScore)
{
    return '<p>Time taken for Scraping = <strong id="elapsedTimeScraping">'+elapsedTimeScraping+'</strong></p>' +
    '<!-- Article Content -->' +
    '<h4>Article Content</h4>' +
    '<div class="alert alert-info" role="alert">' +
    articleContentResult +
    '<br>' +
    'Score: ' + articleContentScore +
    '</div>' +
    '<pre><code class="plaintext hljs" id="articleContent">'+articleContent+'</code></pre>';
}

function make_html_for_scrapingModuleUrl(elapsedTimeScraping, newsURL, articleTitle, articleContent, articleTitleResult, articleTitleScore, articleContentResult, articleContentScore)
{
    return  '<p>Time taken for Scraping = <strong id="elapsedTimeScraping">'+elapsedTimeScraping+'</strong></p>' +
    '<h4>URL Input</h4>' +
    '<pre><code class="plaintext hljs" id="newsURL">'+newsURL+'</code></pre>' +
    '<!-- Article Title -->' +
    '<h4>Article Title</h4>' +
    '<div class="alert alert-info" role="alert" id="articleTitleJudgment">' +
    articleTitleResult +
    '<br>' +
    'Score: ' + articleTitleScore +
    '</div>' +
    '<pre><code class="plaintext hljs" id="articleTitle">'+articleTitle+'</code></pre>' +
    '<!-- Article Content -->' +
    '<h4>Scraped Article Content</h4>' +
    '<div class="alert alert-info" role="alert">' +
    articleContentResult +
    '<br>' +
    'Score: ' + articleContentScore +
    '</div>' +
    '<pre><code class="plaintext hljs" id="articleContent">'+articleContent+'</code></pre>';
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