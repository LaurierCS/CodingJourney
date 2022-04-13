/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /* 
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',
        
        /* 
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        fontFamily: {
            sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif']
        },
        extend: {
            colors: {
                transparent: 'transparent',
                current: 'currentColor',
                'primary': '#475aaa',
                'secondary': '#ae8fdf',
                'rice-white': '#F1FAEE',
                'dark': '#002D3D',
                'success': '#43D678',
                'error': '#E3282A',
                'darker-primary': '#23307a',
                'inactive-primary': 'rgba(71,90,170,0.4)',
                'inactive-secondary': 'rgba(122,86,201,0.4)',
                'inactive-dark': '#002d3d',
                'outline-primary': '#1125da',
                'outline-secondary': '#8b69d7',
                'outline-white': '#c4c4c4',
                'outline-dark': '#000000',
                'outline-success': '#a2f0b3',
                'outline-error': '#ff7387',
                'white': "#ffffff",
                'black': '#000000',
            },
            maxWidth: {
                'vw-full': '100vw',
                'vh-full': '100vh'
            },
            backgroundImage: {
                'primary-gradient': 'linear-gradient(to bottom, #5561FF, #3643FC);',
                'dark-gradient': 'linear-gradient(to bottom, #535354, #020206);'
            },
            keyframes: {
                'fade-in-upward': {
                    '0%': {
                        opacity: '0',
                        transform: 'translateY(10px)'
                    },
                    '100%': {
                        opacity: '1',
                        transform: 'translateY(0)'
                    }
                }
            },
            animation: {
                'fade-in-upward': 'fade-in-upward .5s ease-in'
            }
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
