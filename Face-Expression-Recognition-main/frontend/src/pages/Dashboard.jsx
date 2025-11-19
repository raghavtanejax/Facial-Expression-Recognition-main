import { motion } from 'framer-motion';
import EmotionIndicator from '../components/EmotionIndicator.jsx';
import { emotionPresets } from '../data/emotions.js';

const timeline = Array.from({ length: 7 }).map((_, i) => ({
  label: `T+${i * 5}m`,
  value: Math.random() * 100,
}));

export default function Dashboard() {
  return (
    <motion.section
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      className="py-16 space-y-10"
    >
      <header className="flex flex-wrap gap-4 items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-white/50">Operator Console</p>
          <h2 className="text-4xl font-display">Realtime Dashboard</h2>
        </div>
        <div className="flex gap-3 flex-wrap">
          <button className="px-5 py-2 rounded-full border border-white/10 text-white/70">Snapshot</button>
          <button className="px-5 py-2 rounded-full bg-white text-night font-semibold">Export Report</button>
        </div>
      </header>

      <div className="grid lg:grid-cols-5 gap-8">
        <div className="lg:col-span-3 rounded-[32px] border border-white/5 p-8 bg-card/70 backdrop-blur-2xl space-y-8">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.3em] text-white/50">Emotion Timeline</p>
              <p className="text-2xl font-display text-brand-glow">+18% uplift</p>
            </div>
            <p className="text-white/60 text-sm">Live • synced 2s ago</p>
          </div>
          <div className="h-64 flex items-end gap-3">
            {timeline.map((item) => (
              <motion.div
                key={item.label}
                className="flex-1 bg-gradient-to-t from-brand-500/20 to-brand-glow/60 rounded-2xl relative"
                initial={{ height: 0 }}
                animate={{ height: `${item.value}%` }}
                transition={{ duration: 0.8 }}
              >
                <span className="absolute -top-6 text-xs text-white/60">{item.label}</span>
              </motion.div>
            ))}
          </div>
        </div>
        <div className="lg:col-span-2 space-y-6">
          {emotionPresets.slice(0, 3).map((emotion) => (
            <EmotionIndicator key={emotion.id} {...emotion} />
          ))}
        </div>
      </div>

      <div className="rounded-[32px] border border-white/5 p-8 bg-card/80 backdrop-blur-2xl space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-white/50">Session Notes</p>
            <p className="text-white/80">Observations auto-summarized via LLM</p>
          </div>
          <button className="text-sm text-brand-glow">Open in Research Log →</button>
        </div>
        <div className="grid md:grid-cols-3 gap-4 text-white/70 text-sm">
          {['Audience relaxed after onboarding animation.', 'Peak joy detected at 14:02 during reveal.', 'Recommend A/B test for CTA copy variant.'].map(
            (note) => (
              <div key={note} className="p-4 rounded-2xl border border-white/5 bg-white/5">
                {note}
              </div>
            )
          )}
        </div>
      </div>
    </motion.section>
  );
}

