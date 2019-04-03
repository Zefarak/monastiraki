
$('#gdpr_button').click(function (e) {
    e.preventDefault();
    $.ajax({
        url: '/gdpr/throw/ajax/',
        method: 'GET',
        success: function (data) {
            $('.gdpr_container').html(data.gdpr)
        }
    })
});