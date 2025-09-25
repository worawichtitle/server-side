console.log("showpassword.js loaded");
function showPassword(event) {
  const input = document.getElementById("password_hash");
  const button = event.target;
  if (input.type === "password") {
    input.type = "text";
    button.textContent = "Hide";
  } else {
    input.type = "password";
    button.textContent = "Show";
  }
}
