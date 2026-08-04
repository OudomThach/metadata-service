/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        base: {
          900: "#0b0f14",
          850: "#0f151c",
          800: "#131a22",
          700: "#1a2330",
          600: "#243044",
        },
        accent: {
          DEFAULT: "#2dd4bf",
          dim: "#14b8a6",
        },
      },
    },
  },
  plugins: [],
};
