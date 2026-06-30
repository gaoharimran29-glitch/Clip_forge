"use client";

import { useState } from "react";

export default function Home() {

  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const generateClips = async () => {
  setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: url,
        }),
      });

      const data = await response.json();

      console.log(data);

      setResult(data);
    } catch (error) {
      console.error(error);
    }

    setLoading(false);
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-100">

      <div className="w-full max-w-xl bg-white rounded-2xl shadow-lg p-8">

        <h1 className="text-4xl font-bold text-center mb-2">
          ClipForge
        </h1>

        <p className="text-gray-500 text-center mb-8">
          Turn any YouTube video into viral shorts using AI.
        </p>

        <input
          type="text"
          placeholder="Paste YouTube URL..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <button onClick={generateClips} className="..." disabled={loading}>
          {loading ? "Generating..." : "Generate Clips"}
        </button>

      </div>
    </main>
  );
}