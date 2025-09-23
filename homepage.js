// homepage.js
fetch("/api/stone", {
    method: "GET",
    credentials: "include" // include cookies like session_id
})
.then(response => {
    if (!response.ok) {
        throw new Error("Failed to fetch stone");
    }
    return response.json(); // parse response body as JSON
})
.then(data => {
    const stone = data.stone;
    console.log("Stone from server:", stone);

    // You can now call your rendering function here
    renderStone(stone);
})
.catch(error => {
    console.error("Error:", error);
    console.log("No stone preference found or user not logged in.");
});

const titleEl = document.getElementById('title');
const imagesEl = document.getElementById('images');
const stoneSelection = document.getElementById('stone_selection');

function renderStone(stone) {
    if (!stone) {
        titleEl.textContent = "Don't have a stone group yet? Select one below!";
        stoneSelection.innerHTML = "<button onclick=\"window.location.href='stones.html'\">Go to Stones Page</button>";

    } else {
        titleEl.textContent = `You are in the ${stone.charAt(0).toUpperCase() + stone.slice(1)} group!`;

        // stone name -> array of image URLs
        const stoneImages = {
            granite: [
                'images/granite1.jpg',
                'images/granite2.webp',
                'images/granite3.webp'
            ],
            marble: [
                'images/marble1.jpg',
                'images/marble2.webp',
                'images/marble3.jpg'
            ],
            basalt: [
                'images/basalt1.webp',
                'images/basalt2.jpg',
                'images/basalt3.webp'
            ],
            sandstone: [
                'images/sandstone1.webp',
                'images/sandstone2.jpg',
                'images/sandstone3.jpeg'
            ],
            diamond: [
                'images/diamond1.jpg',
                'images/diamond2.jpg',
                'images/diamond3.webp'
            ],
            emerald: [
                'images/emerald1.webp',
                'images/emerald2.webp',
                'images/emerald3.jpg'
            ],
            amethyst: [
                'images/amethyst1.jpg',
                'images/amethyst2.jpg',
                'images/amethyst3.webp'
            ],
            obsidian: [
                'images/obsidian1.jpg',
                'images/obsidian2.webp',
                'images/obsidian3.webp'
            ],
            quartz: [
                'images/quartz1.jpg',
                'images/quartz2.jpg',
                'images/quartz3.webp'
            ],
            turquoise: [
                'images/turquoise1.jpg',
                'images/turquoise2.jpg',
                'images/turquoise3.webp'
            ]
        };

        const imgs = stoneImages[stone] || [];
        imgs.forEach(src => {
            const img = document.createElement('img');
            img.src = src;
            img.alt = stone;
            imagesEl.appendChild(img);
        });
    }
}