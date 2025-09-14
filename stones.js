const checkboxes = document.querySelectorAll('input[name="traits"]');
const btn = document.getElementById('findStoneBtn');

checkboxes.forEach(cb => cb.addEventListener('change', () => {
  const checked = [...checkboxes].filter(c => c.checked);
  if (checked.length > 2) {
    cb.checked = false; // stop selecting more
  }
  btn.disabled = checked.length !== 2;
}));
