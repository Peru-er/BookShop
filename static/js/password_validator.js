
document.addEventListener("DOMContentLoaded", function() {
    const usernameInput = document.querySelector('input[name="username"]');
    const emailInput = document.querySelector('input[name="email"]');
    const passwordInputs = document.querySelectorAll('input[name="password1"], input[name="new_password1"], input[name="password"]');

    passwordInputs.forEach(input => {
        // Ищем блок требований сначала внутри родителя, а если нет — по ID на всей странице
        const formGroup = input.closest('.form-group') || input.closest('.mb-3');
        const reqBlock = formGroup ? (formGroup.querySelector('.password-requirements') || document.getElementById('password-requirements')) : document.getElementById('password-requirements');

        if (!reqBlock) return;

        const reqLength = reqBlock.querySelector('.req-length');
        const reqNumber = reqBlock.querySelector('.req-number');
        const reqUppercase = reqBlock.querySelector('.req-uppercase');
        const reqNumeric = reqBlock.querySelector('.req-numeric');
        const reqSimilarity = reqBlock.querySelector('.req-similarity');

        input.addEventListener("input", function() {
            const originalVal = input.value;
            const val = originalVal.toLowerCase();

            if (originalVal.length === 0) {
                reqBlock.style.display = "none";
                input.style.borderColor = "";
                return;
            }

            reqBlock.style.display = "block";

            const isLengthValid = originalVal.length >= 8;
            updateStyle(reqLength, isLengthValid);

            const isNumberValid = /\d/.test(originalVal);
            updateStyle(reqNumber, isNumberValid);

            const isUppercaseValid = /[A-ZА-Я]/.test(originalVal);
            updateStyle(reqUppercase, isUppercaseValid);

            const isNotEntirelyNumeric = /\D/.test(val);
            updateStyle(reqNumeric, isNotEntirelyNumeric);

            // Безопасная проверка схожести
            let isNotSimilar = true;
            if (usernameInput && usernameInput.value) {
                const usernameVal = usernameInput.value.toLowerCase();
                if (val.includes(usernameVal) || (usernameVal.includes(val) && val.length > 3)) {
                    isNotSimilar = false;
                }
            }
            if (emailInput && emailInput.value) {
                const emailVal = emailInput.value.toLowerCase();
                const emailName = emailVal.split('@')[0];
                if (val.includes(emailName) || (emailName.includes(val) && val.length > 3)) {
                    isNotSimilar = false;
                }
            }

            // Обновляем стиль схожести, только если этот пункт есть в HTML
            if (reqSimilarity) {
                updateStyle(reqSimilarity, isNotSimilar);
            }

            // Проверяем общую валидность (если пункта similarity нет, то его в расчет не берем)
            const allValid = isLengthValid && isNumberValid && isUppercaseValid && isNotEntirelyNumeric && (!reqSimilarity || isNotSimilar);

            if (allValid) {
                input.style.borderColor = "#79c77b";
            } else {
                input.style.borderColor = "#ff8b8b";
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
