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
          DEFAULT: '#2ECC71',
          dark: '#27AE60',
          light: '#A8E6CF',
          50: '#F0FDF4',
          100: '#DCFCE7',
          200: '#BBF7D0',
          300: '#86EFAC',
          400: '#4ADE80',
          500: '#2ECC71',
          600: '#27AE60',
          700: '#15803D',
          800: '#166534',
          900: '#14532D',
        },
        dark: {
          DEFAULT: '#1E1E1E',
          light: '#2D2D2D',
          lighter: '#3D3D3D',
        }
      },
    },
  },
  plugins: [],
}
