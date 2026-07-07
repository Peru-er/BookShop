
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.wishlist-toggle').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();

            const productId = this.getAttribute('data-product-id');
            const icon = this.querySelector('.wishlist-icon');
            const url = `/users/wishlist/toggle/${productId}/`;

            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    if (data.wished) {
                        icon.setAttribute('fill', '#6d3232');
                        icon.style.transform = 'scale(1.2)';
                        setTimeout(() => icon.style.transform = 'scale(1)', 200);
                    } else {
                        if (item.classList.contains('m-2')) {
                            icon.setAttribute('fill', 'rgba(255, 255, 255, 0.8)');
                        } else {
                            icon.setAttribute('fill', '#6c757d');
                        }
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
