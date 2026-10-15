# Field Notes: images, animations, and video (v0.5)

These features work across Game, Water, and Career. The existing visual style and
Giscus comments remain unchanged. Save a new Markdown article under
content/game/, content/water/, or content/career/.

## Where media goes

Upload your files to the **public** GitHub repository before referencing them:
- assets/images/game/ — game screenshots, preview images, animated GIF/WebP
- assets/images/water/ — GIS maps, charts, screenshots
- assets/images/career/ — non-private career diagrams
- assets/videos/game/ — short gameplay recordings (MP4/WebM)
- assets/videos/water/ — short model animations

GitHub: Add file > Upload files. Keep the directory paths exactly as shown.
An article and its assets may be included in the same commit. The builder reports
a clear error when a referenced media file doesn't exist.

Supported images: .png, .jpg, .jpeg, .webp, .avif, .gif
Supported videos: .mp4, .webm (prefer H.264 MP4 for browser compatibility).

**Cloudflare Pages limits individual static assets to 25 MiB.**
Aim for smaller files. For longer videos use a YouTube embed (not a large Git
binary); for larger self-hosted libraries consider R2 or a dedicated video host.
Avoid uploading private documents, contact details, unpublished game assets you
don't want to share, or copyrighted material without permission.

## 1. Plain Markdown image

~~~markdown
![Pedestrians walking to a restaurant](/assets/images/game/pedestrians.webp)
~~~

Works for static or animated images (GIF or animated WebP). Standard Markdown images
also fit the screen width automatically.

## 2. Captioned, clickable image

~~~text
:::image
src: /assets/images/water/river-depth-map.webp
alt: Simulated flood water depths along the river
caption: Figure 1. Modelled flood depth after the first HEC-RAS run.
:::
~~~

A captioned image is lazy-loaded, resizes to the screen, and opens full-size
when clicked. Alt text is required for readers using assistive technology.

## 3. Short MP4 or WebM with playback controls

~~~text
:::video
src: /assets/videos/game/customer-walkthrough.mp4
poster: /assets/images/game/customer-preview.webp
caption: Video 1. The customer AI walking toward a restaurant.
autoplay: false
loop: false
:::
~~~

The poster, caption, autoplay, and loop fields are optional. By default the
video does not autoplay, with native pause/play and seek controls. When
autoplay is true, playback is muted to comply with browser autoplay rules.
Use loop: true for short looping game or model animations.

## 4. YouTube embed (for longer videos)

~~~text
:::youtube
id: VIDEOID1234
title: Customer simulation walkthrough
caption: Video 2. Full development demonstration.
:::
~~~

Replace VIDEOID1234 with the video's exact 11-character ID from its YouTube URL.
A visitor must click Play before the YouTube player loads. This avoids initial
third-party requests and improves privacy and page speed.

## Publishing

1. Upload public screenshots and clips to the relevant assets folder in GitHub.
2. Give me the topic, your draft notes, and the media filenames. We can assemble
   the Markdown with suitable figures and natural writing.
3. Review the text and media; commit the approved article and files to main.
4. Cloudflare Pages rebuilds automatically. Check the live post on desktop/mobile.

Use one media directive per block with its own opening and closing line.
Unrecognized fields, unsafe file paths, or missing files fail the build so
broken media doesn't quietly appear online.

For privacy, always review screenshots for account numbers, addresses, API
keys, usernames, confidential strategies, and personal correspondence.
