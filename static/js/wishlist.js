
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-product-id]').forEach(item => {
        if (!item.classList.contains('wishlist-toggle') && !item.classList.contains('profile-wishlist-toggle')) return;

        item.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();

            const productId = this.getAttribute('data-product-id');
            const icon = this.querySelector('.wishlist-icon');
            const url = `/users/wishlist/toggle/${productId}/`;

            const itemContainer = document.getElementById(`wishlist-item-${productId}`) || item.closest('.target-wishlist-card');

            if (itemContainer) {
                itemContainer.style.opacity = '0';
                itemContainer.style.transform = 'scale(0.8)';
                itemContainer.style.transition = 'all 0.3s ease';
                setTimeout(() => {
                    itemContainer.remove();

                    const remainingItems = document.querySelectorAll('#wishlist-pane .book-item-container');
                    if (remainingItems.length === 0 && document.getElementById('wishlist-pane')) {
                        location.reload();
                    }
                }, 300);
            }

            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    if (icon) {
                        if (data.wished) {
                            icon.setAttribute('fill', '#6d3232');
                        } else {
                            if (item.classList.contains('m-2')) {
                                icon.setAttribute('fill', 'rgba(255, 255, 255, 0.8)');
                            } else {
                                icon.setAttribute('fill', '#6c757d');
                            }
                        }
                    }

                    if (data.message) {
                        createDynamicFlash(data.message);
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    const tabButtons = document.querySelectorAll('#profileTabs button[data-bs-toggle="tab"]');
    tabButtons.forEach(button => {
        button.addEventListener('hide.bs.tab', () => {
            const scrollPos = window.scrollY;
            requestAnimationFrame(() => {
                window.scrollTo(0, scrollPos);
            });
        });
    });

    function createDynamicFlash(messageText) {
        let container = document.querySelector('.flashes');
        if (!container) {
            container = document.createElement('div');
            container.className = 'flashes';
            const mainContainer = document.querySelector('main.container');
            if (mainContainer) {
                const breadcrumbs = mainContainer.querySelector('nav[aria-label="breadcrumb"]');
                if (breadcrumbs) {
                    breadcrumbs.after(container);
                } else {
                    mainContainer.prepend(container);
                }
            } else {
                document.body.appendChild(container);
            }
        }

        const flash = document.createElement('div');
        flash.className = 'flash success';
        flash.innerText = messageText;

        container.appendChild(flash);

        requestAnimationFrame(() => {
            flash.classList.add('flash-visible');
        });

        const timer = setTimeout(() => {
            removeDynamicFlash(flash);
        }, 4000);

        flash.addEventListener('click', () => {
            clearTimeout(timer);
            removeDynamicFlash(flash);
        });
    }

    function removeDynamicFlash(flash) {
        flash.classList.remove('flash-visible');
        flash.classList.add('flash-hide');
        flash.addEventListener('transitionend', () => {
            flash.remove();
        }, { once: true });
    }
});
