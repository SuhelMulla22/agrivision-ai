import { motion } from "framer-motion";
import {
  Leaf,
  Github,
  ExternalLink,
  Cpu,
  Server,
  Database,
  Cloud,
  Layers,
} from "lucide-react";

const fadeUp = {
  hidden: { opacity: 0, y: 10 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.05, duration: 0.3, ease: "easeOut" },
  }),
};

const techStack = [
  {
    category: "AI & Machine Learning",
    icon: Cpu,
    items: [
      { name: "Gemini 2.5 Flash", desc: "Primary universal Vision API" },
      { name: "OpenRouter Vision", desc: "Secondary universal fallback API" },
      { name: "MobileNetV2 (Keras)", desc: "Offline 46-class TF classifier" },
    ],
  },
  {
    category: "Backend & Database",
    icon: Server,
    items: [
      { name: "FastAPI", desc: "Async Python web framework" },
      { name: "Supabase (PostgreSQL)", desc: "Relational database with RLS policies" },
      { name: "Supabase Storage", desc: "Blob storage for uploaded crop photos" },
    ],
  },
  {
    category: "Frontend",
    icon: Layers,
    items: [
      { name: "React 18", desc: "UI library" },
      { name: "Tailwind CSS", desc: "Premium responsive UI design" },
      { name: "Framer Motion", desc: "Micro-animations & transitions" },
    ],
  },
  {
    category: "Infrastructure",
    icon: Cloud,
    items: [
      { name: "JWT Security", desc: "Secure token-based user authentication" },
      { name: "Dynamic Local KB", desc: "Rule-based multi-language fallback" },
      { name: "Docker", desc: "Containerization" },
    ],
  },
];

export default function About() {
  return (
    <div className="min-h-screen bg-slate-50">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <motion.div initial="hidden" animate="visible" variants={fadeUp}>
          <h1 className="font-display text-3xl sm:text-4xl font-bold text-slate-900">
            About <span className="gradient-text">AgriVision AI</span>
          </h1>
          <p className="mt-3 text-lg text-slate-600 leading-relaxed max-w-2xl">
            AgriVision AI is a hybrid AI-powered crop disease detection platform
            built to help farmers identify plant diseases instantly
            using a smartphone camera — online or offline.
          </p>
        </motion.div>

        {/* Mission */}
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={fadeUp}
          className="glass-card p-8 mt-10"
        >
          <h2 className="font-display text-xl font-bold text-slate-900 mb-4">
            🎯 Our Mission
          </h2>
          <p className="text-slate-600 leading-relaxed">
            Indian agriculture loses over ₹90,000 crores annually to crop
            diseases. Farmers in rural areas lack access to timely diagnosis
            and expert advice. AgriVision AI bridges this gap by putting the
            power of artificial intelligence in every farmer's pocket. Our 
            three-tier hybrid architecture ensures 100% availability by cascading 
            from state-of-the-art vision models to an offline-capable classifier.
          </p>
          <div className="grid sm:grid-cols-3 gap-4 mt-6">
            <div className="text-center p-4 bg-brand-50 rounded-xl">
              <p className="text-2xl font-bold text-brand-700">Universal</p>
              <p className="text-sm text-brand-600">Crops Supported</p>
            </div>
            <div className="text-center p-4 bg-brand-50 rounded-xl">
              <p className="text-2xl font-bold text-brand-700">Zero-Shot</p>
              <p className="text-sm text-brand-600">Diseases Detected</p>
            </div>
            <div className="text-center p-4 bg-brand-50 rounded-xl">
              <p className="text-2xl font-bold text-brand-700">3</p>
              <p className="text-sm text-brand-600">Languages (EN/HI/MR)</p>
            </div>
          </div>
        </motion.div>

        {/* Tech Stack */}
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={fadeUp}
          className="mt-10"
        >
          <h2 className="font-display text-2xl font-bold text-slate-900 mb-6">
            🛠️ Technology Stack
          </h2>
          <div className="grid sm:grid-cols-2 gap-4">
            {techStack.map(({ category, icon: Icon, items }, i) => (
              <motion.div
                key={category}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                custom={i}
                variants={fadeUp}
                className="glass-card p-6"
              >
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 rounded-xl bg-brand-50 text-brand-600 flex items-center justify-center">
                    <Icon className="w-5 h-5" />
                  </div>
                  <h3 className="font-semibold text-slate-900">{category}</h3>
                </div>
                <ul className="space-y-2">
                  {items.map(({ name, desc }) => (
                    <li
                      key={name}
                      className="flex items-center gap-2 text-sm"
                    >
                      <span className="w-1.5 h-1.5 rounded-full bg-brand-400" />
                      <span className="font-medium text-slate-700">
                        {name}
                      </span>
                      <span className="text-slate-400">—</span>
                      <span className="text-slate-500">{desc}</span>
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* System Architecture */}
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={fadeUp}
          className="glass-card p-8 mt-10"
        >
          <h2 className="font-display text-xl font-bold text-slate-900 mb-4">
            🧠 System Architecture (3-Tier Cascade)
          </h2>
          <div className="font-mono text-xs bg-slate-900 text-emerald-400 p-6 rounded-xl overflow-x-auto leading-relaxed">
            <pre>{`Input Image (Uploaded crop leaf, fruit, or vegetable)
                  ↓
       [Tier 1: Direct Gemini 2.5 Flash API] ──► (Succeeds) ──► Universal Diagnosis (JSON)
                  ↓ (Fails / Rate Limit)
       [Tier 2: OpenRouter API Gateway]      ──► (Succeeds) ──► Universal Diagnosis (JSON)
                  ↓ (Fails / Offline)
       [Tier 3: Local MobileNetV2 Model]     ──► (Classifies) ──► 46-Class Model (Acc: 95.85%)
                  ↓
       [Dynamic Local Fallback / KB Lookup]  ──► Offline Rule-Based Local Diagnosis`}</pre>
          </div>
          <p className="text-sm text-slate-500 mt-4">
            Our hybrid architecture combines state-of-the-art Large Vision Models with highly optimized local deep learning. If your direct API quota runs out, the system automatically falls back to OpenRouter. If internet connection is completely lost, it leverages a fine-tuned 46-class MobileNetV2 model running locally on CPU.
          </p>
        </motion.div>

        {/* GitHub CTA */}
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={fadeUp}
          className="text-center mt-12"
        >
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-secondary inline-flex items-center gap-2 text-base px-8 py-4"
          >
            <Github className="w-5 h-5" />
            View Source on GitHub
            <ExternalLink className="w-4 h-4" />
          </a>
        </motion.div>
      </div>
    </div>
  );
}
