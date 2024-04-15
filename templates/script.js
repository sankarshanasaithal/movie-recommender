$(document).ready(function() {
    $('#suggestions').hide();
    $('#movie_name').on('input', function() {
        var inputText = $(this).val().trim();
        if (inputText.length > 0) {
            $.ajax({
                url: '/suggest',
                method: 'POST',
                data: {input_text: inputText},
                success: function(response) {
                    var suggestions = response.split('\n');
                    var dropdown = $('#suggestions');
                    dropdown.empty();
                    for (var i = 0; i < suggestions.length; i++) {
                        dropdown.append($('<div>').attr({
                            'class':'name',
                            'tabindex':'0'
                        }).text(suggestions[i]));
                    }
                    $('#suggestions').show();
                    document.getElementById('suggestions').addEventListener('click', function(event) {
                        if (event.target.classList.contains('name')){
                            var divText = event.target.textContent; // Get text content of the clicked div
                            if(divText!==""){
                                document.getElementById('movie_name').value = divText; // Set input field value to the div text
                                $('#suggestions').hide();
                            }
                        }
                    });
                }
            });
        } else {
            $('#suggestions').hide();
        }
    });
});