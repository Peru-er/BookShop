
document.addEventListener("DOMContentLoaded", function() {

    const searchInput = document.getElementById('search-input');
    const clearBtn = document.getElementById('search-clear-btn');
    const searchForm = document.getElementById('search-form');
        const wrappers = document.querySelectorAll('.slider-wrapper');

    wrappers.forEach(wrapper => {
        const container = wrapper.querySelector('.books-scroll-container');
        const leftArrow = wrapper.querySelector('.left-arrow');
        const rightArrow = wrapper.querySelector('.right-arrow');

        if (!container || !leftArrow || !rightArrow) return;

        const scrollStep = (240 + 16) * 2;

        function updateArrowState() {
            const scrollLeft = Math.ceil(container.scrollLeft);
            const maxScrollLeft = container.scrollWidth - container.clientWidth;

            if (scrollLeft <= 0) {
                leftArrow.classList.add('disabled');
                leftArrow.setAttribute('disabled', 'true');
            } else {
                leftArrow.classList.remove('disabled');
                leftArrow.removeAttribute('disabled');
            }

            if (scrollLeft >= maxScrollLeft - 2) {
                rightArrow.classList.add('disabled');
                rightArrow.setAttribute('disabled', 'true');
            } else {
                rightArrow.classList.remove('disabled');
                rightArrow.removeAttribute('disabled');
            }
        }

        leftArrow.addEventListener('click', () => {
            container.scrollLeft -= scrollStep;
        });

        rightArrow.addEventListener('click', () => {
            container.scrollLeft += scrollStep;
        });

        container.addEventListener('scroll', updateArrowState);

        window.addEventListener('resize', updateArrowState);
        setTimeout(updateArrowState, 300);
    });

    if (searchInput && clearBtn) {

        searchInput.addEventListener('input', function() {
            if (this.value.trim().length > 0) {
                clearBtn.style.display = 'inline-flex';
            } else {
                clearBtn.style.display = 'none';
            }
        });

        clearBtn.addEventListener('click', function() {
            searchInput.value = '';
            clearBtn.style.display = 'none';
            searchInput.focus();

            if (window.location.search.includes('q=')) {
                searchForm.submit();
            }
        });
    }

    function switchProfileTab(targetId) {
        if (!targetId) return;

        const cleanId = targetId.replace('#', '');
        const tabButton = document.querySelector(`button[data-bs-target="#${cleanId}"]`);
        
        if (tabButton) {
            const tab = new bootstrap.Tab(tabButton);
            tab.show();

            tabButton.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }

    const currentHash = window.location.hash;
    if (currentHash) {
        switchProfileTab(currentHash);
    }

    const menuLinks = document.querySelectorAll('.profile-menu-link');
    menuLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (window.location.pathname.includes('/profile/')) {
                e.preventDefault();
                const targetId = this.getAttribute('data-target');
                switchProfileTab(targetId);
                window.location.hash = `#${targetId}`;
            }
        });
    });
});


