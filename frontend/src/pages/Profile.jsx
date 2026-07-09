import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import {
  User,
  Mail,
  MapPin,
  Calendar,
  Shield,
  Activity,
  Heart,
  AlertTriangle,
  LogOut,
  ArrowRight,
  Loader2,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] }
  }
};

export default function Profile() {
  const { user, isAuthenticated, loading: authLoading, logout } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      navigate("/auth/login");
    }
  }, [isAuthenticated, authLoading, navigate]);

  useEffect(() => {
    if (isAuthenticated) {
      fetchStats();
    }
  }, [isAuthenticated]);

  const fetchStats = async () => {
    try {
      const response = await api.get("/api/v1/analytics");
      setStats(response.data.data);
    } catch (err) {
      console.error("Failed to load profile analytics", err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  if (authLoading || (loading && isAuthenticated)) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center bg-slate-50">
        <Loader2 className="w-8 h-8 text-brand-600 animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 py-10">
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="max-w-4xl mx-auto px-4 sm:px-6"
      >
        {/* Profile Card Header */}
        <motion.div
          variants={cardVariants}
          className="glass-card p-6 sm:p-8 flex flex-col sm:flex-row items-center gap-6 shadow-sm mb-6"
        >
          {/* Initial Avatar */}
          <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-brand-600 to-emerald-500 text-white flex items-center justify-center text-4xl font-black shadow-md border-4 border-white shrink-0">
            {user?.name ? user.name[0].toUpperCase() : <User className="w-12 h-12" />}
          </div>

          <div className="text-center sm:text-left flex-1">
            <h1 className="font-display text-2xl sm:text-3xl font-extrabold text-slate-900">
              {user?.name || "Farmer"}
            </h1>
            <p className="text-slate-500 text-sm mt-1 flex items-center justify-center sm:justify-start gap-1.5">
              <Shield className="w-4 h-4 text-brand-500" />
              Verified AgriVision User
            </p>

            <div className="grid sm:grid-cols-2 gap-x-6 gap-y-2 mt-4 text-sm text-slate-600">
              <div className="flex items-center justify-center sm:justify-start gap-2">
                <Mail className="w-4.5 h-4.5 text-slate-400" />
                <span>{user?.email || "No email linked"}</span>
              </div>
              <div className="flex items-center justify-center sm:justify-start gap-2">
                <MapPin className="w-4.5 h-4.5 text-slate-400" />
                <span>{user?.location || "India"}</span>
              </div>
              <div className="flex items-center justify-center sm:justify-start gap-2 sm:col-span-2">
                <Calendar className="w-4.5 h-4.5 text-slate-400" />
                <span>
                  Member since{" "}
                  {user?.created_at
                    ? new Date(user.created_at).toLocaleDateString("en-IN", {
                        year: "numeric",
                        month: "long",
                        day: "numeric",
                      })
                    : "June 2026"}
                </span>
              </div>
            </div>
          </div>

          <button
            onClick={handleLogout}
            className="btn-secondary py-2 px-4 text-xs font-semibold flex items-center gap-1.5 self-center sm:self-start border border-red-200 text-rose-600 hover:bg-rose-50 hover:border-rose-300 transition-colors"
          >
            <LogOut className="w-3.5 h-3.5" />
            Sign Out
          </button>
        </motion.div>

        {/* Statistics Grid */}
        <motion.div
          variants={cardVariants}
          className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-6"
        >
          {/* Card 1: Total Scans */}
          <div className="glass-card p-6 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:scale-110 transition-transform">
              <Activity className="w-16 h-16 text-brand-600" />
            </div>
            <p className="text-sm font-semibold text-slate-400 uppercase tracking-wider">
              Total Scans
            </p>
            <p className="text-3xl font-extrabold text-slate-800 mt-2">
              {stats?.total_predictions || 0}
            </p>
            <p className="text-xs text-slate-500 mt-1">
              Scanned this month: {stats?.predictions_this_month || 0}
            </p>
          </div>

          {/* Card 2: Healthy Crops */}
          <div className="glass-card p-6 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:scale-110 transition-transform">
              <Heart className="w-16 h-16 text-emerald-500" />
            </div>
            <p className="text-sm font-semibold text-slate-400 uppercase tracking-wider">
              Healthy Crops
            </p>
            <p className="text-3xl font-extrabold text-emerald-600 mt-2">
              {stats?.healthy_count || 0}
            </p>
            <p className="text-xs text-slate-500 mt-1">
              No pathogens or pests found
            </p>
          </div>

          {/* Card 3: Diseased Crops */}
          <div className="glass-card p-6 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:scale-110 transition-transform">
              <AlertTriangle className="w-16 h-16 text-rose-500" />
            </div>
            <p className="text-sm font-semibold text-slate-400 uppercase tracking-wider">
              Pathogen Attacks
            </p>
            <p className="text-3xl font-extrabold text-rose-600 mt-2">
              {stats?.diseased_count || 0}
            </p>
            <p className="text-xs text-slate-500 mt-1">
              Requiring organic/chemical care
            </p>
          </div>
        </motion.div>

        {/* Details & Actions Section */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Left panel: Info & Preferences */}
          <motion.div
            variants={cardVariants}
            className="glass-card p-6 shadow-sm"
          >
            <h3 className="font-display text-lg font-bold text-slate-900 mb-4 border-b border-slate-100 pb-3">
              🌾 Account Preferences
            </h3>
            <div className="space-y-4">
              <div>
                <p className="text-xs text-slate-400 font-medium uppercase tracking-wider">
                  Preferred Region
                </p>
                <p className="text-sm text-slate-800 font-semibold mt-0.5">
                  {user?.location || "Not Specified (Defaulting to India)"}
                </p>
              </div>
              <div>
                <p className="text-xs text-slate-400 font-medium uppercase tracking-wider">
                  Universal Analysis Mode
                </p>
                <p className="text-sm text-emerald-600 font-bold mt-0.5">
                  Always Active (Online / Offline Hybrid)
                </p>
              </div>
              <div>
                <p className="text-xs text-slate-400 font-medium uppercase tracking-wider">
                  Frequent Crop Inspected
                </p>
                <p className="text-sm text-slate-800 font-semibold mt-0.5 capitalize">
                  {stats?.most_common_crop || "None Yet"}
                </p>
              </div>
            </div>
          </motion.div>

          {/* Right panel: Next actions */}
          <motion.div
            variants={cardVariants}
            className="glass-card p-6 shadow-sm flex flex-col justify-between"
          >
            <div>
              <h3 className="font-display text-lg font-bold text-slate-900 mb-4 border-b border-slate-100 pb-3">
                🔍 Next Steps
              </h3>
              <p className="text-sm text-slate-600 leading-relaxed mb-6">
                Take a new leaf diagnosis snapshot, or browse detailed statistics on your personal crop analytics dashboard.
              </p>
            </div>

            <div className="flex flex-col gap-3">
              <a
                href="/analyze"
                className="btn-primary py-3 px-4 text-sm font-semibold flex items-center justify-center gap-1.5 shadow-sm hover:shadow"
              >
                Scan A New Crop Leaf <ArrowRight className="w-4 h-4" />
              </a>
              <a
                href="/dashboard"
                className="btn-secondary py-3 px-4 text-sm font-semibold text-center border border-slate-200 hover:bg-slate-100 transition-colors"
              >
                View Analytics Dashboard
              </a>
            </div>
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
}
