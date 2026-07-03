
document.addEventListener('DOMContentLoaded', function () {
    const sideCart = document.getElementById('side-cart');
    const overlay = document.getElementById('sidebar-overlay');
    const openCartBtn = document.getElementById('open-cart-btn');
    const closeCartBtn = document.getElementById('close-cart-btn');
    const sideCartItems = document.getElementById('side-cart-items');
    const sideCartTotal = document.getElementById('side-cart-total');
    const navCartBadge = document.getElementById('nav-cart-badge');

    function openCart() {
        if (sideCart && overlay) {
            sideCart.classList.add('open');
            overlay.classList.add('show');
        }
    }

    function closeCart() {
        if (sideCart && overlay) {
            sideCart.classList.remove('open');
            overlay.classList.remove('show');
        }
    }

    if (openCartBtn) openCartBtn.addEventListener('click', openCart);
    if (closeCartBtn) closeCartBtn.addEventListener('click', closeCart);
    if (overlay) overlay.addEventListener('click', closeCart);

    document.querySelectorAll('.ajax-add-to-cart-form').forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const url = this.getAttribute('action');
            const formData = new FormData(this);

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Server error');
                }
                return response.json();
            })
            .then(data => {
                updateCartUI(data);
                openCart();
            })
            .catch(error => console.error('Error adding to cart:', error));
        });
    });

    function updateCartUI(data) {

        if (navCartBadge) {
            if (data.cart_length > 0) {
                navCartBadge.innerText = data.cart_length;
                navCartBadge.style.display = 'inline-block';
            } else {
                navCartBadge.style.display = 'none';
            }
        }

        const cartHeaderTitle = document.querySelector('#side-cart h5');
        if (cartHeaderTitle) {
            cartHeaderTitle.innerText = `Your Cart (${data.cart_length})`;
        }

        if (sideCartTotal) {
            sideCartTotal.innerText = `£${data.total_price.toFixed(2)}`;
        }

        if (!sideCartItems) return;

        sideCartItems.innerHTML = '';
        if (data.items.length === 0) {
            sideCartItems.innerHTML = '<p class="text-muted text-center py-4">Your cart is empty</p>';
            return;
        }

        data.items.forEach(item => {
            const itemHtml = `
                <div class="side-cart-item align-items-center" id="side-item-${item.id}">
                    <img src="${item.image_url || '/static/placeholder.png'}" class="side-cart-img" alt="${item.name}">
                    <div class="flex-grow-1">
                        <h6 class="m-0 mb-1" style="font-size: 0.95rem; font-weight: 600;">${item.name}</h6>
                        <small class="text-muted d-block mb-2">by ${item.author}</small>

                        <div class="d-flex justify-content-between align-items-center gap-2">
                            <span style="font-size: 0.9rem; color: #8ecf99; font-weight: 500;">
                                ${item.quantity} × £${item.price.toFixed(2)}
                            </span>

                            <button class="btn btn-custom-danger btn-sm ajax-remove-btn"
                                    data-product-id="${item.id}"
                                    style="padding: 2px 10px; font-size: 0.8rem; border-radius: 8px;">
                                Remove
                            </button>
                        </div>
                    </div>
                </div>
            `;
            sideCartItems.insertAdjacentHTML('beforeend', itemHtml);
        });

        document.querySelectorAll('.ajax-remove-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const productId = this.getAttribute('data-product-id');
                removeProductFromCart(productId);
            });
        });
    }

    function removeProductFromCart(productId) {
        const url = `/cart/remove/${productId}/`;
        const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
        if (!csrfInput) return;

        const csrftoken = csrfInput.value;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Error removing item');
            return response.json();
        })
        .then(data => {
            updateCartUI(data);
        })
        .catch(error => console.error('Error removing from cart:', error));
    }
});
