export default function Footer() {
  return (
    <footer className="px-6 md:px-16 py-12 flex flex-col md:flex-row gap-6 md:items-center md:justify-between text-white/60 text-sm">
      <p>© {new Date().getFullYear()} Zenith Expressions. Crafted for neural empathy.</p>
      <div className="flex gap-4">
        <a href="#" className="hover:text-white transition">
          Privacy
        </a>
        <a href="#" className="hover:text-white transition">
          Docs
        </a>
        <a href="#" className="hover:text-white transition">
          Support
        </a>
      </div>
    </footer>
  );
}

