"""Safe, accessible media embeds for Field Notes Markdown articles.

Markdown keeps native ![alt](url) support. For captions and embedded
video use :::image, :::video, or :::youtube blocks.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

_BLOCK = re.compile(r'(?ms)^:::(image|video|youtube)[ \t]*\n(.*?)^:::[ \t]*(?:\n|$)')
_LOCAL = re.compile(r'^/assets/(images|videos)/[a-zA-Z0-9_./-]+$')
_YOUTUBE = re.compile(r'^[A-Za-z0-9_-]{11}$')
_IMAGES = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.avif'}
_VIDEOS = {'.mp4': 'video/mp4', '.webm': 'video/webm'}
_MAX_ASSET = 25 * 1024 * 1024  # Cloudflare Pages maximum per static asset.


def check_media_file(url: str, kind: str, root: Path) -> str:
    """Admit only published media beneath assets/images or assets/videos."""
    match = _LOCAL.fullmatch(url)
    if not match or match.group(1) != kind or '..' in Path(url).parts:
        raise ValueError(f'Invalid {kind} asset URL: {url!r}')
    target = root / url.lstrip('/')
    allowed = _IMAGES if kind == 'images' else set(_VIDEOS)
    if target.suffix.lower() not in allowed:
        raise ValueError(f'Unsupported {kind} file format: {url!r}')
    if not target.is_file():
        raise ValueError(f'Missing {kind} file: {url!r}. Upload it before publishing.')
    if target.stat().st_size > _MAX_ASSET:
        raise ValueError(f'Media file exceeds the Cloudflare Pages 25 MiB limit: {url!r}')
    return url


def _parse_fields(raw: str, media_type: str) -> dict[str, str]:
    allowed = {
        'image': {'src', 'alt', 'caption'},
        'video': {'src', 'poster', 'caption', 'autoplay', 'loop'},
        'youtube': {'id', 'title', 'caption'},
    }[media_type]
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        key, colon, value = line.partition(':')
        key = key.strip().lower()
        if not colon or not key or key not in allowed or key in fields:
            raise ValueError(f'Invalid or duplicate field in ::: {media_type} block: {line!r}')
        fields[key] = value.strip()
    return fields


def _caption(text: str) -> str:
    return f'<figcaption>{html.escape(text)}</figcaption>' if text else ''


def _bool(fields: dict[str, str], key: str) -> bool:
    value = fields.get(key, 'false').lower()
    if value not in ('true', 'false'):
        raise ValueError(f'{key} must be true or false, got {value!r}')
    return value == 'true'


def _embed(media_type: str, options: dict[str, str], root: Path) -> str:
    esc = lambda x: html.escape(x, quote=True)
    caption = _caption(options.get('caption', ''))
    if media_type == 'image':
        src = check_media_file(options.get('src', ''), 'images', root)
        alt = options.get('alt', '').strip()
        if not alt:
            raise ValueError(':::image needs a descriptive alt field')
        return (f'<figure class="media-figure"><a href="{esc(src)}" target="_blank" rel="noopener" '
                f'aria-label="Open full-size image: {esc(alt)}"><img src="{esc(src)}" alt="{esc(alt)}" '
                f'loading="lazy" decoding="async"></a>{caption}</figure>')
    if media_type == 'video':
        src = check_media_file(options.get('src', ''), 'videos', root)
        poster = options.get('poster', '')
        if poster:
            check_media_file(poster, 'images', root)
        autoplay = _bool(options, 'autoplay')
        loop = _bool(options, 'loop')
        suffix = Path(src).suffix.lower()
        extra = (' autoplay muted' if autoplay else '') + (' loop' if loop else '')
        posterattr = f' poster="{esc(poster)}"' if poster else ''
        return (f'<figure class="media-figure media-video"><video controls playsinline preload="metadata"{extra}{posterattr}>'
                f'<source src="{esc(src)}" type="{_VIDEOS[suffix]}">'
                f'Your browser cannot play this video. <a href="{esc(src)}">Open the video file</a>.'
                f'</video>{caption}</figure>')
    video_id = options.get('id', '')
    if not _YOUTUBE.fullmatch(video_id):
        raise ValueError(':::youtube needs an 11-character YouTube video ID')
    title = options.get('title', '').strip()
    if not title:
        raise ValueError(':::youtube needs a title for accessibility')
    return (f'<figure class="media-figure media-youtube"><div class="youtube-placeholder" '
            f'data-video-id="{esc(video_id)}" data-video-title="{esc(title)}">'
            f'<button type="button" class="youtube-load" aria-label="Load YouTube video: {esc(title)}">'
            f'<span aria-hidden="true">▶</span> Play YouTube video</button>'
            f'<p>Loads content from YouTube after you click play.</p></div>{caption}</figure>')


def render_media_markdown(body: str, markdown_renderer, root: Path) -> str:
    """Render Markdown with explicit, escaped media directive markup.

    Directives inside triple-backtick code samples are not interpreted.
    """
    media_html: dict[str, str] = {}

    def substitute(match):
        prefix = body[:match.start()]
        if len(re.findall(r'(?m)^\s*' + chr(96) * 3, prefix)) % 2:
            return match.group(0)
        media_type, raw = match.group(1), match.group(2)
        token = f'FIELDNOTESMEDIABLOCK{len(media_html):05d}END'
        media_html[token] = _embed(media_type, _parse_fields(raw, media_type), root)
        return f'\n{token}\n\n'

    substituted = _BLOCK.sub(substitute, body)
    output = markdown_renderer(substituted)
    for token, replacement in media_html.items():
        wrapped = f'<p>{token}</p>'
        if wrapped not in output:
            raise ValueError(f'Media directive must be on its own line: {token}')
        output = output.replace(wrapped, replacement, 1)
    return output
