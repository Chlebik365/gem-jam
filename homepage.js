fetch("/api/stone", {
  method: "POST",               // your handler only implements POST
  headers: {
    "Content-Type": "application/json"
  },
  credentials: "include"        // <-- important so cookies (session_id) are sent
})
  .then(res => {
    if (!res.ok) {
      throw new Error("Request failed: " + res.status);
    }
    return res.json();
  })
  .then(data => {
    console.log("Stone fetched from server:", data.stone);
    displayStone(data.stone);

  })
  .catch(err => {
    console.error("Error while fetching stone:", err);
  });

function displayStone(stone) {
  const stoneDiv = document.getElementById("stone");
  stoneDiv.textContent = stone;

  const name = stone.toLowerCase();
  const formats = [".jpg", ".png", ".jpeg", ".gif", ".webp"];

  const imageContainer = document.getElementById("images");
  imageContainer.innerHTML = ""; // Clear previous images if any

  for(let i = 1; i <=3; i++) {
    let found = false;
    for(const format of formats) {
      const imgPath = `images/${name}${i}${format}`;
      const img = new Image();
      img.src = imgPath;

      img.onload = () => {
        if(!found) {
          imageContainer.appendChild(img);
          found = true;
        }
      }
    }
  }


}