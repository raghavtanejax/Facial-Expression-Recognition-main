import Hero from '../components/Hero.jsx';
import WebcamPanel from '../components/WebcamPanel.jsx';
import EmotionIndicator from '../components/EmotionIndicator.jsx';
import { emotionPresets } from '../data/emotions.js';
import { motion } from 'framer-motion';

const featureCards = [
  {
    title: 'Webcam Mesh',
    detail: 'Temporal smoothing + occlusion recovery with sub-10ms latency.',
  },
  {
    title: 'Emotion Cloud',
    detail: 'Multi-user aggregation with privacy-first embeddings.',
  },
  {
    title: 'Insight API',
    detail: 'Stream results into BI tools via secure WebSockets.',
  },
];

export default function Landing() {
  return (
    <div className="space-y-12 pb-24">
      <Hero />
      <motion.section
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: '-100px' }}
        transition={{ duration: 0.8 }}
        className="grid md:grid-cols-3 gap-6"
      >
        {featureCards.map((card) => (
          <article key={card.title} className="p-6 rounded-[28px] border border-white/5 bg-card/50 backdrop-blur-xl">
            <p className="text-sm uppercase tracking-[0.3em] text-brand-glow mb-2">{card.title}</p>
            <p className="text-white/70">{card.detail}</p>
          </article>
        ))}
      </motion.section>

      <section className="grid lg:grid-cols-[1.1fr_0.9fr] gap-8">
        <div className="grid sm:grid-cols-2 gap-6">
          {emotionPresets.map((emotion) => (
            <EmotionIndicator key={emotion.id} {...emotion} />
          ))}
        </div>
        <div className="rounded-[32px] border border-white/5 p-8 bg-gradient-to-br from-brand-500/10 to-brand-glow/5 space-y-6">
          <p className="text-sm uppercase tracking-[0.3em] text-white/50">Animated Pulse</p>
          <motion.div
            className="h-64 rounded-[24px] bg-night overflow-hidden relative"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            <motion.div
              className="absolute inset-0"
              animate={{ backgroundPosition: ['0% 50%', '100% 50%'] }}
              transition={{ repeat: Infinity, duration: 6, ease: 'linear' }}
              style={{
                backgroundImage: 'radial-gradient(circle at 25% 25%, rgba(92,244,255,.35), transparent 40%)',
              }}
            />
            <motion.div
              className="absolute bottom-12 left-0 right-0 mx-auto w-11/12 h-16 rounded-full bg-white/5 blur-3xl"
              animate={{ opacity: [0.3, 0.6, 0.3] }}
              transition={{ repeat: Infinity, duration: 5 }}
            />
            <motion.div
              className="absolute inset-x-6 bottom-10 h-20 rounded-3xl border border-white/10 flex items-center justify-between px-6"
              animate={{ y: [0, -8, 0] }}
              transition={{ repeat: Infinity, duration: 4 }}
            >
              <p className="font-display text-4xl">72%</p>
              <p className="text-white/50 text-sm uppercase tracking-[0.3em]">Positive</p>
            </motion.div>
          </motion.div>
        </div>
      </section>

      <WebcamPanel />
    </div>
  );
}

