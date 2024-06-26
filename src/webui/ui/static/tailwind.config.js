/** @product_type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "../templates/**/*.{html,js}",
    ],
    theme: {
        extend: {},
    },
    plugins: [require("@tailwindcss/typography"), require("daisyui")],

    daisyui: {
        themes: ["dracula"],
    },
}