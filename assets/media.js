/* Video embeds only contact YouTube after a visitor clicks Play. */
document.addEventListener('click', (event) => {
  const button = event.target.closest('.youtube-load');
  if (!button) return;
  const holder = button.closest('.youtube-placeholder');
  if (!holder) return;
  const id = holder.dataset.videoId;
  if (!/^[A-Za-z0-9_-]{11}$/.test(id)) return;
  const frame = document.createElement('iframe');
  frame.title = holder.dataset.videoTitle || 'YouTube video';
  frame.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1';
  frame.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; web-share';
  frame.allowFullscreen = true;
  frame.referrerPolicy = 'strict-origin-when-cross-origin';
  frame.loading = 'lazy';
  holder.replaceChildren(frame);
});
