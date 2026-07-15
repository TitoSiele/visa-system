const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

// In-memory array to simulate an Immigration database
let applications = [
    { id: 101, name: "Alice Smith", passportNo: "A1234567", country: "Canada", type: "Tourist Visa", status: "Pending" }
];

// 1. Endpoint to submit a new application
app.post('/api/apply', (req, res) => {
    const { name, passportNo, country, type } = req.body;
    if (!name || !passportNo || !country) {
        return res.status(400).json({ success: false, message: "Missing required information." });
    }
    
    const newApplication = {
        id: Date.now(),
        name,
        passportNo,
        country,
        type,
        status: "Pending"
    };
    
    applications.push(newApplication);
    res.json({ success: true, message: "Application submitted successfully!", id: newApplication.id });
});

// 2. Endpoint to fetch all applications for the Officer Dashboard
app.get('/api/applications', (req, res) => {
    res.json(applications);
});

// 3. Endpoint to Approve/Reject an application
app.post('/api/action', (req, res) => {
    const { id, status } = req.body;
    const application = applications.find(app => app.id === parseInt(id));
    
    if (application) {
        application.status = status;
        return res.json({ success: true, message: `Application ${status} successfully!` });
    }
    res.status(404).json({ success: false, message: "Application not found." });
});

app.listen(PORT, () => {
    console.log(`Immigration system running at http://localhost:${PORT}`);
});