import { useCallback, useMemo, useState } from 'react';
import Webcam from 'react-webcam';
import { motion } from 'framer-motion';
import clsx from 'clsx';

const overlayClasses =
  'absolute inset-0 rounded-[28px] border border-white/10 pointer-events-none mix-blend-screen bg-gradient-to-br from-white/5 to-transparent';

export default function WebcamPanel() {
  const [isActive, setIsActive] = useState(false);
  const [emotion, setEmotion] = useState('Awaiting signal');

  const videoConstraints = useMemo(
    () => ({
      width: 720,
      height: 480,
      facingMode: 'user',
    }),
    []
  );

  const handleCapture = useCallback(() => {
    setIsActive((prev) => !prev);
    if (!isActive) {
      const states = ['Joy', 'Calm', 'Surprise', 'Focus'];
      const next = states[Math.floor(Math.random() + (states.length - 1) * Math.random())];
      setEmotion(`Streaming • ${next}`);
    } else {
      setEmotion('Awaiting signal');
    }
  }, [isActive]);

  return (
    <section id="demo" className="py-16">
      <div className="rounded-[32px] bg-card/80 border border-white/5 p-6 md:p-10 shadow-glass space-y-6">
        <div className="flex flex-wrap gap-4 items-center justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-white/50">Realtime Feed</p>
            <p className="text-2xl font-display">{emotion}</p>
          </div>
          <button
            onClick={handleCapture}
            className={clsx(
              'px-6 py-3 rounded-full text-sm font-semibold tracking-wide border border-white/10 transition',
              isActive ? 'bg-white text-night' : 'text-white/80 hover:text-white'
            )}
          >
            {isActive ? 'Stop Stream' : 'Activate Camera'}
          </button>
        </div>
        <div className="relative rounded-[28px] overflow-hidden bg-night aspect-video">
          {isActive ? (
            <Webcam audio={false} screenshotFormat="image/jpeg" videoConstraints={videoConstraints} className="w-full" />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-white/40 tracking-[0.4em] uppercase">
              Camera Idle
            </div>
          )}
          <div className={overlayClasses} />
        </div>
      </div>
    </section>
  );
}

