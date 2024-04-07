var isCaptchaVerified = false;

function verifyCaptcha() {
  isCaptchaVerified = true;
  document.getElementById("captchaMessage").style.display = "none";
}

document
  .getElementById("yourForm")
  .addEventListener("submit", function (event) {
    // Clear previous error messages
    document.getElementById("emailError").style.display = "none";
    document.getElementById("captchaMessage").style.display = "none";

    const emailInput = document.getElementById("email");
    const emailValue = emailInput.value;
    const emailDomain = emailValue.substring(emailValue.lastIndexOf("@") + 1);
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Simple regex for email validation

    // Validate Email Format
    if (!emailRegex.test(emailValue)) {
      document.getElementById("emailError").textContent =
        "Please enter a valid business email address.";
      document.getElementById("emailError").style.display = "block";
      event.preventDefault(); // Stop form submission
      return; // Exit function to prevent further execution
    }

    // CAPTCHA Verification
    if (!isCaptchaVerified) {
      document.getElementById("captchaMessage").style.display = "block";
      event.preventDefault(); // Prevent form submission
      return; // Exit function to prevent further execution
    }
  });
