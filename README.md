# waveform-render

Personal audio-reactive visualizer. Turns a music track plus a hex seed into
a short MP4 (waveform bars, beat-reactive particles). Built on Remotion and
FFmpeg. Heavier renders take 20-40 minutes, so they run as manual dispatches
instead of local jobs.

## Usage

Actions -> render -> Run workflow

- `seed` - 32-char hex, drives palette and geometry determinism
- `profile` - `preview` renders only, `full` renders and publishes the clip
  to my channel

## Layout

- `tools/waveform.py` - quick static waveform preview generator
- `.github/workflows/render.yml` - the render pipeline

Status: personal WIP. Not useful for anyone else yet.
