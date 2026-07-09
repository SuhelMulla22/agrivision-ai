import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Leaf, ArrowLeft, AlertCircle } from "lucide-react";

export default function NotFound() {
  return (
    <div className="min-h-[80vh] bg-slate-50 flex items-center justify-center px-4">
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, ease: "easeOut" }}
        className="glass-card max-w-md w-full p-8 text-center shadow-lg"
      >
        <div className="w-16 h-16 bg-amber-50 rounded-2xl flex items-center justify-center mx-auto mb-6 border border-amber-200">
          <AlertCircle className="w-8 h-8 text-amber-600" />
        </div>
        
        <h1 className="font-display text-2xl font-black text-slate-900 mb-2">
          Page Not Found
        </h1>
        
        <p className="text-slate-600 text-sm leading-relaxed mb-8">
          The page you are looking for doesn't exist or has been moved. Let's get you back to safety.
        </p>

        <Link
          to="/"
          className="btn-primary w-full flex items-center justify-center gap-2 py-3"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Home
        </Link>
      </motion.div>
    </div>
  );
}
