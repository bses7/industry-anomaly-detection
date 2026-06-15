"use client";
import { useState, useEffect, useMemo } from "react";
import Sidebar from "@/components/Sidebar";
import UploadPanel from "@/components/UploadPanel";
import ResultDisplay from "@/components/ResultDisplay";
import MetricCard from "@/components/MetricCard";
import AlertList from "@/components/AlertList";
import { Cpu, Zap, Activity, ShieldCheck, Loader2 } from "lucide-react";

export default function Dashboard() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<any[]>([]);

  // --- DYNAMIC STATS CALCULATION ---
  const stats = useMemo(() => {
    const total = history.length;
    const critical = history.filter((item) => {
      // Handle both nested and flat structures safely
      const isAnomaly = item.results
        ? item.results.is_anomaly
        : item.is_anomaly;
      return isAnomaly === 1 || isAnomaly === true;
    }).length;

    return {
      totalScans: total,
      criticalAlerts: critical,
      healthScore:
        total > 0 ? Math.round(((total - critical) / total) * 100) : 100,
    };
  }, [history]);

  // --- DATA FETCHING ---
  const fetchHistory = async () => {
    try {
      const res = await fetch("http://localhost:8000/history");
      if (!res.ok) throw new Error("Failed to fetch");
      const data = await res.json();
      setHistory(data);
    } catch (err) {
      console.error("Database connection error:", err);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  // --- EVENT HANDLERS ---
  const handleLoading = (isLoading: boolean) => {
    setLoading(isLoading);
    if (isLoading) setResult(null); // Clear previous result to prevent "undefined" crashes
  };

  const handleComplete = (data: any) => {
    setResult(data);
    fetchHistory(); // Refresh history list and stats immediately
  };

  return (
    <div className="flex h-screen bg-panel-bg text-slate-200 overflow-hidden font-sans">
      <Sidebar />

      <main className="flex-1 overflow-y-auto p-6 relative custom-scrollbar">
        {/* Aesthetic Background Glows */}
        <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-neon-cyan/5 blur-[120px] pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-neon-ruby/5 blur-[100px] pointer-events-none" />

        <div className="max-w-[1600px] mx-auto">
          {/* Header Area */}
          <header className="flex justify-between items-center mb-8">
            <div className="animate-in fade-in slide-in-from-left duration-700">
              <h2 className="text-slate-500 text-[10px] font-black uppercase tracking-[0.4em] mb-1">
                Industrial Intelligence Unit
              </h2>
              <h1 className="text-3xl font-black text-white tracking-tight uppercase">
                System Overview
              </h1>
            </div>

            <div className="flex items-center gap-4 bg-slate-900/50 border border-white/5 p-2 rounded-2xl backdrop-blur-md">
              <div className="px-4 py-2 text-right">
                <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">
                  Asset Health
                </p>
                <p
                  className={`text-xs font-black uppercase ${stats.healthScore > 70 ? "text-emerald-400" : "text-neon-ruby"}`}
                >
                  {stats.healthScore}% Optimal
                </p>
              </div>
              <div
                className={`w-10 h-10 rounded-xl flex items-center justify-center border ${
                  stats.healthScore > 70
                    ? "bg-emerald-500/10 border-emerald-500/20"
                    : "bg-neon-ruby/10 border-neon-ruby/20"
                }`}
              >
                <ShieldCheck
                  className={
                    stats.healthScore > 70
                      ? "text-emerald-400"
                      : "text-neon-ruby"
                  }
                  size={20}
                />
              </div>
            </div>
          </header>

          {/* Top Metrics Grid */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <MetricCard
              label="Active Assets"
              value="04"
              sub="Fan, Pump, Valve, Slider"
              icon={<Cpu />}
              color="cyan"
            />
            <MetricCard
              label="Total Scans"
              value={stats.totalScans.toString()}
              sub="Database Records"
              icon={<Zap />}
              color="purple"
            />
            <MetricCard
              label="Critical Alerts"
              value={stats.criticalAlerts.toString()}
              sub="Action Required"
              icon={<Activity />}
              color="ruby"
            />
            <MetricCard
              label="System Status"
              value={stats.criticalAlerts > 0 ? "Warning" : "Healthy"}
              sub="Live Monitoring"
              icon={<ShieldCheck />}
              color={stats.criticalAlerts > 0 ? "ruby" : "emerald"}
            />
          </div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Control Panel */}
            <div className="lg:col-span-3">
              <UploadPanel
                onLoading={handleLoading}
                onComplete={handleComplete}
              />
            </div>

            {/* AI Output Center */}
            <div className="lg:col-span-6">
              {loading ? (
                /* High-Tech Loading State */
                <div className="h-full min-h-[500px] bg-card-bg backdrop-blur-xl border border-white/5 rounded-[2.5rem] flex flex-col items-center justify-center text-center p-12 relative overflow-hidden">
                  <div className="absolute inset-0 bg-neon-cyan/5 animate-pulse" />
                  <div className="relative">
                    <Loader2
                      className="animate-spin text-neon-cyan mb-6"
                      size={64}
                      strokeWidth={1}
                    />
                    <div className="absolute inset-0 bg-neon-cyan/20 blur-2xl animate-pulse" />
                  </div>
                  <h3 className="text-xl font-black text-white tracking-widest uppercase">
                    Analyzing Spectral Data
                  </h3>
                  <p className="text-[10px] text-slate-500 font-bold uppercase mt-2 tracking-[0.2em]">
                    Running Hybrid-ViT Inference Engine
                  </p>
                </div>
              ) : result ? (
                <ResultDisplay data={result} />
              ) : (
                /* Empty State */
                <div className="h-full min-h-[500px] bg-card-bg backdrop-blur-xl border border-white/5 rounded-[2.5rem] flex flex-col items-center justify-center text-center p-12 border-dashed border-slate-800">
                  <div className="w-20 h-20 bg-slate-800/30 rounded-full flex items-center justify-center mb-6">
                    <Activity className="text-slate-600" size={32} />
                  </div>
                  <h3 className="text-xl font-bold text-slate-400 mb-2 tracking-tight">
                    Signal Input Required
                  </h3>
                  <p className="text-sm text-slate-600 max-w-xs leading-relaxed">
                    Upload a .wav capture to begin acoustic decomposition and
                    anomaly classification.
                  </p>
                </div>
              )}
            </div>

            {/* Recent Activity Log */}
            <div className="lg:col-span-3">
              <AlertList history={history} />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
