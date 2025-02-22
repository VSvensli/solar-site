/** @type {import('tailwindcss').Config} */
const primeui = require('tailwindcss-primeui');

export default {
    darkMode: ['class', 'dark-mode'],
    content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
    plugins: [primeui]
};