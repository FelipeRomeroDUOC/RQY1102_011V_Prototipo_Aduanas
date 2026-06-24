/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        aduana: {
          blue: '#003087',
          light: '#0057A8',
        },
        estado: {
          valido: '#15803D',
          rechazado: '#B91C1C',
          observado: '#B45309',
          pendiente: '#B45309'
        }
      }
    },
  },
  plugins: [],
}
