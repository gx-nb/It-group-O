// 无障碍 + 表单验证最终版
document.addEventListener('DOMContentLoaded', function () {

    // ESC 关闭 alert
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            const alerts = document.querySelectorAll('.alert');
            alerts.forEach(alert => {
                alert.classList.remove('show');
                setTimeout(() => alert.remove(), 300);
            });
        }
    });

    const forms = document.querySelectorAll('form');

    forms.forEach(form => {

        form.addEventListener('submit', function (e) {

            let hasError = false;

            // 清除旧错误
            form.querySelectorAll('.invalid-feedback').forEach(el => el.remove());

            const requiredInputs = form.querySelectorAll('[required]');

            requiredInputs.forEach(input => {

                if (!input.value.trim()) {

                    hasError = true;

                    input.classList.add('is-invalid');
                    input.setAttribute('aria-invalid', 'true');

                    const label = input.previousElementSibling
                        ? input.previousElementSibling.textContent.replace(':', '')
                        : "this field";

                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'invalid-feedback';
                    errorDiv.textContent = `Please enter ${label}`;

                    input.parentNode.appendChild(errorDiv);
                }
            });

            // Email 格式检查
            const email = form.querySelector("input[name='email']");
            if (email && email.value && !email.value.includes("@")) {

                hasError = true;

                email.classList.add('is-invalid');

                const errorDiv = document.createElement('div');
                errorDiv.className = 'invalid-feedback';
                errorDiv.textContent = "Please enter a valid email address";

                email.parentNode.appendChild(errorDiv);
            }

            // Password match 检查
            const p1 = form.querySelector("input[name='password1']");
            const p2 = form.querySelector("input[name='password2']");

            if (p1 && p2 && p1.value !== p2.value) {

                hasError = true;

                p2.classList.add('is-invalid');

                const errorDiv = document.createElement('div');
                errorDiv.className = 'invalid-feedback';
                errorDiv.textContent = "Passwords do not match";

                p2.parentNode.appendChild(errorDiv);
            }

            if (hasError) {
                e.preventDefault();

                const firstError = form.querySelector('.is-invalid');
                if (firstError) firstError.focus();
            }

        });

        // 输入时清除错误
        form.querySelectorAll('input').forEach(input => {

            input.addEventListener('input', function () {

                this.classList.remove('is-invalid');
                this.setAttribute('aria-invalid', 'false');

                const errorDiv = this.parentNode.querySelector('.invalid-feedback');
                if (errorDiv) errorDiv.remove();

            });

        });

    });

});
// Room Inspection: No issues logic
const noIssue = document.getElementById("noIssue");
const issues = document.querySelectorAll(".issue");

if (noIssue && issues.length > 0) {

    noIssue.addEventListener("change", function () {

        if (this.checked) {

            issues.forEach(box => {
                box.checked = false;
                box.disabled = true;
            });

        } else {

            issues.forEach(box => {
                box.disabled = false;
            });

        }

    });

    issues.forEach(box => {

        box.addEventListener("change", function () {

            if (this.checked) {
                noIssue.checked = false;
            }

        });

    });

}