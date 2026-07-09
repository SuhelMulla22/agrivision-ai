import { useState, useCallback, useEffect } from "react";
import { useDropzone } from "react-dropzone";
import { motion, AnimatePresence } from "framer-motion";
import toast from "react-hot-toast";
import {
  Upload,
  ScanLine,
  Loader2,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  Leaf,
  ArrowLeft,
  Download,
  Clock,
  Shield,
  Pill,
  Bug,
  ChevronDown,
  ChevronUp,
  Languages,
} from "lucide-react";
import { predictDisease } from "../services/api";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const LANGUAGES = [
  { code: "en", label: "English" },
  { code: "hi", label: "हिन्दी" },
  { code: "mr", label: "मराठी" },
];

export default function Analyze() {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const navigate = useNavigate();

  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [language, setLanguage] = useState("en");
  const [showFullInfo, setShowFullInfo] = useState(false);

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setImage(file);
    setImagePreview(URL.createObjectURL(file));
    setResult(null);
    setShowFullInfo(false);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "image/*": [".jpg", ".jpeg", ".png", ".webp"] },
    maxSize: 10 * 1024 * 1024,
    multiple: false,
  });

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      toast.error("Please sign in to analyze crop diseases.");
      navigate("/auth/login");
    }
  }, [isAuthenticated, authLoading, navigate]);

  if (authLoading) {
    return (
      <div className="min-h-[85vh] flex items-center justify-center bg-slate-50">
        <Loader2 className="w-8 h-8 text-brand-600 animate-spin" />
      </div>
    );
  }

  const handleAnalyze = async () => {
    if (!image) return;
    setLoading(true);

    try {
      const data = await predictDisease(image, language);
      setResult(data);
      toast.success("Analysis complete!");
    } catch (err) {
      toast.error(err.message || "Analysis failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setImage(null);
    setImagePreview(null);
    setResult(null);
    setShowFullInfo(false);
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="font-display text-3xl sm:text-4xl font-bold text-slate-900">
            Crop Disease <span className="gradient-text">Detection</span>
          </h1>
          <p className="mt-2 text-slate-600">
            Upload a clear photo of a crop leaf, fruit, or plant part for instant AI-powered diagnosis.
          </p>
          <div className="mt-4 p-4 rounded-xl bg-emerald-50 border border-emerald-200 flex items-start gap-3">
            <Leaf className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-semibold text-emerald-800">Universal Hybrid AI Mode Active</p>
              <p className="text-xs text-emerald-600 mt-0.5">
                Our primary engine uses Gemini 2.5 Flash to support all plants, fruits, and vegetables (including leaves and fruits like Mangoes). It automatically falls back to our local TensorFlow failover model if the API quota is reached.
              </p>
            </div>
          </div>
        </motion.div>

        {/* Language Selector */}
        <div className="flex items-center gap-2 mb-6">
          <Languages className="w-4 h-4 text-slate-500" />
          <span className="text-sm text-slate-500">Language:</span>
          {LANGUAGES.map(({ code, label }) => (
            <button
              key={code}
              onClick={() => setLanguage(code)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                language === code
                  ? "bg-brand-600 text-white shadow-sm"
                  : "bg-white text-slate-600 hover:bg-slate-100 border border-slate-200"
              }`}
            >
              {label}
            </button>
          ))}
        </div>

        <AnimatePresence mode="wait">
          {!result ? (
            /* ========== UPLOAD STATE ========== */
            <motion.div
              key="upload"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="grid lg:grid-cols-2 gap-6"
            >
              {/* Dropzone */}
              <div
                {...getRootProps()}
                className={`glass-card p-8 cursor-pointer transition-all duration-300 ${
                  isDragActive
                    ? "border-brand-500 bg-brand-50/50 shadow-xl shadow-brand-500/10"
                    : "hover:border-brand-300 hover:shadow-lg"
                }`}
              >
                <input {...getInputProps()} />
                <div className="flex flex-col items-center justify-center h-80 gap-4">
                  <div
                    className={`w-16 h-16 rounded-2xl flex items-center justify-center transition-colors ${
                      isDragActive
                        ? "bg-brand-100 text-brand-600"
                        : "bg-slate-100 text-slate-400"
                    }`}
                  >
                    <Upload className="w-8 h-8" />
                  </div>
                  {isDragActive ? (
                    <p className="text-brand-600 font-semibold">
                      Drop the image here...
                    </p>
                  ) : (
                    <div className="text-center">
                      <p className="font-semibold text-slate-700">
                        Drag & drop a leaf image here
                      </p>
                      <p className="text-sm text-slate-500 mt-1">
                        or click to browse · JPG, PNG, WEBP · Max 10MB
                      </p>
                    </div>
                  )}
                </div>
              </div>

              {/* Preview & Analyze */}
              <div className="glass-card p-8 flex flex-col">
                {imagePreview ? (
                  <>
                    <div className="relative flex-1 rounded-xl overflow-hidden bg-slate-100">
                      <img
                        src={imagePreview}
                        alt="Leaf preview"
                        className="w-full h-full max-h-80 object-contain"
                      />
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleReset();
                        }}
                        className="absolute top-3 right-3 p-1.5 bg-white/90 rounded-lg hover:bg-white shadow-sm transition-colors"
                      >
                        <XCircle className="w-5 h-5 text-slate-500" />
                      </button>
                    </div>
                    <div className="mt-4 flex items-center gap-3">
                      <p className="text-sm text-slate-500 truncate flex-1">
                        {image?.name}
                      </p>
                      <span className="text-xs text-slate-400">
                        {(image?.size / 1024 / 1024).toFixed(1)} MB
                      </span>
                    </div>
                    <button
                      onClick={handleAnalyze}
                      disabled={loading}
                      className="btn-primary w-full mt-4 py-4 text-base"
                    >
                      {loading ? (
                        <>
                          <Loader2 className="w-5 h-5 animate-spin" />
                          Analyzing...
                        </>
                      ) : (
                        <>
                          <ScanLine className="w-5 h-5" />
                          Analyze Leaf
                        </>
                      )}
                    </button>
                  </>
                ) : (
                  <div className="flex-1 flex flex-col items-center justify-center text-center gap-3 text-slate-400">
                    <Leaf className="w-12 h-12" />
                    <p className="text-sm">
                      Upload an image to see preview here
                    </p>
                  </div>
                )}
              </div>
            </motion.div>
          ) : (
            /* ========== RESULTS STATE ========== */
            <motion.div
              key="results"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <button
                onClick={handleReset}
                className="btn-secondary mb-6"
              >
                <ArrowLeft className="w-4 h-4" />
                New Analysis
              </button>

              <div className="grid lg:grid-cols-5 gap-6">
                {/* Left: Image + Quick Info */}
                <div className="lg:col-span-2 space-y-4">
                  <div className="glass-card p-4">
                    <img
                      src={imagePreview}
                      alt="Analyzed leaf"
                      className="w-full rounded-xl max-h-64 object-contain bg-slate-50"
                    />
                  </div>

                  {/* Quick Result Card */}
                  <div
                    className={`glass-card p-6 border-l-4 ${
                      result.data.is_healthy
                        ? "border-l-emerald-500"
                        : result.data.severity === "high"
                        ? "border-l-red-500"
                        : result.data.severity === "moderate"
                        ? "border-l-amber-500"
                        : "border-l-blue-500"
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      <div
                        className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${
                          result.data.is_healthy
                            ? "bg-emerald-100 text-emerald-600"
                            : "bg-red-100 text-red-600"
                        }`}
                      >
                        {result.data.is_healthy ? (
                          <CheckCircle2 className="w-5 h-5" />
                        ) : (
                          <AlertTriangle className="w-5 h-5" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-display font-bold text-lg text-slate-900">
                          {result.data.disease}
                        </p>
                        <p className="text-sm text-slate-500 mt-0.5">
                          {result.data.crop}
                        </p>
                        <div className="flex items-center gap-3 mt-3">
                          <div className="flex-1">
                            <div className="flex items-center justify-between text-xs mb-1">
                              <span className="text-slate-500">Confidence</span>
                              <span className="font-semibold text-slate-700">
                                {(result.data.confidence * 100).toFixed(1)}%
                              </span>
                            </div>
                            <div className="w-full bg-slate-100 rounded-full h-2">
                              <motion.div
                                initial={{ width: 0 }}
                                animate={{
                                  width: `${result.data.confidence * 100}%`,
                                }}
                                transition={{ duration: 1, ease: "easeOut" }}
                                className={`h-2 rounded-full ${
                                  result.data.is_healthy
                                    ? "bg-emerald-500"
                                    : "bg-red-500"
                                }`}
                              />
                            </div>
                          </div>
                          {result.data.severity && (
                            <span
                              className={`badge ${
                                result.data.severity === "high"
                                  ? "badge-high"
                                  : result.data.severity === "moderate"
                                  ? "badge-moderate"
                                  : "badge-low"
                              }`}
                            >
                              {result.data.severity}
                            </span>
                          )}
                        </div>
                        <div className="flex items-center gap-4 mt-3 text-xs text-slate-400">
                          <span className="flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            {result.data.processing_time_ms}ms
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Top Predictions */}
                  <div className="glass-card p-5">
                    <h3 className="text-sm font-semibold text-slate-700 mb-3">
                      Top Predictions
                    </h3>
                    <div className="space-y-2">
                      {result.data.top_predictions.map((pred, i) => (
                        <div key={i} className="flex items-center gap-3">
                          <span className="text-xs text-slate-400 w-4">
                            #{i + 1}
                          </span>
                          <div className="flex-1">
                            <div className="flex items-center justify-between text-sm">
                              <span className="text-slate-700 truncate">
                                {pred.disease}
                              </span>
                              <span className="font-medium text-slate-900 ml-2">
                                {(pred.confidence * 100).toFixed(1)}%
                              </span>
                            </div>
                            <div className="w-full bg-slate-100 rounded-full h-1.5 mt-1">
                              <div
                                className="bg-brand-500 h-1.5 rounded-full transition-all duration-700"
                                style={{
                                  width: `${pred.confidence * 100}%`,
                                }}
                              />
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Right: Disease Info */}
                <div className="lg:col-span-3 space-y-4">
                  {/* Disease Description */}
                  <div className="glass-card p-6">
                    <div className="flex items-center gap-2 mb-3">
                      <Bug className="w-5 h-5 text-slate-600" />
                      <h3 className="font-semibold text-slate-900">About This Disease</h3>
                    </div>
                    <p className="text-slate-600 leading-relaxed">
                      {result.data.disease_info.description}
                    </p>
                  </div>

                  {/* Symptoms */}
                  {result.data.disease_info.symptoms?.length > 0 && (
                    <div className="glass-card p-6">
                      <h3 className="font-semibold text-slate-900 mb-3">
                        🔍 Symptoms to Look For
                      </h3>
                      <ul className="space-y-2">
                        {result.data.disease_info.symptoms.map((symptom, i) => (
                          <li
                            key={i}
                            className="flex items-start gap-2 text-sm text-slate-600"
                          >
                            <span className="w-1.5 h-1.5 rounded-full bg-amber-400 mt-1.5 flex-shrink-0" />
                            {symptom}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Treatment */}
                  <div className="glass-card p-6">
                    <div className="flex items-center gap-2 mb-4">
                      <Pill className="w-5 h-5 text-slate-600" />
                      <h3 className="font-semibold text-slate-900">
                        Treatment Recommendations
                      </h3>
                    </div>

                    {/* Toggle */}
                    <button
                      onClick={() => setShowFullInfo(!showFullInfo)}
                      className="flex items-center gap-1 text-sm text-brand-600 font-medium mb-4 hover:text-brand-700"
                    >
                      {showFullInfo ? (
                        <>
                          Show less <ChevronUp className="w-4 h-4" />
                        </>
                      ) : (
                        <>
                          Show all details <ChevronDown className="w-4 h-4" />
                        </>
                      )}
                    </button>

                    {result.data.disease_info.treatment.organic?.length > 0 && (
                      <div className="mb-4">
                        <h4 className="text-sm font-medium text-emerald-700 mb-2 flex items-center gap-1.5">
                          <Leaf className="w-4 h-4" /> Organic / Natural
                        </h4>
                        <ul className="space-y-1.5">
                          {result.data.disease_info.treatment.organic
                            .slice(0, showFullInfo ? undefined : 3)
                            .map((t, i) => (
                              <li
                                key={i}
                                className="flex items-start gap-2 text-sm text-slate-600"
                              >
                                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 flex-shrink-0" />
                                {t}
                              </li>
                            ))}
                        </ul>
                      </div>
                    )}

                    {result.data.disease_info.treatment.chemical?.length > 0 && (
                      <div>
                        <h4 className="text-sm font-medium text-blue-700 mb-2 flex items-center gap-1.5">
                          <Shield className="w-4 h-4" /> Chemical Treatment
                        </h4>
                        <ul className="space-y-1.5">
                          {result.data.disease_info.treatment.chemical
                            .slice(0, showFullInfo ? undefined : 3)
                            .map((t, i) => (
                              <li
                                key={i}
                                className="flex items-start gap-2 text-sm text-slate-600"
                              >
                                <span className="w-1.5 h-1.5 rounded-full bg-blue-400 mt-1.5 flex-shrink-0" />
                                {t}
                              </li>
                            ))}
                        </ul>
                      </div>
                    )}
                  </div>

                  {/* Prevention */}
                  {result.data.disease_info.prevention?.length > 0 && (
                    <div className="glass-card p-6">
                      <h3 className="font-semibold text-slate-900 mb-3">
                        🛡️ Prevention Tips
                      </h3>
                      <ul className="space-y-2">
                        {result.data.disease_info.prevention.map((tip, i) => (
                          <li
                            key={i}
                            className="flex items-start gap-2 text-sm text-slate-600"
                          >
                            <CheckCircle2 className="w-4 h-4 text-brand-500 mt-0.5 flex-shrink-0" />
                            {tip}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Severity Info */}
                  {result.data.disease_info.severity_info && (
                    <div
                      className={`p-5 rounded-2xl border ${
                        result.data.severity === "high"
                          ? "bg-red-50 border-red-200"
                          : result.data.severity === "moderate"
                          ? "bg-amber-50 border-amber-200"
                          : "bg-blue-50 border-blue-200"
                      }`}
                    >
                      <p className="text-sm font-medium text-slate-800">
                        ⚠️ {result.data.disease_info.severity_info}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
