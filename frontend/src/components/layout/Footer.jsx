import { Link } from "react-router-dom";
import { Leaf, Github, Linkedin, Mail, Heart } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-slate-900 text-slate-400">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="md:col-span-2">
            <div className="flex items-center gap-2.5 mb-4">
              <div className="w-9 h-9 bg-gradient-to-br from-brand-500 to-emerald-600 rounded-xl flex items-center justify-center">
                <Leaf className="w-5 h-5 text-white" />
              </div>
              <span className="font-display font-bold text-xl text-white">
                Agri<span className="text-brand-400">Vision</span>
              </span>
            </div>
            <p className="text-sm leading-relaxed max-w-md">
              AI-powered crop disease detection built for Indian farmers.
              Upload a leaf photo, get instant diagnosis with treatment
              recommendations in English, Hindi, and Marathi.
            </p>
            <div className="flex items-center gap-3 mt-4">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 rounded-lg hover:bg-slate-800 transition-colors"
              >
                <Github className="w-5 h-5" />
              </a>
              <a
                href="https://linkedin.com"
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 rounded-lg hover:bg-slate-800 transition-colors"
              >
                <Linkedin className="w-5 h-5" />
              </a>
              <a
                href="mailto:hello@agrivision.ai"
                className="p-2 rounded-lg hover:bg-slate-800 transition-colors"
              >
                <Mail className="w-5 h-5" />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-semibold text-sm mb-4">
              Quick Links
            </h3>
            <ul className="space-y-2">
              {[
                { to: "/", label: "Home" },
                { to: "/analyze", label: "Analyze" },
                { to: "/about", label: "About" },
              ].map(({ to, label }) => (
                <li key={to}>
                  <Link
                    to={to}
                    className="text-sm hover:text-white transition-colors"
                  >
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Technology */}
          <div>
            <h3 className="text-white font-semibold text-sm mb-4">
              Powered By
            </h3>
            <ul className="space-y-2 text-sm">
              <li>TensorFlow / Keras</li>
              <li>FastAPI</li>
              <li>React + Tailwind CSS</li>
              <li>Google Cloud</li>
              <li>Firebase</li>
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="mt-10 pt-6 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs">
            © {new Date().getFullYear()} AgriVision AI. All rights reserved.
          </p>
          <p className="text-xs flex items-center gap-1">
            Built with <Heart className="w-3 h-3 text-red-400 fill-current" /> for Indian Agriculture
          </p>
        </div>
      </div>
    </footer>
  );
}
