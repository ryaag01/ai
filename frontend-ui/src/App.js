import React, { useState } from "react";
import axios from "axios";

function App() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async () => {
    const res = await axios.post("http://localhost:8080/infer", {
      input,
      model: "deepseek-v2",
    });
    setResponse(JSON.stringify(res.data, null, 2));
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Unified AI Platform</h1>
      <textarea
        rows="4"
        cols="50"
        placeholder="Enter prompt..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
      ></textarea>
      <br />
      <button onClick={handleSubmit}>Submit</button>
      <pre>{response}</pre>
    </div>
  );
}

export default App;