module.exports = {
    content: [
        './**/*.html',
        './**/*.scss',
        '!./.venv/**/*',
        '!./node_modules/**/*',
    ],
    theme: {
        extend: {
            colors: {
                'gray-bg': '#f7f8fc',
            }
        },
    },
    variants: {},
    plugins: [],
}
