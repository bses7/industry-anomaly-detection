"use client";
import { useState } from "react";
import {
  Upload,
  Fan,
  Activity,
  Waves,
  Sliders,
  AlertCircle,
  Loader2,
} from "lucide-react";

interface UploadPanelProps {
  onLoading: (val: boolean) => void;
  onComplete: (data: any) => void;
}

const MACHINES = [
  { id: "fan", label: "Fan Unit", icon: <Fan size={18} /> },
  { id: "pump", label: "Pump System", icon: <Activity size={18} /> },
  { id: "valve", label: "Control Valve", icon: <Waves size={18} /> },
  { id: "slider", label: "Slide Rail", icon: <Sliders size={18} /> },
];

export default function UploadPanel({
  onLoading,
  onComplete,
}: UploadPanelProps) {
  const [selectedMachine, setSelectedMachine] = useState("fan");
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setIsUploading(true);
    onLoading(true);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("machine_type", selectedMachine);

    try {
      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      onComplete(data);
    } catch (err) {
      console.error("Upload failed", err);
      alert(
        "Backend connection error. Ensure server.py is running on port 8000.",
      );
    } finally {
      setIsUploading(false);
      onLoading(false);
    }
  };

  return (
    <div className="bg-card-bg backdrop-blur-xl border border-white/5 rounded-[2rem] p-6 shadow-2xl h-full flex flex-col">
      <h3 className="text-sm font-black text-slate-500 uppercase tracking-[0.2em] mb-6 flex items-center gap-2">
        <Upload size={16} className="text-neon-cyan" />
        Input Configuration
      </h3>

      {/* Machine Type Selection */}
      <div className="space-y-3 mb-8">
        <label className="text-[10px] font-black text-slate-600 uppercase tracking-widest px-2">
          Asset Category
        </label>
        <div className="grid grid-cols-1 gap-2">
          {MACHINES.map((m) => (
            <button
              key={m.id}
              onClick={() => setSelectedMachine(m.id)}
              className={`flex items-center gap-4 p-4 rounded-2xl border transition-all duration-300 ${
                selectedMachine === m.id
                  ? "bg-neon-cyan/10 border-neon-cyan text-neon-cyan shadow-[0_0_15px_rgba(34,211,238,0.15)]"
                  : "bg-slate-900/40 border-white/5 text-slate-500 hover:border-white/10"
              }`}
            >
              <div
                className={
                  selectedMachine === m.id ? "text-neon-cyan" : "text-slate-600"
                }
              >
                {m.icon}
              </div>
              <span className="text-sm font-bold">{m.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* File Dropzone */}
      <div className="flex-1 flex flex-col justify-end">
        <div
          className={`relative h-32 rounded-3xl border-2 border-dashed transition-all flex flex-col items-center justify-center mb-6 ${
            file
              ? "border-emerald-500/40 bg-emerald-500/5"
              : "border-white/10 bg-white/[0.02] hover:bg-white/[0.05]"
          }`}
        >
          <input
            type="file"
            accept=".wav"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          />
          {file ? (
            <div className="text-center px-4">
              <p className="text-xs font-bold text-emerald-400 truncate max-w-[180px]">
                {file.name}
              </p>
              <p className="text-[10px] text-slate-500 font-bold uppercase mt-1">
                Ready for analysis
              </p>
            </div>
          ) : (
            <>
              <Activity className="text-slate-700 mb-2" size={24} />
              <p className="text-[10px] font-black text-slate-600 uppercase tracking-widest text-center px-6">
                Drop Acoustic Capture (.wav)
              </p>
            </>
          )}
        </div>

        {/* Submit Button */}
        <button
          onClick={handleUpload}
          disabled={!file || isUploading}
          className={`w-full py-5 rounded-2xl font-black uppercase tracking-widest text-xs transition-all shadow-xl ${
            !file || isUploading
              ? "bg-slate-800 text-slate-600 cursor-not-allowed"
              : "bg-gradient-to-r from-neon-cyan to-blue-600 text-panel-bg shadow-neon-cyan/20 hover:scale-[1.02] active:scale-95"
          }`}
        >
          {isUploading ? (
            <div className="flex items-center justify-center gap-2">
              <Loader2 className="animate-spin" size={16} />
              <span>Analyzing Spectral Data...</span>
            </div>
          ) : (
            "Initialize AI Diagnostic"
          )}
        </button>
      </div>
    </div>
  );
}
