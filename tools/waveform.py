#!/usr/bin/env python3
"""Quick static waveform preview: audio file -> PNG strip.

Pure stdlib (wave + zlib PNG writer). The heavy beat-reactive render lives in
the Remotion pipeline; this tool is for fast thumbnails/scratch checks.
"""
import argparse, math, struct, wave, zlib


def write_png(path, w, h, pixels):
    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c))
    raw = b"".join(b"\x00" + bytes(row) for row in pixels)
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    open(path, "wb").write(png)


def envelope(path, n):
    w = wave.open(path, "rb")
    sw, ch, fr = w.getsampwidth(), w.getnchannels(), w.getframerate()
    frames = w.readframes(w.getnframes())
    w.close()
    step = max(1, len(frames) // (n * sw * ch))
    out = []
    for i in range(n):
        seg = frames[i * step * sw * ch:(i + 1) * step * sw * ch]
        peak = 0
        for j in range(0, len(seg) - sw * ch + 1, sw * ch * 8):
            v = abs(struct.unpack_from("<h", seg, j)[0])
            peak = max(peak, v)
        out.append(peak / 32768.0)
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--audio", help="16-bit PCM wav")
    p.add_argument("--out", default="waveform.png")
    p.add_argument("--seed", default="0", help="hex seed shifts hue")
    p.add_argument("--width", type=int, default=640)
    p.add_argument("--height", type=int, default=120)
    a = p.parse_args()
    w, h = a.width, a.height
    hue = int(a.seed.replace("0x", ""), 16) % 256 if a.seed else 0
    if a.audio:
        env = envelope(a.audio, w)
    else:
        env = [0.5 + 0.4 * math.sin(i / 9.0) * math.sin(i / 53.0) for i in range(w)]
    rows = []
    for y in range(h):
        row = bytearray()
        for x in range(w):
            v = env[x]
            bar = abs(y - h // 2) < v * (h // 2)
            r = (hue + x // 4) % 256
            g = 60 + int(140 * v)
            b = 220 - (hue // 2) % 128
            row += bytes((r, g, b)) if bar else bytes((12, 14, 18))
        rows.append(row)
    write_png(a.out, w, h, rows)
    print(f"ok -> {a.out}")


if __name__ == "__main__":
    main()
