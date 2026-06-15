"use client";
import React from "react";
import { ShieldCheck, ShieldAlert, Zap, AlertTriangle } from "lucide-react";

export default function ResultDisplay({ data }: { data: any }) {
  // Defensive Check: If the backend sent an error or malformed data
  if (!data || !data.results) {
    return (
      <div className="bg-card-bg backdrop-blur-xl border border-neon-ruby/20 rounded-[2.5rem] p-12 flex flex-col items-center justify-center text-center">
        <AlertTriangle className="text-neon-ruby mb-4" size={48} />
        <h3 className="text-xl font-bold text-white">Analysis Failed</h3>
        <p className="text-sm text-slate-500 mt-2 max-w-xs">
          The AI engine encountered a structural mismatch while loading the
          model. Check the backend terminal for logs.
        </p>
      </div>
    );
  }

  const { is_anomaly, severity, anomaly_score, confidence } = data.results;

  return (
    <div className="bg-card-bg backdrop-blur-xl border border-white/10 rounded-[2.5rem] p-8 shadow-2xl animate-in fade-in zoom-in duration-500">
      <div className="flex justify-between items-center mb-8">
        <h3 className="text-xl font-bold flex items-center gap-2">
          <Zap className="text-neon-cyan" size={20} />
          Diagnostic Fingerprint
        </h3>
        <div
          className={`px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest flex items-center gap-2 border ${
            is_anomaly
              ? "bg-neon-ruby/10 text-neon-ruby border-neon-ruby/30"
              : "bg-emerald-500/10 text-emerald-400 border-emerald-500/30"
          }`}
        >
          {is_anomaly ? <ShieldAlert size={14} /> : <ShieldCheck size={14} />}
          {is_anomaly ? "Anomaly Detected" : "Normal Operation"}
        </div>
      </div>

      <div className="relative rounded-2xl overflow-hidden border border-white/5 mb-8">
        <img
          src={data.visualization}
          alt="Spectrogram"
          className="w-full h-auto"
        />
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-slate-900/50 p-6 rounded-2xl border border-white/5">
          <span className="text-[10px] font-black text-slate-500 uppercase block mb-2">
            Score
          </span>
          <span
            className={`text-3xl font-mono font-bold ${is_anomaly ? "text-neon-ruby" : "text-neon-cyan"}`}
          >
            {anomaly_score}
          </span>
        </div>
        <div className="bg-slate-900/50 p-6 rounded-2xl border border-white/5">
          <span className="text-[10px] font-black text-slate-500 uppercase block mb-2">
            Severity
          </span>
          <span
            className={`text-2xl font-bold uppercase ${is_anomaly ? "text-neon-ruby" : "text-emerald-400"}`}
          >
            {severity}
          </span>
        </div>
      </div>
    </div>
  );
}
