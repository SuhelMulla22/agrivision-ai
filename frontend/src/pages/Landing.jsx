import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ScanLine,
  Zap,
  Shield,
  Languages,
  ArrowRight,
  Upload,
  BarChart3,
  Sprout,
  Users,
  Globe,
} from "lucide-react";

const fadeUp = {
  hidden: { opacity: 0, y: 10 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.05, duration: 0.3, ease: "easeOut" },
  }),
};

const stats = [
  { value: "Universal", label: "Crops Supported" },
  { value: "Zero-Shot", label: "Diseases Detected" },
  { value: "95.85%", label: "Local Accuracy" },
  { value: "100%", label: "Uptime (Hybrid Cascade)" },
];

const features = [
  {
    icon: ScanLine,
    title: "Instant Detection",
    desc: "Upload a leaf photo and get disease diagnosis in under 2 seconds.",
    color: "text-brand-600 bg-brand-50",
  },
  {
    icon: Languages,
    title: "Multilingual",
    desc: "Full support in English, Hindi, and Marathi for local farmers.",
    color: "text-blue-600 bg-blue-50",
  },
  {
    icon: Shield,
    title: "Treatment Advice",
    desc: "Organic and chemical treatment recommendations for every disease.",
    color: "text-amber-600 bg-amber-50",
  },
  {
    icon: Zap,
    title: "Powered by AI",
    desc: "Built on Google Gemini 2.5 Flash API with local model fallback.",
    color: "text-purple-600 bg-purple-50",
  },
];

const steps = [
  {
    step: "01",
    icon: Upload,
    title: "Upload Photo",
    desc: "Take a clear photo of the affected crop leaf and upload it.",
  },
  {
    step: "02",
    icon: Zap,
    title: "AI Analysis",
    desc: "Our hybrid vision models analyze the image in milliseconds.",
  },
  {
    step: "03",
    icon: BarChart3,
    title: "Get Results",
    desc: "Receive disease diagnosis with severity, treatment, and prevention tips.",
  },
];

