/* Apply the saved preference before painting; English remains the default route. */
(() => {
  const root = document.documentElement;
  root.classList.add('js');
  let theme;
  try { theme = localStorage.getItem('arnav-theme'); } catch { /* Storage is optional. */ }
  if (theme !== 'light' && theme !== 'dark') {
    theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  root.dataset.theme = theme;
})();
