/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Space Grotesk"', 'system-ui', 'sans-serif'],
        body: ['"Inter"', 'system-ui', 'sans-serif'],
      },
      colors: {
        brand: {
          50: '#eef8ff',
          100: '#d9edff',
          200: '#b4daff',
          300: '#85c0ff',
          400: '#4b9bff',
          500: '#1e78ff',
          600: '#0f5de6',
          700: '#0f49b3',
          800: '#123f8d',
          900: '#123872',
          glow: '#5cf4ff',
        },
        night: '#0f1629',
        card: '#121b36',
      },
      boxShadow: {
        glass: '0 20px 45px rgba(15, 22, 41, 0.35)',
      },
    },
  },
  plugins: [],
};

