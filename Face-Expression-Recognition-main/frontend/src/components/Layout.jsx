import Navbar from './Navbar.jsx';
import Footer from './Footer.jsx';

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-night text-white font-body relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div className="glow-gradient glow-gradient--primary" />
        <div className="glow-gradient glow-gradient--secondary" />
      </div>
      <div className="relative z-10">
        <Navbar />
        <main className="px-6 md:px-16">{children}</main>
        <Footer />
      </div>
    </div>
  );
}

