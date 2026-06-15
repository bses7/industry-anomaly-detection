"use client";
import React from "react";
import { History, ShieldAlert, ShieldCheck, Clock } from "lucide-react";

export default function AlertList({ history }: { history: any[] }) {
  return (
    // Set a max-height (approx 550px fits about 4 items) and overflow-y-auto
    <div className="bg-card-bg backdrop-blur-xl border border-white/5 rounded-[2.5rem] p-6 h-[600px] flex flex-col shadow-2xl">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-sm font-black text-slate-500 uppercase tracking-[0.2em] flex items-center gap-2">
          <History size={16} className="text-neon-cyan" />
          Recent Activity
        </h3>
        <span className="text-[10px] font-bold bg-white/5 px-2 py-1 rounded text-slate-400">
          {history.length} SCANS
        </span>
      </div>

      {/* Scrollable Container */}
      <div className="flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar">
        {history.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-slate-600 opacity-50">
            <Clock size={32} strokeWidth={1} />
            <p className="text-[10px] font-bold uppercase mt-2">
              No records found
            </p>
          </div>
        ) : (
          history.map((item, idx) => {
            // Safety logic: Check if timestamp exists and is a string
            const timeStr =
              item.timestamp && typeof item.timestamp === "string"
                ? item.timestamp.split(" ")[1]
                : "--:--";

            // Safety logic: Handle nested results object or flat DB object
            const isAnomaly = item.results
              ? item.results.is_anomaly
              : item.is_anomaly;
            const score = item.results
              ? item.results.anomaly_score
              : item.anomaly_score;
            const severity = item.results
              ? item.results.severity
              : item.severity;

            return (
              <div
                key={item.id || idx}
                className="bg-slate-900/40 border border-white/5 p-4 rounded-2xl hover:bg-white/5 transition-all group"
              >
                <div className="flex justify-between items-start mb-2">
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                        isAnomaly
                          ? "bg-neon-ruby/10 text-neon-ruby"
                          : "bg-emerald-500/10 text-emerald-400"
                      }`}
                    >
                      {isAnomaly ? (
                        <ShieldAlert size={16} />
                      ) : (
                        <ShieldCheck size={16} />
                      )}
                    </div>
                    <div>
                      <p className="text-xs font-black text-white uppercase tracking-tight truncate max-w-[100px]">
                        {item.machine_type}
                      </p>
                      <p className="text-[9px] text-slate-500 font-bold uppercase">
                        {timeStr}
                      </p>
                    </div>
                  </div>
                  <div
                    className={`text-[9px] font-black px-2 py-1 rounded-md uppercase tracking-tighter border ${
                      isAnomaly
                        ? "border-neon-ruby/30 text-neon-ruby bg-neon-ruby/5"
                        : "border-emerald-500/30 text-emerald-400 bg-emerald-500/5"
                    }`}
                  >
                    {severity}
                  </div>
                </div>
                <p className="text-[10px] text-slate-400 truncate italic">
                  "{item.filename}"
                </p>
                <div className="mt-3 flex items-center justify-between text-[10px]">
                  <span className="text-slate-600 font-bold uppercase">
                    Score
                  </span>
                  <span
                    className={`font-mono font-bold ${isAnomaly ? "text-neon-ruby" : "text-neon-cyan"}`}
                  >
                    {score}
                  </span>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
