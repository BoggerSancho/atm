$(document).ready(function(){
    const CARD_NUM_LEN = 16;
    var inputValue = ''

    function formatCardNumber(){
        nonNumbers = "_".repeat(CARD_NUM_LEN - inputValue.length);
        rawString = nonNumbers + inputValue;
        $("#card-num-input").val(rawString.replace(/\W/gi, '').replace(/(.{4})/g, '$1-').slice(0, -1));
    };
    formatCardNumber();


    function formatCardPassword(){
        subs = "X".repeat(inputValue.length);
        $("#card-pass-input").val(subs);
    };

    $(".btn-ctrl").click(function(){
        if ($(this).val() != 'C' && $(this).val() != 'Enter' && inputValue.length < CARD_NUM_LEN) {
                inputValue += $(this).val();
                $("#card-num").val(inputValue);
            }
        if ($(this).val() == 'C') {
            inputValue = ''
        }
        $("#card-num-input").val(inputValue);
        formatCardNumber();
    });
});