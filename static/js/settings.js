
document.addEventListener("DOMContentLoaded", function() {
    const allInputs = document.querySelectorAll('.tab-content input');

    allInputs.forEach(input => {
        input.classList.add('form-control');
    });
});
