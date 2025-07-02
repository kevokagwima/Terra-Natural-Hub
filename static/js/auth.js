const btn = document.querySelector(".btn");
const inputs = document.querySelectorAll(".name");

btn.addEventListener("click", () => {
  let allInputsFilled = true;

  inputs.forEach((input) => {
    if (!input.value) {
      allInputsFilled = false;
    }
  });

  if (allInputsFilled) {
    btn.classList.toggle("btn--loading");
    btn.disabled = true;
    btn.form.submit();
  }
});

document.addEventListener("DOMContentLoaded", function () {
  var passwordToggle = document.querySelectorAll(".password-toggle");
  var passwordInput = document.querySelector(".password");

  passwordToggle.forEach((p) => {
    p.addEventListener("click", function () {
      if (p.previousElementSibling.type === "password") {
        p.previousElementSibling.type = "text";
        p.classList.remove("fa-eye");
        p.classList.add("fa-eye-slash");
      } else {
        p.previousElementSibling.type = "password";
        p.classList.remove("fa-eye-slash");
        p.classList.add("fa-eye");
      }
    });
  });
});
