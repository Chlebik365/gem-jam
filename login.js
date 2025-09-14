const form = document.getElementById("login-form");
const errorMsg = document.getElementById("login-error");
console.log("login.js loaded");

form.addEventListener("submit", async e => {
  e.preventDefault();
  console.log("Submitting login form");

  const formData = new FormData(form);
  const res = await fetch(form.action, { method: "POST", body: formData });
  console.log("Response status:", res.status);

  if (res.status === 200) {
    window.location.href = "/home.html";
  } else {
    console.log("Login failed");
    errorMsg.textContent = "Invalid login"; // make sure text exists
    errorMsg.style.display = "block";       // force visible
  }
});
