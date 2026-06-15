"use client";
import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Database,
  ChevronLeft,
  ChevronRight,
  Activity,
} from "lucide-react";

export default function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const pathname = usePathname();

  const menuItems = [
    { icon: <LayoutDashboard size={20} />, label: "Overview", href: "/" },
    { icon: <Database size={20} />, label: "Datasets", href: "/datasets" },
  ];

  return (
    <aside
      className={`relative flex flex-col border-r border-white/5 bg-panel-bg p-4 transition-all duration-300 ease-in-out z-20 ${isCollapsed ? "w-20" : "w-64"}`}
    >
      <button
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="absolute -right-3 top-10 flex h-6 w-6 items-center justify-center rounded-full border border-slate-700 bg-slate-900 text-neon-cyan shadow-[0_0_10px_rgba(34,211,238,0.3)] hover:scale-110 transition-transform"
      >
        {isCollapsed ? <ChevronRight size={14} /> : <ChevronLeft size={14} />}
      </button>

      <div
        className={`flex items-center gap-3 mb-12 ${isCollapsed ? "justify-center" : "px-2"}`}
      >
        <div className="flex-shrink-0 w-9 h-9 bg-neon-cyan rounded-xl flex items-center justify-center shadow-[0_0_20px_rgba(34,211,238,0.4)]">
          <Activity className="text-panel-bg" size={22} />
        </div>
        {!isCollapsed && (
          <span className="text-xl font-black text-white tracking-tighter uppercase">
            AnomalyDetect
          </span>
        )}
      </div>

      <nav className="space-y-2 flex-1">
        {menuItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link key={item.href} href={item.href}>
              <div
                className={`flex items-center rounded-xl cursor-pointer transition-all group relative mb-2 ${isCollapsed ? "justify-center p-3" : "gap-4 p-3"} ${
                  isActive
                    ? "bg-neon-cyan/10 text-neon-cyan"
                    : "text-slate-500 hover:bg-white/5 hover:text-slate-200"
                }`}
              >
                <div className="flex-shrink-0">{item.icon}</div>
                {!isCollapsed && (
                  <span className="font-bold text-sm tracking-wide">
                    {item.label}
                  </span>
                )}
                {isActive && (
                  <div
                    className={`bg-neon-cyan rounded-full shadow-[0_0_8px_#22d3ee] ${isCollapsed ? "absolute right-2 top-2 w-1.5 h-1.5" : "ml-auto w-1.5 h-1.5"}`}
                  />
                )}
              </div>
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto pt-6 border-t border-white/5">
        <div
          className={`bg-slate-900/40 rounded-2xl border border-white/5 transition-all ${isCollapsed ? "p-2" : "p-4 flex items-center gap-3"}`}
        >
          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-tr from-neon-cyan to-blue-600 shadow-lg" />
          {!isCollapsed && (
            <div>
              <p className="text-xs font-black text-white uppercase">Admin</p>
              <p className="text-[10px] text-slate-500 font-bold uppercase tracking-tighter">
                System Admin
              </p>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
}
