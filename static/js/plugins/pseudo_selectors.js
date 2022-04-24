const plugin = require("tailwindcss/plugin")

module.exports = plugin(({ addVariant }) => {
  addVariant('not-focus-visible','&:not(:focus-visible)')
}) 