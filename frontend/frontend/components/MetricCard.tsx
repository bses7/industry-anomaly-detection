export default function MetricCard({ label, value, sub, icon, color }: any) {
  const colors: any = {
    cyan: "text-neon-cyan bg-neon-cyan/10 border-neon-cyan/20",
    ruby: "text-neon-ruby bg-neon-ruby/10 border-neon-ruby/20",
    emerald: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
    purple: "text-purple-400 bg-purple-500/10 border-purple-500/20",
  };

  return (
    <div className="bg-card-bg backdrop-blur-md border border-white/5 p-5 rounded-[2rem] flex items-center gap-5">
      <div
        className={`w-12 h-12 rounded-2xl flex items-center justify-center border ${colors[color]}`}
      >
        {icon}
      </div>
      <div>
        <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">
          {label}
        </p>
        <h4 className="text-2xl font-black text-white leading-none my-1">
          {value}
        </h4>
        <p className="text-[10px] font-bold text-slate-600 uppercase">{sub}</p>
      </div>
    </div>
  );
}
