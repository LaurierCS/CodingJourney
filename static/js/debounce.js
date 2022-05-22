/**
 * 
 * @param {Function} func 
 * @param {number} timeout in milliseconds. Default 300ms.
 * @returns 
 */
function debounce(func, timeout = 300) {
  let timer;
  return (...args) => {
    clearTimeout(timer)
    timer = setTimeout(() => {
      func.apply(this, args)
    }, timeout);
  }
}