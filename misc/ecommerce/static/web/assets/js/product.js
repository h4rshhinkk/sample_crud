$(document).ready(function() {
    $("#ProductForm").validate({
        rules: {},
        messages: {},
        submitHandler: function(form, event) {
            event.preventDefault();
            var formData = $("#ProductForm").serializeArray();
            var url = $("#form_url").val()
            $.ajax({
                url: url,
                headers: {
                    "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
                },
                method: "POST",
                data: formData,
                beforeSend: function() {
                    $("#product-submit").attr("disabled", "disabled");
                    $("#product-submit").val("Saving...");
                },
                success: function(response) {
                    if (response.status) {                        
                        $(".carousel__button").click()
                        FilterProduct('')
                        $(".msg_desc").text(response.message)
                        $("#flash_message_success").attr("style", "display:block;")
                        setTimeout(function() {
                            $("#flash_message_success").attr("style", "display:none;")
                        }, 3500)
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
                            $('#product-form-div').html(response.template)     
                        } 
                    }                
                },
                complete: function() {
                    $("#product-submit").attr("disabled", false);
                    $("#product-submit").val("Save");
                },
            });
        },
    });

});

function FilterProduct(page) {
    if (page == '') {
        page = $('#current_page').val()
    }
    var url = $('#load_product').val()
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: { 'page': page },
        beforeSend: function() {},
        success: function(response) {
            $('#product-tbody').html(response.template)
            $('#product-pagination').html(response.pagination)
        },
    });
}

$(document).on('click', '#create_product', function(event) {
    event.preventDefault();
    var url = $(this).attr('data-url')
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function() {
            $('#product-form-div').html('Loading...')
        },
        success: function(response) {            
            $('#product-form-div').html(response.template)
            $('#popup_head').html(response.title)
        },
    });
})


function ProductDelete(id) {
    var url = '/product/' + String(id) + '/delete/'
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
                        FilterProduct('')
                        location.reload();
                    }
                },
            });
        }
    });
}