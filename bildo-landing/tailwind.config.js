/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#16232A',
          dark: '#0D1419',
          light: '#1F3240',
        },
        accent: {
          DEFAULT: '#FF5804',
          light: '#FF7333',
          dark: '#CC4603',
        },
        secondary: {
          DEFAULT: '#075056',
          light: '#0A6A70',
          dark: '#043B3F',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
