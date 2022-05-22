module.exports = {
  /**
   * Look for class within all html files in our template folder
   */
  content: ["../../../templates/**/*.html", "../*.js"],
  /**
   * Theme configuration
   */
  theme: {
    fontFamily: {
      sans: [
        "-apple-system",
        "BlinkMacSystemFont",
        "Segoe UI",
        "Roboto",
        "sans-serif",
      ],
    },
    /**
     * Extend the classes that tailwind has to offerY instead of overriding them.
     * Overriding any of the default category, such as margin, will get rid of all
     * built-in classes for margin and leave the ones you have define.
     */
    extend: {
      colors: {
        transparent: "transparent",
        current: "currentColor",
        primary: "var(--primary)",
        secondary: "var(--secondary)",
        "darker-blue": "var(--darker-blue)",
        success: "var(--success)",
        active: "var(--active)",
        error: "var(--error)",
        active: "var(--active)",
        white: "var(--white)",
        black: "var(--black)",
        background: "var(--background)",
        foreground: "var(--foreground)", // for navbar, cards, and any foreground color
        "foreground-dark": "var(--darker-blue)", // darker background for an element next to or inside a an element with color "foreground"
        "rice-white": "var(--rice-white)",
        "primary-dark": "var(--primary-dark)",
        "primary-darker": "var(--primary-darker)",
        "inactive-primary": "var(--inactive-primary-color)",
        "inactive-secondary": "var(--inactive-secondary-color)",
        "inactive-dark": "var(--inactive-dark-color)",
        "outline-primary": "var(--outline-primary-color)",
        "outline-secondary": "var(--outline-secondary-color)",
        "outline-white": "var(--outline-white-color)",
        "outline-dark": "var(--outline-dark-color)",
        "outline-success": "var(--outline-success-color)",
        "outline-error": "var(--outline-error-color)",
      },
      maxWidth: {
        "vw-full": "100vw",
        "vh-full": "100vh",
      },
      backgroundImage: {
        "primary-gradient": "var(--primary-gradient-top-bottom)",
        "dark-gradient": "var(--dark-gradient-top-bottom)",
      },
      keyframes: {
        "fade-in-upward": {
          "0%": {
            opacity: "0",
            transform: "translateY(10px)",
          },
          "100%": {
            opacity: "1",
            transform: "translateY(0)",
          },
        },
      },
      animation: {
        "fade-in-upward": "fade-in-upward .5s ease-in",
      },
      fontSize: {
        'h1': '70px',
        'h2': '55px',
        'h3': '40px',
        'h4': '25px',
        'button': '16px',
        'body': '19px',
        'link': '17px',
      },
      lineHeight : {
        'h1': '75.5px',
        'h2': '41px',
        'h4': '38px',
        'button': '30px',
        'link': '15px',
      },
    },
  },
  plugins: [
    require('./plugins/pseudo_selectors'),
    require('@tailwindcss/line-clamp'),
  ]
};
