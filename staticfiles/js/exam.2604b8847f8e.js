$(document).ready(function(){
    if ($.cookie("timer_cook")){
        runTimer($.cookie("timer_cook"), $.cookie("examEndpointUrl"), $.cookie("userId"), $.cookie("examId"));
    }
});

function runTimer(timeLeft, url, userId, examId){
    setInterval(function() {
        timeLeft = timeLeft - 1;
        $.cookie("timer_cook", timeLeft, {path: '/'});
        var hours = Math.floor(timeLeft / 3600) % 3600;
        var minutes = Math.floor(timeLeft / 60) % 60;
        var seconds = timeLeft % 60;
        $("#demo").text(hours + "h " + minutes + "m " + seconds + "s ");
        if (timeLeft < 1) {
            $.removeCookie("timer_cook");
            $.removeCookie("userId");
            $.removeCookie("examId");
            $.removeCookie("examEndpointUrl");
            data = {
                'user' : userId,
                'quiz' : examId
            }
            $.ajax({
                headers:{"X-CSRFToken": $.cookie('csrftoken')},
                data: data,
                method: "PUT",
                url: url,
                success: function(){
                    location.href = '/';
                },
                error: function(data){
                    console.log("error");
                    console.log(data);
                }
            });
        }
    }, 1000);
};


function createExamForUser(userId, examId, answerCreateUrl, examEndpointUrl, examStartUrl, questionListUrl){
    var nextQuestionUrl;
    var questionId;
    var answerId;
    var csrftoken = getCookie('csrftoken');

    function makeAjaxGETRequestForQuestion(url){
        $.ajax({
            method: "GET",
            url: url,
            success: function(data){
                nextQuestionUrl = data.next;
                firstQuestion = data.results[0];
                parseQuestion(firstQuestion);
            },
            error: function(data){
                console.log("error");
                console.log(data);
            }
        });
    }


    function parseQuestion(data){
        var htmlText;
        var questionTitle = data.title;
        var questionOptions = data.options;
        var questionId = data.id;
        var questionImage = data.image;
        var quizId = examId;
        htmlText =  '<form action="." method="POST">' +
                    '<input type="hidden" name="quizId" value="' + quizId + '">' +
                    '<input type="hidden" name="questionId" value="' + questionId + '">' +
                    '<p>' + questionTitle + '</p>'
        if (questionImage) {
            htmlText += '<p>' + '<img class="img-responsive img-question" src="' + questionImage + '">' + '</p>'
        }
        $.each(questionOptions, function(key, value){
            var optionId = value.id
            var optionTitle = value.title
            htmlText += '<input type="radio" name="optionId" value="' + optionId + '">' + optionTitle + '<br/>'
        });
        htmlText += '<input type="submit" class="btn btn-default" id="btn-confirm" value="Next" disabled></form>'
        $("#exam-question").empty();
        $("#exam-question").html(htmlText)
    }


    $(document).on('change', 'input:radio', function(){
        answerId = $(this).attr("value");
        $("#btn-confirm").prop("disabled", false);
    });


    $(document).on('click', '#btn-confirm', function(event){
        event.preventDefault();
        var this_ = $(this)
        var form = this_.parent();
        var formData = form.serialize();
        $.ajax({
            method: "POST",
            headers:{"X-CSRFToken": csrftoken},
            url: answerCreateUrl,
            data: formData,
            success: function(data){
                console.log(data);
            },
            error: function(data){
                console.log("error");
                console.log(data);
            }
        });

        if (nextQuestionUrl) {
            makeAjaxGETRequestForQuestion(nextQuestionUrl)
        } else {
            url = examEndpointUrl
            data = {
                'user' : userId,
                'quiz' : examId
            }
            $.ajax({
                headers:{"X-CSRFToken": csrftoken},
                data: data,
                method: "PUT",
                url: url,
                success: function(){
                    location.href = '/';
                },
                error: function(data){
                    console.log("error");
                    console.log(data);
                }
            });
        }
    });


    $("#start-exam").click(function(event){
        event.preventDefault();
        $(this).hide();
        $.ajax({
            headers:{"X-CSRFToken": csrftoken},
            method: "POST",
            url: examStartUrl,
            success: function(data){
                if (data.timer && !($.cookie("timer_cook"))){
                    $.cookie("userId", userId, {path: '/'});
                    $.cookie("examId", examId, {path: '/'});
                    $.cookie("examEndpointUrl", examEndpointUrl, {path: '/'});
                    $.cookie("timer_cook", data.timer, {path: '/'});
                    runTimer($.cookie("timer_cook"), examEndpointUrl, userId, examId);
                }
            },
            error: function(data){
                console.log("error");
                console.log(data);
            }
        });
        var url = questionListUrl;
        makeAjaxGETRequestForQuestion(url);
    });
};

if ($.cookie("timer_cook")){
    runTimer($.cookie("timer_cook"), $.cookie("examEndpointUrl"), $.cookie("userId"), $.cookie("examId"));
}
