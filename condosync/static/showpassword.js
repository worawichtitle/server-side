console.log("showpassword.js loaded");
function showPassword(event, inputId) {
  const input = document.getElementById(inputId);
  const button = event.target;
  if (input.type === "password") {
    input.type = "text";
    button.textContent = "Hide";
  } else {
    input.type = "password";
    button.textContent = "Show";
  }
}
