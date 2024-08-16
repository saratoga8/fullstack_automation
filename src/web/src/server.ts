import express from 'express';
import path from 'path';
import {readFileSync} from "fs";


const app = express();
const port = 3000;

app.use(express.static(path.join(__dirname, '../dist')));

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/welcome/:userName', (req, res) => {
    const htmlTxt = readFileSync(path.join(__dirname, 'welcome.html'))
    res.set('Content-Type', 'text/html')
    res.send(htmlTxt);
})

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
