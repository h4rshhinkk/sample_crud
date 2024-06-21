$(document).ready(function() {
    $("#CategoryForm").validate({
        rules: {},
        messages: {},
        submitHandler: function(form, event) {
            event.preventDefault();
            var formData = $("#CategoryForm").serializeArray();
            var url = $("#form_url").val()
            $.ajax({
                url: url,
                headers: {
                    "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
                },
                method: "POST",
                data: formData,
                beforeSend: function() {
                    $("#category-submit").attr("disabled", "disabled");
                    $("#category-submit").val("Saving...");
                },
                success: function(response) {
                    if (response.status) {                        
                        $(".carousel__button").click()
                        FilterCategory('')
                        $(".msg_desc").text(response.message)
                        $("#flash_message_success").attr("style", "display:block;")
                        setTimeout(function() {
                            $("#flash_message_success").attr("style", "display:none;")
                        }, 3500)
                        location.reload();
                    } else {
                        alert('ho')
                        if ('message' in response ){
                            $(".carousel__button").click()
                            $(".msg_desc").text(response.message)
                            $("#flash_message_error").attr("style", "display:block;")
                            setTimeout(function() {
                                $("#flash_message_error").attr("style", "display:none;")
                            }, 3500)                                                       
                        } else {     
                            alert('form')                    
                            $('#category-form-div').html(response.template)     
                        } 
                    }                
                },
                complete: function() {
                    $("#category-submit").attr("disabled", false);
                    $("#category-submit").val("Save");
                },
            });
        },
    });

});

function FilterCategory(page) {
    if (page == '') {
        page = $('#current_page').val()
    }
    var url = $('#load_category').val()
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: { 'page': page },
        beforeSend: function() {},
        success: function(response) {
            $('#category-tbody').html(response.template)
            $('#category-pagination').html(response.pagination)
        },
    });
}

$(document).on('click', '#create_category', function(event) {
    event.preventDefault();
    var url = $(this).attr('data-url')
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function() {
            $('#category-form-div').html('Loading...')
        },
        success: function(response) {            
            $('#category-form-div').html(response.template)
            $('#popup_head').html(response.title)
            
        },
    });
})

$(document).on('click', '.category-edit', function(event) {
    event.preventDefault();
    var url = $(this).attr('data-url')
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function() {
            $('#category-form-div').html('Loading...')
        },
        success: function(response) {
            $('#category-form-div').html(response.template)
            $('#popup_head').html(response.title)
        },
    });
})


// Function to delete curriculum
function CategoryDelete(id) {
    var url = '/category/' + String(id) + '/delete/'
    swal({
        icon: "warning",
        title: "Verify Details",
        text: "Are you sure you want to delete this record?",
        buttons: true,
        dangerMode: true,
    }).then(function(okey) {
        if (okey) {
            $.ajax({
                url: url,
                headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
                method: "POST",
                data: {},
                beforeSend: function() {},
                success: function(response) {
                    if (response.status) {
                        $(".msg_desc").text(response.message);
                        $("#flash_message_success").attr("style", "display:block;");
                        setTimeout(function() {
                            $("#flash_message_success").attr("style", "display:none;");
                        }, 3500);
                        FilterCategory('')
                    }
                },
            });
        }
    });
}