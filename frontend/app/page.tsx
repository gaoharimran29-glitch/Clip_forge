"use client";

import { useState } from "react";
import { Sparkles, Video, Download, Link2, AlertCircle, Play } from "lucide-react";

interface Clip {
  id: number;
  start: number;
  end: number;
  score: number;
  reason: string;
  clips_path_normalized: string;
}

export default function Home() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [clips, setClips] = useState<Clip[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  const generateClips = async () => {
    if (!url) return;
    setLoading(true);
    setError(null);
    setClips(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) throw new Error("Failed to generate clips. Is your backend running?");
      
      const data = await response.json();
      setClips(data.clips);
    } catch (err: any) {
      console.error(err);
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#0B0F19] text-gray-100 selection:bg-indigo-500 selection:text-white antialiased overflow-x-hidden relative flex flex-col items-center p-6 md:p-12">
      
      {/* Background Decorative Glows */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-[500px] pointer-events-none opacity-20 bg-[radial-gradient(circle_at_top,_var(--tw-gradient-stops))] from-indigo-500 via-purple-500 to-transparent blur-3xl -z-10" />

      {/* Header section */}
      <header className="w-full max-w-5xl flex justify-between items-center mb-16">
        <div className="flex items-center gap-2 font-bold text-xl tracking-tight bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">
          <Sparkles className="w-5 h-5 text-indigo-400" />
          ClipForge.ai
        </div>
        <div className="text-xs bg-gray-800/40 border border-gray-700/50 text-gray-400 px-3 py-1.5 rounded-full backdrop-blur-md">
          v1.0.0 (Beta)
        </div>
      </header>

      {/* Input Box Card */}
      <section className="w-full max-w-2xl bg-gray-900/40 border border-gray-800/80 backdrop-blur-xl rounded-3xl p-8 md:p-10 shadow-2xl relative">
        <div className="absolute -top-3 left-6 bg-gradient-to-r from-indigo-500 to-purple-500 text-[10px] font-bold tracking-widest uppercase px-3 py-1 rounded-md shadow-lg shadow-indigo-500/20">
          AI-Powered Engine
        </div>

        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight bg-gradient-to-b from-white to-gray-400 bg-clip-text text-transparent mb-3">
            Turn Videos into Viral Shorts
          </h1>
          <p className="text-sm md:text-base text-gray-400 max-w-md mx-auto leading-relaxed">
            Paste a YouTube link and let our pipeline extract high-retention vertical clips using AI.
          </p>
        </div>

        <div className="space-y-4">
          <div className="relative group">
            <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none text-gray-500 group-focus-within:text-indigo-400 transition-colors">
              <Link2 className="w-5 h-5" />
            </div>
            <input
              type="text"
              placeholder="Paste YouTube video URL here..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              disabled={loading}
              className="w-full bg-gray-950/60 border border-gray-800 rounded-xl pl-12 pr-4 py-4 text-gray-200 placeholder-gray-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/30 transition-all text-sm disabled:opacity-50"
            />
          </div>

          <button
            onClick={generateClips}
            disabled={loading || !url}
            className="w-full relative group overflow-hidden bg-gradient-to-r from-indigo-600 to-purple-600 disabled:from-gray-800 disabled:to-gray-800 disabled:cursor-not-allowed text-white font-medium py-4 px-6 rounded-xl transition-all active:scale-[0.99] shadow-lg shadow-indigo-600/10 hover:shadow-indigo-600/20"
          >
            <div className="absolute inset-0 bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity" />
            <span className="flex items-center justify-center gap-2">
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Analyzing Timestamps & Hooks...
                </>
              ) : (
                <>
                  <Video className="w-5 h-5" />
                  Forge Micro-Clips
                </>
              )}
            </span>
          </button>
        </div>

        {error && (
          <div className="mt-6 flex items-start gap-3 bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-xl text-sm animate-in fade-in duration-200">
            <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
            <p>{error}</p>
          </div>
        )}
      </section>

      {/* Results Workspace Grid */}
      {clips && clips.length > 0 && (
        <section className="w-full max-w-5xl mt-20 animate-in fade-in slide-in-from-bottom-6 duration-500">
          <div className="flex items-center gap-3 mb-8 justify-between border-b border-gray-800 pb-4">
            <div className="flex items-center gap-2">
              <span className="bg-indigo-500/10 text-indigo-400 p-2 rounded-lg border border-indigo-500/20">
                <Video className="w-5 h-5" />
              </span>
              <h2 className="text-xl font-bold tracking-tight text-white">Generated Shorts Workspace</h2>
            </div>
            <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-gray-900 border border-gray-800 text-gray-400">
              {clips.length} Clips Ready
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {clips.map((clip, index) => (
              <div
                key={index}
                className="group/card bg-gray-900/20 border border-gray-800/60 rounded-2xl p-4 flex flex-col justify-between hover:border-gray-700/80 transition-all shadow-xl hover:shadow-black/40"
              >
                <div>
                  {/* Smartphone Aspect Preview Box */}
                  <div className="aspect-[9/16] w-full max-w-[240px] mx-auto bg-gray-950 rounded-xl overflow-hidden mb-4 relative shadow-inner border border-gray-800 group-hover/card:border-gray-700 transition-colors">
                    <video
                      src={`http://127.0.0.1:8000${clip.clips_path_normalized}`}
                      controls
                      className="w-full h-full object-cover"
                      poster="/api/placeholder/240/426" 
                    />
                    <div className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-100 group-hover/card:opacity-0 pointer-events-none transition-opacity">
                      <div className="bg-white/10 p-4 rounded-full backdrop-blur-md border border-white/20">
                        <Play className="w-6 h-6 text-white fill-white" />
                      </div>
                    </div>
                  </div>

                  <div className="px-1">
                    <h3 className="font-semibold text-base text-gray-100 line-clamp-1 mb-1 group-hover/card:text-indigo-400 transition-colors">
                    Clip #{clip.id} • Score {clip.score}/10
                    </h3>
                    <p className="text-xs text-gray-400 line-clamp-2 leading-relaxed mb-4">
                      {clip.reason || "No descriptions parsed for this segment."}
                    </p>
                  </div>
                </div>

                <a
                  href={`http://127.0.0.1:8000${clip.clips_path_normalized}`}
                  download
                  className="flex items-center justify-center gap-2 w-full bg-gray-800 hover:bg-gray-700 text-gray-200 font-medium py-2.5 rounded-xl transition-all text-sm group/btn border border-gray-700/50"
                >
                  <Download className="w-4 h-4 transition-transform group-hover/btn:-translate-y-0.5" />
                  Download Assets
                </a>
              </div>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}