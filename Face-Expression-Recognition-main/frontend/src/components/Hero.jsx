import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

export default function Hero() {
  return (
    <section className="py-20 md:py-28 grid md:grid-cols-[1.1fr_0.9fr] gap-12 items-center">
      <div className="space-y-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 border border-white/20 text-sm uppercase tracking-[0.3em]"
        >
          FUTURES RESEARCH
          <span className="w-2 h-2 rounded-full bg-brand-glow animate-pulse" />
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.8 }}
          className="font-display text-4xl md:text-6xl leading-tight"
        >
          Decode human emotion streams <span className="text-brand-glow">in realtime</span>.
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.8 }}
          className="text-lg text-white/70 max-w-xl"
        >
          A premium analytics layer for your vision models. Capture webcam signals, interpret micro-expressions, and
          orchestrate immersive dashboards that feel alive.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.8 }}
          className="flex flex-wrap gap-4"
        >
          <Link
            to="/dashboard"
            className="px-8 py-4 rounded-2xl bg-white text-night font-semibold tracking-wide shadow-glass"
          >
            Launch Console
          </Link>
          <a href="#demo" className="px-8 py-4 rounded-2xl border border-white/20 text-white/80">
            Watch Demo
          </a>
        </motion.div>
      </div>
      <motion.div
        initial={{ opacity: 0, x: 60 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.2, duration: 0.9 }}
        className="p-8 rounded-[32px] bg-card/80 backdrop-blur-2xl border border-white/5 shadow-glass space-y-6"
      >
        <p className="text-sm uppercase tracking-[0.3em] text-white/50">LIVE STACK</p>
        <div className="space-y-4">
          {['Signal Fusion', 'Graph Transformer', 'Emotion API', 'Realtime Stream'].map((item, index) => (
            <div key={item} className="flex items-center justify-between text-white/70">
              <span>{item}</span>
              <span className="text-brand-glow">{index === 2 ? '4.2ms' : 'Ready'}</span>
            </div>
          ))}
        </div>
        <div className="h-40 rounded-3xl bg-gradient-to-br from-brand-500/30 to-brand-glow/20 relative overflow-hidden">
          <motion.div
            className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(92,244,255,0.35),_transparent_55%)]"
            animate={{ rotate: 360 }}
            transition={{ repeat: Infinity, duration: 12, ease: 'linear' }}
          />
          <div className="absolute bottom-4 left-6">
            <p className="text-xs uppercase tracking-[0.4em] text-white/60">SENTIMENT</p>
            <p className="text-3xl font-display">92% Lift</p>
          </div>
        </div>
      </motion.div>
    </section>
  );
}

