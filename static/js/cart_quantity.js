// Получаем CSRF-токен из куки, так как Джанго требует защиту для POST-запросов
function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === 'csrftoken=') {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}


function sendCartUpdate(productId, newQuantity, inputField) {
    const url = `/cart/update/${productId}/`;
    
    fetch(url, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken()
        },
        body: new URLSearchParams({ 'quantity': newQuantity })
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => {

        inputField.value = newQuantity;

        const itemRow = inputField.closest('.cart-item');
        if (itemRow) {

            const currentItem = data.items.find(item => item.id == productId);
            if (currentItem) {

                const totalLine = itemRow.querySelector('.cart-total');
                if (totalLine) {
                    totalLine.textContent = `£${currentItem.total_price.toFixed(2)}`;
                }
            }
        }

        const globalTotalContainer = document.querySelector('.cart-summary .price, #cart-global-total');
        if (globalTotalContainer) {
            globalTotalContainer.textContent = `£${data.total_price.toFixed(2)}`;
        }

        const badge = document.querySelector('.cart-badge');
        if (badge) {
            badge.textContent = data.cart_length;
        }
    })
    .catch(error => console.error('Error updating cart:', error));
}

function decreaseQuantity(button) {
    const input = button.nextElementSibling;
    const productId = input.getAttribute('data-product-id');
    let currentValue = parseInt(input.value);
    
    if (currentValue > 1) {
        sendCartUpdate(productId, currentValue - 1, input);
    }
}

function increaseQuantity(button) {
    const input = button.previousElementSibling;
    const productId = input.getAttribute('data-product-id');
    let currentValue = parseInt(input.value);
    
    sendCartUpdate(productId, currentValue + 1, input);
}
