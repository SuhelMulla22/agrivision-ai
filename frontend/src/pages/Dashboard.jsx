import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  BarChart3,
  Activity,
  Leaf,
  Bug,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  Clock,
  Loader2,
} from "lucide-react";
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";

const COLORS = [
  "#16a34a", "#ef4444", "#f59e0b", "#3b82f6", "#8b5cf6",
  "#ec4899", "#14b8a6", "#f97316", "#6366f1", "#84cc16",
];

const SEVERITY_COLORS = {
  high: "#ef4444",
  moderate: "#f59e0b",
  low: "#3b82f6",
};

export default function Dashboard() {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading) {
      if (isAuthenticated) {
        fetchAnalytics();
      } else {
        setLoading(false);
      }
    }
  }, [isAuthenticated, authLoading]);

  const fetchAnalytics = async () => {
    try {
      const response = await api.get("/api/v1/analytics");
      setAnalytics(response.data.data);
    } catch {
      // Will show empty state
    } finally {
      setLoading(false);
    }
  };

  if (authLoading || (loading && isAuthenticated)) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-brand-600" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center"
        >
          <div className="w-20 h-20 bg-brand-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <BarChart3 className="w-10 h-10 text-brand-600" />
          </div>
          <h2 className="font-display text-2xl font-bold text-slate-900 mb-2">
            Sign in to view your dashboard
          </h2>
          <p className="text-slate-500 mb-6">
            Track your crop analysis history and insights
          </p>
          <a href="/auth/login" className="btn-primary">
            Sign In
          </a>
        </motion.div>
      </div>
    );
  }

  const stats = [
    {
      label: "Total Analyses",
      value: analytics?.total_predictions || 0,
      icon: Activity,
      color: "text-brand-600",
      bg: "bg-brand-100",
    },
    {
      label: "Healthy Detected",
      value: analytics?.healthy_count || 0,
      icon: CheckCircle2,
      color: "text-emerald-600",
      bg: "bg-emerald-100",
    },
    {
      label: "Diseases Found",
      value: analytics?.diseased_count || 0,
      icon: Bug,
      color: "text-red-600",
      bg: "bg-red-100",
    },
    {
      label: "This Month",
      value: analytics?.predictions_this_month || 0,
      icon: TrendingUp,
      color: "text-blue-600",
      bg: "bg-blue-100",
    },
  ];

  const severityData = analytics?.severity_distribution
    ? Object.entries(analytics.severity_distribution)
        .filter(([_, count]) => count > 0)
        .map(([name, count]) => ({
          name: name.charAt(0).toUpperCase() + name.slice(1),
          value: count,
        }))
    : [];

  const cropData = analytics?.crop_distribution || [];
  const diseaseData = (analytics?.disease_distribution || []).slice(0, 6);

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="font-display text-3xl sm:text-4xl font-bold text-slate-900">
            Your <span className="gradient-text">Dashboard</span>
          </h1>
          <p className="mt-2 text-slate-600">
            Track your crop analysis activity and insights.
          </p>
        </motion.div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {stats.map((stat, i) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="glass-card p-5"
            >
              <div className="flex items-center gap-3">
                <div
                  className={`w-10 h-10 rounded-xl flex items-center justify-center ${stat.bg}`}
                >
                  <stat.icon className={`w-5 h-5 ${stat.color}`} />
                </div>
                <div>
                  <p className="text-2xl font-bold text-slate-900">
                    {stat.value}
                  </p>
                  <p className="text-xs text-slate-500">{stat.label}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {analytics?.total_predictions > 0 ? (
          <div className="grid lg:grid-cols-2 gap-6">
            {/* Crop Distribution */}
            {cropData.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="glass-card p-6 shadow-sm hover:shadow-md transition-shadow"
              >
                <h3 className="font-semibold text-slate-900 mb-4 flex items-center gap-2">
                  <Leaf className="w-5 h-5 text-emerald-600" /> Crops Analyzed
                </h3>
                <ResponsiveContainer width="100%" height={260}>
                  <BarChart data={cropData}>
                    <defs>
                      <linearGradient id="cropBarGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#10b981" stopOpacity={0.95}/>
                        <stop offset="100%" stopColor="#059669" stopOpacity={0.75}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                    <XAxis
                      dataKey="name"
                      axisLine={false}
                      tickLine={false}
                      tick={{ fill: "#64748b", fontSize: 12 }}
                    />
                    <YAxis
                      axisLine={false}
                      tickLine={false}
                      tick={{ fill: "#64748b", fontSize: 12 }}
                    />
                    <Tooltip
                      cursor={{ fill: '#f1f5f9', opacity: 0.4 }}
                      contentStyle={{
                        background: "rgba(255, 255, 255, 0.95)",
                        border: "none",
                        boxShadow: "0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05)",
                        borderRadius: "16px",
                        padding: "12px",
                      }}
                    />
                    <Bar dataKey="count" fill="url(#cropBarGrad)" radius={[8, 8, 0, 0]} maxBarSize={45} />
                  </BarChart>
                </ResponsiveContainer>
              </motion.div>
            )}

            {/* Severity Distribution */}
            {severityData.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="glass-card p-6 shadow-sm hover:shadow-md transition-shadow"
              >
                <h3 className="font-semibold text-slate-900 mb-4 flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-amber-500" /> Severity Distribution
                </h3>
                <div className="relative flex justify-center items-center">
                  <ResponsiveContainer width="100%" height={260}>
                    <PieChart>
                      <Pie
                        data={severityData}
                        cx="50%"
                        cy="50%"
                        innerRadius={70}
                        outerRadius={95}
                        paddingAngle={5}
                        dataKey="value"
                      >
                        {severityData.map((entry, i) => (
                          <Cell
                            key={i}
                            fill={
                              SEVERITY_COLORS[entry.name.toLowerCase()] ||
                              COLORS[i]
                            }
                          />
                        ))}
                      </Pie>
                      <Tooltip
                        contentStyle={{
                          background: "rgba(255, 255, 255, 0.95)",
                          border: "none",
                          boxShadow: "0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05)",
                          borderRadius: "16px",
                        }}
                      />
                      <Legend iconType="circle" layout="horizontal" align="center" verticalAlign="bottom" />
                    </PieChart>
                  </ResponsiveContainer>
                  <div className="absolute flex flex-col items-center justify-center pointer-events-none mb-6">
                    <span className="text-3xl font-extrabold text-slate-800">
                      {severityData.reduce((acc, curr) => acc + curr.value, 0)}
                    </span>
                    <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">
                      Total Issues
                    </span>
                  </div>
                </div>
              </motion.div>
            )}

            {/* Top Diseases */}
            {diseaseData.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="glass-card p-6 lg:col-span-2 shadow-sm hover:shadow-md transition-shadow"
              >
                <h3 className="font-semibold text-slate-900 mb-4 flex items-center gap-2">
                  <Bug className="w-5 h-5 text-red-500" /> Most Detected Diseases
                </h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={diseaseData} layout="vertical">
                    <defs>
                      <linearGradient id="diseaseBarGrad" x1="0" y1="0" x2="1" y2="0">
                        <stop offset="0%" stopColor="#f43f5e" stopOpacity={0.95}/>
                        <stop offset="100%" stopColor="#b91c1c" stopOpacity={0.75}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
                    <XAxis type="number" axisLine={false} tickLine={false} tick={{ fill: "#64748b", fontSize: 12 }} />
                    <YAxis
                      dataKey="name"
                      type="category"
                      width={150}
                      axisLine={false}
                      tickLine={false}
                      tick={{ fill: "#64748b", fontSize: 11 }}
                    />
                    <Tooltip
                      cursor={{ fill: '#f1f5f9', opacity: 0.4 }}
                      contentStyle={{
                        background: "rgba(255, 255, 255, 0.95)",
                        border: "none",
                        boxShadow: "0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05)",
                        borderRadius: "16px",
                        padding: "12px",
                      }}
                    />
                    <Bar dataKey="count" fill="url(#diseaseBarGrad)" radius={[0, 8, 8, 0]} maxBarSize={25} />
                  </BarChart>
                </ResponsiveContainer>
              </motion.div>
            )}
          </div>
        ) : (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card p-12 text-center"
          >
            <Activity className="w-16 h-16 text-slate-300 mx-auto mb-4" />
            <h3 className="font-display text-xl font-bold text-slate-700 mb-2">
              No analyses yet
            </h3>
            <p className="text-slate-500 mb-6">
              Start analyzing crop leaves to see your insights here.
            </p>
            <a href="/analyze" className="btn-primary">
              <Leaf className="w-4 h-4" /> Start Analyzing
            </a>
          </motion.div>
        )}
      </div>
    </div>
  );
}
