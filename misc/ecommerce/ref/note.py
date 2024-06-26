#jquery validation after save just go back to list page

#    $(document).ready(function(){
# $("#contactform").validate();      

# var validator = $("#contactform").validate({

#      ignore: ":hidden",
#     rules: {
#         name: {
#             required: true,
#             minlength: 3
#         },
#         cognome: {
#             required: true,
#             minlength: 3
#         },
#         subject: {
#             required: true,

#         },



#         message: {
#             required: true,
#             minlength: 10
#         }
#     },

#     submitHandler: function(form) {



#    $("#contactform").submit(function(e){
#    e.preventDefault();
#       $.ajax({
#         url: form.attr("data-url"),
#         method: "POST",
#         data: formData,
#         headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
#         beforeSend: function () {
#           $(".send-now-button").text("Saving...");
#           $(".send-now-button").attr("disabled", true);
#         },
#         success: function (response) {
#           if (response.status == "success") {
#             $(".msg_desc").text(response.message);
#             $("#flash_message_success").attr("style", "display:block;");
#             setTimeout(function () {
#               $("#flash_message_success").attr("style", "display:none;");
#             }, 3500);
#             setTimeout(function () {
#               window.location.href = "/incentives/";
#             }, 2000);
#           } else {
    
#             $(".msg_desc").text(response.message);
#             $("#flash_message_error").attr("style", "display:block;");
#             setTimeout(function () {
#               $("#flash_message_error").attr("style", "display:none;");
#             }, 3500);
          
#         }
#         },
#         error: function (errors) {
#           console.log(errors);
#         },
#         complete: function () {
#           $(".send-now-button").attr("disabled", false);
#           $(".send-now-button").val("Save");
#         },
#       });
#     },

# });

#  });