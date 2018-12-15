$(document).ready(function(){
    const CARD_PASS_LEN = 4;
    var inputValue = ''

    $(".btn-ctrl").click(function(){
        if ($(this).val() != 'C' && $(this).val() != 'Enter') {
            inputValue += $(this).val();
        }
        if ($(this).val() == 'C') {
            inputValue = ''
        }
        $("#card-cash-input").val(inputValue);
        $("#card-cash").val(inputValue);
    });
});