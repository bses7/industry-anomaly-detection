"use client";
import Sidebar from "@/components/Sidebar";
import MetricCard from "@/components/MetricCard";
import { Info, BarChart, Zap, Globe, Layers, Activity } from "lucide-react";

export default function DatasetPage() {
  return (
    <div className="flex h-screen bg-panel-bg text-slate-200 overflow-hidden font-sans">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8 relative custom-scrollbar">
        {/* Background Decorative Glow */}
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-neon-cyan/5 blur-[120px] pointer-events-none" />

        <div className="max-w-6xl mx-auto">
          <header className="mb-12">
            <h2 className="text-slate-500 text-[10px] font-black uppercase tracking-[0.4em] mb-2">
              Knowledge Discovery Center
            </h2>
            <h1 className="text-4xl font-black text-white tracking-tight uppercase">
              MIMII Dataset Insights
            </h1>
            <p className="text-slate-500 mt-4 max-w-2xl text-sm leading-relaxed">
              Exploratory Data Analysis of the Malfunctioning Industrial
              Machines Investigation and Inspection dataset. Analyzing 100.2 GB
              of acoustic emission data across four industrial asset categories.
            </p>
          </header>

          {/* Core Dataset Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <MetricCard
              label="Total Samples"
              value="29,265"
              sub="Acoustic Clips"
              icon={<Globe />}
              color="cyan"
            />
            <MetricCard
              label="Audio Duration"
              value="81.29h"
              sub="Lifetime Scanned"
              icon={<Zap />}
              color="purple"
            />
            <MetricCard
              label="Signal Noise"
              value="-6dB"
              sub="Worst Case SNR"
              icon={<Layers />}
              color="ruby"
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Section 1: Class Imbalance */}
            <div className="bg-card-bg backdrop-blur-xl border border-white/5 rounded-[2.5rem] p-8 shadow-2xl">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <BarChart className="text-neon-cyan" size={20} />
                  Class Imbalance
                </h3>
                <span className="text-[10px] font-bold text-slate-500 bg-white/5 px-2 py-1 rounded">
                  LOG SCALE
                </span>
              </div>
              <p className="text-sm text-slate-500 mb-6 leading-relaxed">
                The dataset exhibits extreme class imbalance. Training on
                high-volume "Normal" data allows the model to learn a baseline
                distribution, identifying anomalies as statistical outliers.
              </p>
              <div className="rounded-2xl overflow-hidden border border-white/10 bg-slate-950/50 p-2">
                <img
                  src="/distribution_summary.png"
                  alt="Class Distribution"
                  className="w-full h-auto rounded-xl opacity-90 hover:opacity-100 transition-opacity"
                />
              </div>
            </div>

            {/* Section 2: Noise Robustness */}
            <div className="bg-card-bg backdrop-blur-xl border border-white/5 rounded-[2.5rem] p-8 shadow-2xl">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <Info className="text-ruby-400" size={20} />
                  SNR Spectral Power
                </h3>
                <span className="text-[10px] font-bold text-slate-500 bg-white/5 px-2 py-1 rounded">
                  PSD ANALYSIS
                </span>
              </div>
              <p className="text-sm text-slate-500 mb-6 leading-relaxed">
                Industrial environments present a "Noise Floor" challenge. At
                -6dB SNR, the background factory noise often masks the
                mechanical frequency peaks, requiring latent noise filtration.
              </p>
              <div className="rounded-2xl overflow-hidden border border-white/10 bg-slate-950/50 p-2">
                <img
                  src="/noise.png"
                  alt="Noise Floor Analysis"
                  className="w-full h-auto rounded-xl opacity-90 hover:opacity-100 transition-opacity"
                />
              </div>
            </div>

            {/* Section 3: Spectral Significance (Wide Span) */}
            <div className="lg:col-span-2 bg-card-bg backdrop-blur-xl border border-white/5 rounded-[2.5rem] p-8 shadow-2xl">
              <div className="flex items-center gap-2 mb-6">
                <Activity className="text-neon-cyan" size={20} />
                <h3 className="text-lg font-bold text-white uppercase tracking-tight">
                  Multi-Domain Diagnostic Mapping
                </h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-center">
                <div className="md:col-span-1 space-y-4">
                  <p className="text-sm text-slate-400 leading-relaxed">
                    By transforming 1D audio into 2D{" "}
                    <strong>Log-Mel Spectrograms</strong>, the system can
                    identify horizontal harmonic bands. Failures manifest as
                    spectral blurring or transient "clicks" that are invisible
                    in the time-domain waveform.
                  </p>
                  <div className="p-4 bg-neon-cyan/5 border border-neon-cyan/10 rounded-xl">
                    <p className="text-[11px] text-neon-cyan font-bold leading-tight">
                      Expert Insight: The Hybrid ConvStem-ViT architecture was
                      specifically chosen to balance local transient extraction
                      with global rhythmic dependencies.
                    </p>
                  </div>
                </div>
                <div className="md:col-span-2 bg-slate-950 rounded-2xl p-3 border border-white/10 shadow-inner">
                  <img
                    src="/dual_domain_analysis_fan_snr0.png"
                    alt="Dual Domain Analysis"
                    className="w-full h-auto rounded-xl shadow-2xl"
                  />
                </div>
              </div>
            </div>
          </div>

          <footer className="mt-12 mb-8 text-center">
            <p className="text-[10px] font-black text-slate-600 uppercase tracking-[0.5em]">
              End of Intelligence Report — MIMII v1.0
            </p>
          </footer>
        </div>
      </main>
    </div>
  );
}
