module.exports = {
  /**
   * Look for class within all html files in our template folder
   */
  content: ["../../../templates/**/*.html"],

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
     * Extend the classes that tailwind has to offer instead of overriding them.
     * Overriding any of the default category, such as margin, will get rid of all
     * built-in classes for margin and leave the ones you have define.
     */
    extend: {
      colors: {
        transparent: "transparent",
        current: "currentColor",
        primary: "var(--primary-color-bluishPurple)",
        secondary: "var(--secondary-color-lightPurple)",
        "rice-white": "var(--rice-white)",
        dark: "var(--dark-background)",
        darker_blue: "#00232f",
        success: "var(--success)",
        active: "var(--active)",
        error: "var(--error)",
        active: "var(--active)",
        "darker-primary": "var(--darker-primary)",
        "inactive-primary": "var(--inactive-primary-color)",
        "inactive-secondary": "var(--inactive-secondary-color)",
        "inactive-dark": "var(--inactive-dark-color)",
        "outline-primary": "var(--outline-primary-color)",
        "outline-secondary": "var(--outline-secondary-color)",
        "outline-white": "var(--outline-white-color)",
        "outline-dark": "var(--outline-dark-color)",
        "outline-success": "var(--outline-success-color)",
        "outline-error": "var(--outline-error-color)",
        white: "var(--white)",
        black: "var(--black)",
        background: "var(--background)",
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
    },
  },
  plugins: [
    require('./plugins/pseudo_selectors')
  ]
};
