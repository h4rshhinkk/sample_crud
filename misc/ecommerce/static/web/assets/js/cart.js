$(document).ready(function () {

    // Event listener for add cart button click
    $(".btn-addtocart").click(function () {
        var product_Id = $(this).siblings('input[name="product_id"]').val();
        var url = "/shop/cart/add/?product_id=" + product_Id;

        console.log(url);
        $.ajax({
            type: "GET",
            url: url,

            success: function (data) {
                console.log("success", data);
                window.location.href = '/shop/cart/';
            },
            error: function (data) {
                if (data.status == '401') {
                    window.location.href = '/accounts/login/';
                } else {
                    // Display error message with SweetAlert
                    console.log(data);
                }
            }
        });
    });
});