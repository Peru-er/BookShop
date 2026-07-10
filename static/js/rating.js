
document.addEventListener('DOMContentLoaded', function() {
    const starContainer = document.getElementById('interactive-stars');
    if (!starContainer) return;

    const stars = starContainer.querySelectorAll('.star-btn');
    const hiddenSelect = document.querySelector('select[name="rating"]');

    let currentRating = 0;

    if (hiddenSelect && hiddenSelect.value && hiddenSelect.value !== '5') {
        currentRating = parseInt(hiddenSelect.value);
    } else if (hiddenSelect) {

        hiddenSelect.value = '';
    }

    highlightStars(currentRating);

    stars.forEach(star => {

        star.addEventListener('mouseover', function() {
            const hoverValue = parseInt(this.getAttribute('data-value'));
            highlightStars(hoverValue);
        });

        star.addEventListener('mouseout', function() {
            highlightStars(currentRating);
        });

        star.addEventListener('click', function() {
            currentRating = parseInt(this.getAttribute('data-value'));
            if (hiddenSelect) {
                hiddenSelect.value = currentRating;
            }
            highlightStars(currentRating);
        });
    });

    function highlightStars(value) {
        stars.forEach(star => {
            const starValue = parseInt(star.getAttribute('data-value'));
            if (starValue <= value) {
                star.classList.add('active');
            } else {
                star.classList.remove('active');
            }
        });
    }
});
