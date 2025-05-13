const express = require('express');
const axios = require('axios');

const app = express();
const PORT = 3000;

//Static server files (HTML, CSS, JS)
app.use(express.static('public'));

//Fetch the detected gesture
app.get('/gesture', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:5000/gesture');
        res.json(response.data);
    } catch (error) {
        console.error("Error fetching gesture:", error.message);
        res.status(500).json({ error: "Failed to fetch gesture data" });
    }
});

//Fetch the latest 10 images with attached gesture detections
app.get('/recent', async (req, res) => {
    try{
        const response = await axios.get('http://localhost:5000/recent');
        res.json(response.data);
    }
    catch (error){
        console.error("Error fetching recent images:", error.message);
        res.status(500).json({ error: "Failed to fetch recent images" });
    }
});

//Fetch user feedback based on recent images
app.post('/feedback', async (req, res) => {
  try {
    await axios.post('http://localhost:5000/feedback', req.body);
    res.json({ status: 'ok' });
  } catch (err) {
    res.status(500).json({ error: 'Feedback failed' });
  }
});

//Final layer of error handling for the server
app.use((err, req, res, next) => {
    console.error('Server error:', err);
    res.status(500).json({ error: 'Internal server error' });
});

//Launch the server
app.listen(PORT, () => {
    console.log(`Web server running at http://localhost:${PORT}`);
});