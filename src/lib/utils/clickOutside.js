
export function clickOutside(node, handler) {
  const handleClick = event => {
    if (!node.contains(event.target)) {
      handler();
    }
  };

  document.addEventListener('click', handleClick, true);

  return {
    destroy() {
      document.removeEventListener('click', handleClick, true);
    }
  };
}