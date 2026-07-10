
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

    const reviewForm = document.getElementById('review-form');
    const reviewList = document.querySelector('.review-list');
    const formContainer = document.querySelector('.review-form-container');

    if (reviewForm && reviewList) {
        reviewForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(this);

            fetch(window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {

                    const noReviewsText = reviewList.querySelector('.text-muted');
                    if (noReviewsText) noReviewsText.remove();

                    let verifiedBadge = '';
                    if (data.is_verified) {
                        verifiedBadge = `
                            <span class="verified-purchase-badge">
                                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" class="bi bi-patch-check-fill me-1" viewBox="0 0 16 16">
                                    <path d="M10.067.87a2.89 2.89 0 0 0-4.134 0l-.622.622-.622-.622a2.89 2.89 0 0 0-4.134 0l.622.622-.622.622a2.89 2.89 0 0 0 0 4.134l.622.622-.622.622a2.89 2.89 0 0 0 4.134 0l.622-.622.622.622a2.89 2.89 0 0 0 4.134 0l-.622-.622.622-.622a2.89 2.89 0 0 0 0-4.134l-.622-.622.622-.622z"/>
                                </svg>
                                Verified Purchase
                            </span>`;
                    }

                    const newReviewHtml = `
                        <div class="custom-review-card" style="animation: fadeIn 0.5s ease-in-out;">
                            <div class="d-flex justify-content-between align-items-start flex-wrap gap-2 mb-3">
                                <div>
                                    <div class="review-user-name mb-1">${data.username}</div>
                                    <div class="review-date">${data.date}</div>
                                </div>
                                <div class="d-flex align-items-center gap-3">
                                    <span class="review-stars-static">${data.rating_stars}</span>
                                    ${verifiedBadge}
                                </div>
                            </div>
                            <p class="review-comment-text mb-0" style="white-space: pre-line;">${data.text}</p>
                        </div>`;

                    reviewList.insertAdjacentHTML('afterbegin', newReviewHtml);

                    formContainer.innerHTML = `
                        <h4 class="text-white mb-3">Leave a Review</h4>
                        <div class="alert alert-info" style="background: #1c2d23; border-color: #2b4737; color: #a3cfb6; animation: fadeIn 0.4s ease;">
                            You have already reviewed this product. Thank you for your feedback.
                        </div>`;
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

});
