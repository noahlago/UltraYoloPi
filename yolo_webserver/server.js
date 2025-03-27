const express = require('express');
const axios = require('axios');

const app = express();
const PORT = 3000;

//Static server files (HTML, CSS, JS)
app.use(express.static('public'));

//Fetch gesture and image data from the python yolo api
app.get('/gesture', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:5000/gesture');
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: "Failed to fetch gesture data" });
    }
});

//Launch the server
app.listen(PORT, () => {
    console.log(`Web server running at http://localhost:${PORT}`);
});