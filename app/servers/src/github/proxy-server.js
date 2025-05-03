import express from "express";
import { spawn } from "child_process";
import cors from "cors";


const app = express();
const PORT = 3000;
const MCP_PROCESS = spawn("node", ["dist/index.js"], {
    stdio: ["pipe", "pipe", "pipe"]
});

app.use(cors());
app.use(express.json());

let buffer = "";

MCP_PROCESS.stdout.on("data", (chunk) => {
    buffer += chunk.toString();
});

app.post("/mcp", (req, res) => {
    console.log("Received request:", req.body);
    const input = JSON.stringify(req.body) + "\n"; // newline important
    console.log("Sending to MCP:", input);
    MCP_PROCESS.stdin.write(input);

    const interval = setInterval(() => {
        if (buffer.includes("\n")) {
            const lines = buffer.split("\n");
            const fullResponse = lines.shift();
            buffer = lines.join("\n"); // keep any leftover

            clearInterval(interval);

            try {
                const response = JSON.parse(fullResponse);
                console.log("Responding:", response);
                res.json(response);
            } catch (err) {
                console.error("Error parsing MCP response:", err.message);
                res.status(500).send("Error parsing MCP response: " + err.message);
            }
        }
    }, 10);
});

app.listen(PORT, () => {
    console.log("✅ Proxy server listening on http://localhost:" + PORT);
});
