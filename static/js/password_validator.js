
document.addEventListener("DOMContentLoaded", function() {

    const usernameInput = document.querySelector('input[name="username"]');
    const emailInput = document.querySelector('input[name="email"]');

    const passwordInputs = document.querySelectorAll('input[name="password1"], input[name="new_password1"]');

    passwordInputs.forEach(input => {
        const formGroup = input.closest('.form-group') || input.closest('.mb-3');
        const reqBlock = formGroup.querySelector('.password-requirements') || document.getElementById('password-requirements');

        if (!reqBlock) return;

        const reqLength = reqBlock.querySelector('.req-length');
        const reqNumber = reqBlock.querySelector('.req-number');
        const reqUppercase = reqBlock.querySelector('.req-uppercase');
        const reqNumeric = reqBlock.querySelector('.req-numeric');
        const reqSimilarity = reqBlock.querySelector('.req-similarity');

        input.addEventListener("input", function() {
            const val = input.value.toLowerCase();

            if (val.length === 0) {
                reqBlock.style.display = "none";
                input.style.borderColor = "";
                return;
            }

            reqBlock.style.display = "block";

            const isLengthValid = val.length >= 8;
            updateStyle(reqLength, isLengthValid);

            const isNumberValid = /\d/.test(input.value);
            updateStyle(reqNumber, isNumberValid);

            const isUppercaseValid = /[A-ZА-Я]/.test(input.value);
            updateStyle(reqUppercase, isUppercaseValid);

            const isNotEntirelyNumeric = /\D/.test(val);
            updateStyle(reqNumeric, isNotEntirelyNumeric);

            let isNotSimilar = true;
            const usernameVal = usernameInput ? usernameInput.value.toLowerCase() : "";
            const emailVal = emailInput ? emailInput.value.toLowerCase() : "";

            if (usernameVal && (val.includes(usernameVal) || usernameVal.includes(val) && val.length > 3)) {
                isNotSimilar = false;
            }
            if (emailVal) {
                const emailName = emailVal.split('@')[0];
                if (val.includes(emailName) || emailName.includes(val) && val.length > 3) {
                    isNotSimilar = false;
                }
            }
            updateStyle(reqSimilarity, isNotSimilar);

            if (isLengthValid && isNumberValid && isUppercaseValid && isNotEntirelyNumeric && isNotSimilar) {
                input.style.borderColor = "#79c77b";
            } else {
                input.style.borderColor = "#ff8b8b";
            }

            if (input.value.length > 0) {
                input.dispatchEvent(new Event('input'));
            }
        });
    });

    function updateStyle(element, isValid) {
        if (!element) return;
        if (isValid) {
            element.classList.remove("text-danger");
            element.classList.add("text-success");
            element.innerHTML = "✔ " + element.innerHTML.substring(2);
        } else {
            element.classList.remove("text-success");
            element.classList.add("text-danger");
            element.innerHTML = "✖ " + element.innerHTML.substring(2);
        }
    }
});
