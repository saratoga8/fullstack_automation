import express from 'express';
import path from 'path';

const app = express();
const port = 3000;

app.use(express.static(path.join(__dirname, '../dist')));

app.get('/login', async (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/welcome', async (req, res) => {
    res.sendFile(path.join(__dirname, 'welcome.html'));
})

app.listen(port, '0.0.0.0', () => {
    console.log(`Server is running on http://localhost:${port}`);
});

app.get('/health', (req, res) => {
    res.sendStatus(200)
})
