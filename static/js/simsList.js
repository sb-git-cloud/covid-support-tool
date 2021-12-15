var chartOutputResources;
const csrftoken = $("[name=csrfmiddlewaretoken]").val();

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function() {
    $(".delete_sim").click(function(e) {
        e.preventDefault();
        var tr = $(this).closest('tr')
        $.ajax({
            type: "DELETE",
            url: $(this).attr('href'),
            success: function(result) {
                tr.fadeOut(1000, function(){
                        $(this).remove();
                    });
                $('.success-div').each(function() {
                    $(this).show()
                    setTimeout(function() {
                        $('.success-div').each(function() {$(this).slideUp('medium')})
                        }, 1000);
                })
            },
            error: function(xhr, status, error) {
                $('.danger-div').each(function() {
                    var err = (xhr.responseText);
                    $(this).html(err.Message)
                    $(this).show()
                    setTimeout(function() {
                        $('.danger-div').each(function() {$(this).slideUp('slow')})
                        }, 5000);
                })
            }
        });
    })

});

// Enables all input forms and hides loading div after graphs have been updated
$(document).ajaxStop(function() {
    $('#inputdiv input').each(function() {
        $(this).prop( "disabled", false );
    })
    $(".loading-div").each(function() {
        $(this).hide()
    })
});

//$('.active').removeClass('active')
$('#id_navItemMySimulations').addClass("active");