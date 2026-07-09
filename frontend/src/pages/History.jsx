import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Clock,
  Leaf,
  AlertTriangle,
  CheckCircle2,
  Loader2,
  ChevronLeft,
  ChevronRight,
  ScanLine,
  X,
  Shield,
  Pill,
  Bug,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";

export default function History() {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const [history, setHistory] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [selectedItem, setSelectedItem] = useState(null);
  const limit = 10;

  useEffect(() => {
    if (!authLoading) {
      if (isAuthenticated) {
        fetchHistory();
      } else {
        setLoading(false);
      }
    }
  }, [isAuthenticated, page, authLoading]);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const response = await api.get("/api/v1/history", {
        params: { limit, offset: page * limit },
      });
      setHistory(response.data.data.predictions);
      setTotal(response.data.data.total);
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
            <Clock className="w-10 h-10 text-brand-600" />
          </div>
          <h2 className="font-display text-2xl font-bold text-slate-900 mb-2">
            Sign in to view history
          </h2>
          <p className="text-slate-500 mb-6">
            Your past crop analyses are saved when you're signed in.
          </p>
          <a href="/auth/login" className="btn-primary">
            Sign In
          </a>
        </motion.div>
      </div>
    );
  }

  const totalPages = Math.ceil(total / limit);

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="font-display text-3xl sm:text-4xl font-bold text-slate-900">
            Analysis <span className="gradient-text">History</span>
          </h1>
          <p className="mt-2 text-slate-600">
            Review your past crop disease analyses.{" "}
            {total > 0 && (
              <span className="text-slate-500">
                ({total} total)
              </span>
            )}
          </p>
        </motion.div>

        {loading ? (
          <div className="flex justify-center py-20">
            <Loader2 className="w-8 h-8 animate-spin text-brand-600" />
          </div>
        ) : history.length > 0 ? (
          <>
            <div className="space-y-4">
              {history.map((item, i) => (
                <motion.div
                  key={item.id || i}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.05 }}
                  onClick={() => setSelectedItem(item)}
                  className={`glass-card p-5 border-l-4 cursor-pointer hover:shadow-md hover:scale-[1.01] transition-all ${
                    item.is_healthy
                      ? "border-l-emerald-500"
                      : item.severity === "high"
                      ? "border-l-red-500"
                      : item.severity === "moderate"
                      ? "border-l-amber-500"
                      : "border-l-blue-500"
                  }`}
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex items-start gap-3 flex-1 min-w-0">
                      <div
                        className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${
                          item.is_healthy
                            ? "bg-emerald-100 text-emerald-600"
                            : "bg-red-100 text-red-600"
                        }`}
                      >
                        {item.is_healthy ? (
                          <CheckCircle2 className="w-5 h-5" />
                        ) : (
                          <AlertTriangle className="w-5 h-5" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-semibold text-slate-900 truncate">
                          {item.disease || "Unknown"}
                        </p>
                        <p className="text-sm text-slate-500">{item.crop}</p>
                        <div className="flex items-center gap-3 mt-2 flex-wrap">
                          <span className="text-xs text-slate-400 flex items-center gap-1">
                            <ScanLine className="w-3 h-3" />
                            {((item.confidence || 0) * 100).toFixed(1)}%
                            confidence
                          </span>
                          {item.severity && (
                            <span
                              className={`badge ${
                                item.severity === "high"
                                  ? "badge-high"
                                  : item.severity === "moderate"
                                  ? "badge-moderate"
                                  : "badge-low"
                              }`}
                            >
                              {item.severity}
                            </span>
                          )}
                          <span className="text-xs text-slate-400 flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            {item.processing_time_ms}ms
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="text-right flex-shrink-0">
                      <p className="text-xs text-slate-400">
                        {item.created_at
                          ? new Date(item.created_at).toLocaleDateString(
                              "en-IN",
                              {
                                day: "numeric",
                                month: "short",
                                year: "numeric",
                              }
                            )
                          : ""}
                      </p>
                      <p className="text-xs text-slate-400 mt-0.5">
                        {item.created_at
                          ? new Date(item.created_at).toLocaleTimeString(
                              "en-IN",
                              { hour: "2-digit", minute: "2-digit" }
                            )
                          : ""}
                      </p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-center gap-4 mt-8">
                <button
                  onClick={() => setPage(Math.max(0, page - 1))}
                  disabled={page === 0}
                  className="btn-secondary py-2 px-4 text-sm disabled:opacity-40"
                >
                  <ChevronLeft className="w-4 h-4" /> Previous
                </button>
                <span className="text-sm text-slate-500">
                  Page {page + 1} of {totalPages}
                </span>
                <button
                  onClick={() => setPage(Math.min(totalPages - 1, page + 1))}
                  disabled={page >= totalPages - 1}
                  className="btn-secondary py-2 px-4 text-sm disabled:opacity-40"
                >
                  Next <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            )}
          </>
        ) : (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card p-12 text-center"
          >
            <Clock className="w-16 h-16 text-slate-300 mx-auto mb-4" />
            <h3 className="font-display text-xl font-bold text-slate-700 mb-2">
              No analyses yet
            </h3>
            <p className="text-slate-500 mb-6">
              Your analysis history will appear here after you analyze a crop
              leaf.
            </p>
            <a href="/analyze" className="btn-primary">
              <Leaf className="w-4 h-4" /> Start Analyzing
            </a>
          </motion.div>
        )}

        {/* Detail Modal Overlay */}
        <AnimatePresence>
          {selectedItem && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelectedItem(null)}
              className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 sm:p-6 overflow-y-auto"
            >
              <motion.div
                initial={{ opacity: 0, scale: 0.95, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95, y: 20 }}
                onClick={(e) => e.stopPropagation()}
                className="bg-white rounded-2xl shadow-xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col"
              >
                {/* Header */}
                <div className="p-6 border-b border-slate-100 flex items-center justify-between bg-slate-50">
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                        selectedItem.is_healthy
                          ? "bg-emerald-100 text-emerald-600"
                          : "bg-red-100 text-red-600"
                      }`}
                    >
                      {selectedItem.is_healthy ? (
                        <CheckCircle2 className="w-5 h-5" />
                      ) : (
                        <AlertTriangle className="w-5 h-5" />
                      )}
                    </div>
                    <div>
                      <h2 className="font-display text-xl font-bold text-slate-955">
                        {selectedItem.disease || "Unknown Disease"}
                      </h2>
                      <p className="text-sm text-slate-500">{selectedItem.crop}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => setSelectedItem(null)}
                    className="p-2 hover:bg-slate-200 rounded-lg transition-colors text-slate-400 hover:text-slate-600"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto p-6 grid md:grid-cols-2 gap-6">
                  {/* Left: Image & Stats */}
                  <div className="flex flex-col gap-4">
                    <div className="aspect-video sm:aspect-square w-full rounded-xl overflow-hidden bg-slate-100 border border-slate-200 relative">
                      {selectedItem.image_url ? (
                        <img
                          src={selectedItem.image_url}
                          alt="Diagnosis Crop"
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="w-full h-full flex flex-col items-center justify-center text-slate-400 gap-2">
                          <Leaf className="w-12 h-12" />
                          <span className="text-sm">Image not available</span>
                        </div>
                      )}
                      <div className="absolute bottom-3 left-3 bg-black/60 backdrop-blur-sm text-white px-3 py-1.5 rounded-lg text-xs flex items-center gap-1.5">
                        <Clock className="w-3.5 h-3.5" />
                        {selectedItem.created_at
                          ? new Date(selectedItem.created_at).toLocaleDateString("en-IN", {
                              day: "numeric",
                              month: "short",
                              year: "numeric",
                            })
                          : ""}
                      </div>
                    </div>

                    <div className="grid grid-cols-3 gap-3">
                      <div className="bg-slate-50 p-3 rounded-xl text-center border border-slate-100">
                        <p className="text-xs text-slate-400 font-medium">Confidence</p>
                        <p className="text-lg font-bold text-slate-800 mt-1">
                          {((selectedItem.confidence || 0) * 100).toFixed(1)}%
                        </p>
                      </div>
                      <div className="bg-slate-50 p-3 rounded-xl text-center border border-slate-100">
                        <p className="text-xs text-slate-400 font-medium">Severity</p>
                        <p className="text-lg font-bold text-slate-800 mt-1 capitalize">
                          {selectedItem.severity || "None"}
                        </p>
                      </div>
                      <div className="bg-slate-50 p-3 rounded-xl text-center border border-slate-100">
                        <p className="text-xs text-slate-400 font-medium">Status</p>
                        <p
                          className={`text-lg font-bold mt-1 ${
                            selectedItem.is_healthy ? "text-emerald-600" : "text-rose-600"
                          }`}
                        >
                          {selectedItem.is_healthy ? "Healthy" : "Diseased"}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Right: Detailed Diagnosis */}
                  <div className="flex flex-col gap-6">
                    {selectedItem.disease_info ? (
                      <>
                        <div>
                          <h4 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-2">
                            Description
                          </h4>
                          <p className="text-sm text-slate-600 leading-relaxed bg-slate-50 p-4 rounded-xl border border-slate-100">
                            {selectedItem.disease_info.description}
                          </p>
                        </div>

                        {selectedItem.disease_info.symptoms && selectedItem.disease_info.symptoms.length > 0 && (
                          <div>
                            <h4 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                              <Bug className="w-4 h-4 text-rose-500" /> Symptoms
                            </h4>
                            <ul className="list-disc list-inside text-sm text-slate-600 space-y-1.5 pl-1">
                              {selectedItem.disease_info.symptoms.map((s, idx) => (
                                <li key={idx} className="leading-relaxed">{s}</li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {selectedItem.disease_info.treatment && (
                          <div>
                            <h4 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                              <Pill className="w-4 h-4 text-emerald-500" /> Treatments
                            </h4>
                            <div className="space-y-3">
                              {selectedItem.disease_info.treatment.organic && selectedItem.disease_info.treatment.organic.length > 0 && (
                                <div className="bg-emerald-50/50 p-4 rounded-xl border border-emerald-100">
                                  <p className="text-xs font-bold text-emerald-800 uppercase mb-2">Organic</p>
                                  <ul className="list-disc list-inside text-xs text-emerald-700 space-y-1">
                                    {selectedItem.disease_info.treatment.organic.map((t, idx) => (
                                      <li key={idx}>{t}</li>
                                    ))}
                                  </ul>
                                </div>
                              )}
                              {selectedItem.disease_info.treatment.chemical && selectedItem.disease_info.treatment.chemical.length > 0 && (
                                <div className="bg-blue-50/50 p-4 rounded-xl border border-blue-100">
                                  <p className="text-xs font-bold text-blue-800 uppercase mb-2">Chemical</p>
                                  <ul className="list-disc list-inside text-xs text-blue-700 space-y-1">
                                    {selectedItem.disease_info.treatment.chemical.map((t, idx) => (
                                      <li key={idx}>{t}</li>
                                    ))}
                                  </ul>
                                </div>
                              )}
                            </div>
                          </div>
                        )}
                        
                        {selectedItem.disease_info.prevention && selectedItem.disease_info.prevention.length > 0 && (
                          <div>
                            <h4 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                              <Shield className="w-4 h-4 text-brand-500" /> Prevention
                            </h4>
                            <ul className="list-disc list-inside text-sm text-slate-600 space-y-1.5 pl-1">
                              {selectedItem.disease_info.prevention.map((p, idx) => (
                                <li key={idx} className="leading-relaxed">{p}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </>
                    ) : (
                      <div className="h-full flex flex-col items-center justify-center text-center text-slate-400 py-12 gap-2">
                        <Leaf className="w-12 h-12 text-slate-300" />
                        <p className="text-sm font-medium">Detailed dynamic guidelines not available for this legacy record.</p>
                        <p className="text-xs max-w-xs">This prediction was processed before dynamic details were saved in your database.</p>
                      </div>
                    )}
                  </div>
                </div>

                {/* Footer */}
                <div className="p-4 border-t border-slate-100 bg-slate-50 flex justify-end">
                  <button
                    onClick={() => setSelectedItem(null)}
                    className="btn-secondary py-2 px-4 text-sm"
                  >
                    Close
                  </button>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
