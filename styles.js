document.addEventListener("DOMContentLoaded", () => {
  // Apply saved theme on page load
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "light") {
    document.documentElement.classList.add("light");
  } else {
    document.documentElement.classList.remove("light"); // default dark
  }

  // Toggle button logic (only if it exists on this page)
  const toggleBtn = document.getElementById("toggle-btn");
  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      document.documentElement.classList.toggle("light");

      // Save current theme
      if (document.documentElement.classList.contains("light")) {
        localStorage.setItem("theme", "light");
      } else {
        localStorage.setItem("theme", "dark");
      }
    });
  }
});
