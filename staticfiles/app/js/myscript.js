$(document).ready(function() {

    function updateCart(url, id, eml) {
        console.log("Making AJAX request to:", url); // Debugging
        $.ajax({
            type: "GET",
            url: url,
            data: { prod_id: id },
            success: function(data) {
                console.log("AJAX success:", data); // Debugging

                // Update amount and total amount
                $('#amount').text(data.amount);
                $('#totalamount').text(data.totalamount);

                // Update quantity or remove item from DOM
                if (data.quantity !== undefined) {
                    console.log("Updating quantity for product ID:", id); // Debugging
                    if (data.quantity <= 0) {
                        console.log("Removing item from cart:", eml); // Debugging
                        $(eml).closest('.row.mb-3').remove();
                    } else {
                        $(eml).text(data.quantity);
                    }
                }

                // Check if cart is empty and update DOM
                if (data.amount === 0) {
                    console.log("Cart is empty, updating DOM"); // Debugging
                    $('.card').remove(); // This removes the entire card; modify if necessary
                    $('.container.my-5').html('<h1 class="text-center mb-5">Cart is Empty</h1>');
                }
            },
            error: function(xhr, status, error) {
                console.error("AJAX error:", status, error); // Debugging
            }
        });
    }

    $('.plus-cart').click(function() {
        var id = $(this).attr("pid").toString();
        var eml = $(this).siblings('.cart-quantity')[0];
        updateCart("/pluscart", id, eml);
    });

    $('.minus-cart').click(function() {
        var id = $(this).attr("pid").toString();
        var eml = $(this).siblings('.cart-quantity')[0];
        updateCart("/minuscart", id, eml);
    });

    $('.remove-cart').click(function() {
        var id = $(this).attr("pid").toString();
        var eml = $(this).closest('.row.mb-3');

        $.ajax({
            type: "GET",
            url: "/removecart",
            data: { prod_id: id },
            success: function(data) {
                console.log("Remove item AJAX success:", data); // Debugging

                // Update the displayed amounts
                $('#amount').text(data.amount);
                $('#totalamount').text(data.totalamount);

                // Remove the item from the DOM
                eml.remove();

                // If cart is empty, update the DOM accordingly
                if (data.amount === 0) {
                    console.log("Cart is empty after removal"); // Debugging
                    $('.card').remove(); // This removes the entire card; adjust if necessary
                    $('.container.my-5').html('<h1 class="text-center mb-5">Cart is Empty</h1>');
                }
            },
            error: function(xhr, status, error) {
                console.error("Remove item AJAX error:", status, error); // Debugging
            }
        });
    });
});
$(document).on('click', '.plus-wishlist', function(){
    var id = $(this).data("pid").toString();
    $.ajax({
        type: "GET",
        url: "/pluswishlist",
        data: {
            prod_id: id
        },
        success: function(data) {
            // Handle the response, e.g., updating the UI or redirecting
            window.location.href = `/product-detail/${id}`;
        },
        error: function(xhr, status, error) {
            console.error("An error occurred while adding to the wishlist: ", error);
        }
    });
});

$(document).on('click', '.minus-wishlist', function(){
    var id = $(this).data("pid").toString();
    $.ajax({
        type: "GET",
        url: "/minuswishlist",
        data: {
            prod_id: id
        },
        success: function(data) {
            // Handle the response, e.g., updating the UI or redirecting
            window.location.href = `/product-detail/${id}`;
        },
        error: function(xhr, status, error) {
            console.error("An error occurred while removing from the wishlist: ", error);
        }
    });
});
