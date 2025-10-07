document.addEventListener("DOMContentLoaded", () => {
  // Apply saved theme
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "light") {
    document.documentElement.classList.add("light");
  }

  // Toggle theme
  const toggleBtn = document.getElementById("toggle-btn");
  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      document.documentElement.classList.toggle("light");
      const theme = document.documentElement.classList.contains("light") ? "light" : "dark";
      localStorage.setItem("theme", theme);
    });
  }

  // Sidebar logic
  const openSidebarBtn = document.getElementById("open-sidebar");
  const sidebar = document.getElementById("sidebar");
  const closeSidebarBtn = document.getElementById("sidebar-close");
  const overlay = document.getElementById("sidebar-overlay");

  if (openSidebarBtn && sidebar && closeSidebarBtn && overlay) {
    openSidebarBtn.addEventListener("click", () => {
      sidebar.classList.add("open");
      overlay.classList.add("active");
    });

    const closeSidebar = () => {
      sidebar.classList.remove("open");
      overlay.classList.remove("active");
    };

    closeSidebarBtn.addEventListener("click", closeSidebar);
    overlay.addEventListener("click", closeSidebar);
  }
});
