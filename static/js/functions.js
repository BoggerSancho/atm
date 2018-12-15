function showFlashMessage(message){
    var template =  "<div class='container-alert-flash'>"+
                    "<div class='col-sm-3 col-sm-offset-6'>"+
                    "<div class='alert alert-danger'>"+
                    message+
                    "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>"+
                    "<span aria-hidden='true'>&times;</span>"
                    "</button>"+
                    "</div></div></div>"
    $("body").append(template);
    $(".container-alert-flash").fadeIn();
    setTimeout(function(){
        $(".container-alert-flash").fadeOut();
    }, 4000)
}