export default function Landing() {
  return (
    <div className="overflow-hidden">
      {/* ========== HERO ========== */}
      <section className="relative bg-hero-pattern">
        {/* Background decoration */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-gradient-radial from-brand-200/30 to-transparent rounded-full blur-3xl" />
          <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-gradient-radial from-emerald-200/20 to-transparent rounded-full blur-3xl" />
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-24 sm:pt-28 sm:pb-32">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left — Text */}
            <motion.div
              initial="hidden"
              animate="visible"
              variants={fadeUp}
            >
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand-50 border border-brand-200 text-brand-700 text-sm font-medium mb-6">
                <Sprout className="w-4 h-4" />
                AI for Indian Agriculture
              </div>

              <h1 className="font-display text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 leading-tight">
                Detect Crop Diseases
                <br />
                <span className="gradient-text">in Seconds</span>
              </h1>

              <p className="mt-6 text-lg text-slate-600 leading-relaxed max-w-lg">
                Upload a photo of any crop leaf — our AI instantly identifies
                the disease, assesses severity, and provides treatment
                recommendations in{" "}
                <span className="font-semibold text-slate-900">
                  English, Hindi, and Marathi
                </span>
                .
              </p>

              <div className="mt-8 flex flex-col sm:flex-row gap-3">
                <Link to="/analyze" className="btn-primary text-base px-8 py-4">
                  <ScanLine className="w-5 h-5" />
                  Analyze a Leaf
                  <ArrowRight className="w-4 h-4" />
                </Link>
                <Link to="/about" className="btn-secondary text-base px-8 py-4">
                  Learn More
                </Link>
              </div>

              {/* Trust badges */}
              <div className="mt-8 flex items-center gap-6 text-sm text-slate-500">
                <span className="flex items-center gap-1.5">
                  <Globe className="w-4 h-4" /> Universal Crops
                </span>
                <span className="flex items-center gap-1.5">
                  <Shield className="w-4 h-4" /> Any Disease
                </span>
                <span className="flex items-center gap-1.5">
                  <Users className="w-4 h-4" /> Free & Open
                </span>
              </div>
            </motion.div>

            {/* Right — Hero Illustration / Upload Preview */}
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.3, duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
              className="relative"
            >
              <div className="glass-card p-8 max-w-md mx-auto">
                <div className="w-full h-64 bg-gradient-to-br from-brand-50 to-emerald-50 rounded-xl border-2 border-dashed border-brand-300 flex flex-col items-center justify-center gap-4 text-brand-600">
                  <div className="w-16 h-16 rounded-2xl bg-brand-100 flex items-center justify-center">
                    <ScanLine className="w-8 h-8 text-brand-600" />
                  </div>
                  <div className="text-center">
                    <p className="font-semibold text-brand-700">
                      Drop a leaf image here
                    </p>
                    <p className="text-sm text-brand-500 mt-1">
                      or click to browse
                    </p>
                  </div>
                </div>

                {/* Mock result card */}
                <div className="mt-6 p-4 bg-emerald-50 rounded-xl border border-emerald-200">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-semibold text-emerald-800">
                      Tomato — Late Blight
                    </span>
                    <span className="badge-high">High</span>
                  </div>
                  <div className="w-full bg-emerald-200 rounded-full h-2">
                    <div
                      className="bg-emerald-600 h-2 rounded-full"
                      style={{ width: "96.7%" }}
                    />
                  </div>
                  <p className="text-xs text-emerald-600 mt-1.5">
                    Confidence: 96.7% · Detected in 847ms
                  </p>
                </div>
              </div>

              {/* Floating badges */}
              <motion.div
                animate={{ y: [0, -8, 0] }}
                transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                className="absolute -top-4 -right-4 glass-card px-4 py-2.5 shadow-xl"
              >
                <span className="text-2xl">🌾</span>
              </motion.div>
              <motion.div
                animate={{ y: [0, -6, 0] }}
                transition={{
                  duration: 2.5,
                  repeat: Infinity,
                  ease: "easeInOut",
                  delay: 0.5,
                }}
                className="absolute -bottom-4 -left-4 glass-card px-4 py-2.5 shadow-xl"
              >
                <span className="text-2xl">🤖</span>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* ========== STATS ========== */}
      <section className="py-12 bg-white border-y border-slate-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, i) => (
              <motion.div
                key={stat.label}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                custom={i}
                variants={fadeUp}
                className="text-center"
              >
                <p className="text-3xl sm:text-4xl font-display font-extrabold gradient-text">
                  {stat.value}
                </p>
                <p className="text-sm text-slate-500 mt-1">{stat.label}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ========== HOW IT WORKS ========== */}
      <section className="py-20 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeUp}
            className="text-center mb-14"
          >
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-900">
              How It Works
            </h2>
            <p className="mt-3 text-slate-600 max-w-lg mx-auto">
              Three simple steps from leaf photo to complete disease report.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {steps.map(({ step, icon: Icon, title, desc }, i) => (
              <motion.div
                key={step}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                custom={i}
                variants={fadeUp}
                className="glass-card p-8 text-center hover:shadow-xl transition-shadow duration-300"
              >
                <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-brand-50 text-brand-600 mb-5">
                  <Icon className="w-7 h-7" />
                </div>
                <div className="text-xs font-bold text-brand-600 tracking-widest mb-2">
                  STEP {step}
                </div>
                <h3 className="text-lg font-semibold text-slate-900 mb-2">
                  {title}
                </h3>
                <p className="text-sm text-slate-600 leading-relaxed">
                  {desc}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ========== FEATURES ========== */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeUp}
            className="text-center mb-14"
          >
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-900">
              Why AgriVision AI?
            </h2>
            <p className="mt-3 text-slate-600 max-w-lg mx-auto">
              Built specifically for Indian agriculture with Google's latest AI.
            </p>
          </motion.div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map(({ icon: Icon, title, desc, color }, i) => (
              <motion.div
                key={title}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                custom={i}
                variants={fadeUp}
                className="glass-card p-6 hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
              >
                <div
                  className={`inline-flex items-center justify-center w-12 h-12 rounded-xl ${color} mb-4`}
                >
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="font-semibold text-slate-900 mb-2">{title}</h3>
                <p className="text-sm text-slate-600 leading-relaxed">{desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ========== CTA ========== */}
      <section className="py-20 bg-gradient-to-br from-brand-600 via-brand-700 to-emerald-800 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeUp}
          >
            <h2 className="font-display text-3xl sm:text-4xl font-bold mb-4">
              Protect Your Crops Today
            </h2>
            <p className="text-lg text-brand-100 mb-8 max-w-xl mx-auto">
              Don't wait for diseases to spread. Upload a leaf photo now and
              get instant, actionable diagnosis.
            </p>
            <Link
              to="/analyze"
              className="inline-flex items-center gap-2 px-8 py-4 bg-white text-brand-700 font-bold rounded-xl shadow-xl hover:shadow-2xl hover:bg-brand-50 transition-all duration-200 text-lg"
            >
              <ScanLine className="w-5 h-5" />
              Start Analyzing
              <ArrowRight className="w-5 h-5" />
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
