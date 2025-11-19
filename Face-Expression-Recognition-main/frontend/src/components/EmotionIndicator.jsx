import { motion } from 'framer-motion';

export default function EmotionIndicator({ label, intensity, description, color }) {
  return (
    <motion.div
      whileHover={{ scale: 1.03, y: -4 }}
      className="rounded-3xl border border-white/5 bg-white/5 backdrop-blur-2xl p-5 space-y-4"
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-white/50">{label}</p>
          <p className="text-white text-3xl font-display">{Math.round(intensity * 100)}%</p>
        </div>
        <div
          className="h-12 w-12 rounded-2xl bg-white/10 border border-white/10 shadow-inner"
          style={{ boxShadow: `0 0 30px ${color}55 inset` }}
        />
      </div>
      <div className="h-2 rounded-full bg-white/10 overflow-hidden">
        <motion.div
          className="h-full rounded-full"
          style={{ background: color }}
          initial={{ width: 0 }}
          animate={{ width: `${intensity * 100}%` }}
          transition={{ duration: 0.8 }}
        />
      </div>
      <p className="text-white/60 text-sm">{description}</p>
    </motion.div>
  );
}

