"""Stdlib-only objective audio measurements. These are NOT pronunciation-quality scores."""
import array, hashlib, math, struct, sys
def read_wav(path):
    """Minimal RIFF reader: PCM16 (tag 1) or IEEE float32 (tag 3), little-endian. Returns (rate, channels, samples in [-1,1])."""
    b = open(path, "rb").read()
    if b[:4] != b"RIFF" or b[8:12] != b"WAVE": raise ValueError("not a RIFF/WAVE file")
    i, fmt, data = 12, None, None
    while i + 8 <= len(b):
        cid, size = b[i:i + 4], struct.unpack("<I", b[i + 4:i + 8])[0]; body = b[i + 8:i + 8 + size]
        if len(body) < size: raise ValueError("truncated chunk")
        if cid == b"fmt ":
            if size < 16: raise ValueError("fmt chunk too short")
            fmt = struct.unpack("<HHIIHH", body[:16])
        elif cid == b"data": data = body
        i += 8 + size + (size & 1)
    if fmt is None or data is None: raise ValueError("missing fmt or data chunk")
    tag, ch, sr, _, _, bits = fmt
    if (tag, bits) == (1, 16): a = array.array("h", data[:len(data) // 2 * 2]); scale = 32768.0
    elif (tag, bits) == (3, 32): a = array.array("f", data[:len(data) // 4 * 4]); scale = 1.0
    else: raise ValueError(f"unsupported format tag={tag} bits={bits}")
    if sys.byteorder != "little": a.byteswap()
    return sr, ch, [x / scale for x in a]
def stats(path, silence_dbfs=-40.0, frame_ms=20):
    sr, ch, a = read_wav(path); n = len(a) // ch
    if n == 0 or ch == 0 or sr == 0: raise ValueError("no audio frames")
    mono = [sum(a[i:i + ch]) / ch for i in range(0, n * ch, ch)]
    full = 1.0; step = max(1, sr * frame_ms // 1000); thr = full * 10 ** (silence_dbfs / 20)
    frames = [mono[i:i + step] for i in range(0, len(mono), step)]
    silent = sum(1 for f in frames if math.sqrt(sum(x * x for x in f) / len(f)) < thr)
    rms = math.sqrt(sum(x * x for x in mono) / len(mono)) if mono else 0.0
    return {"sha256": hashlib.sha256(open(path, "rb").read()).hexdigest(), "sample_rate": sr, "channels": ch,
            "duration_s": round(n / sr, 3), "rms_dbfs": round(20 * math.log10(rms / full), 2) if rms else None,
            "peak_abs": round(max((abs(x) for x in a), default=0.0), 4), "clipped_samples": sum(1 for x in a if abs(x) >= 0.9999),
            "silent_frame_fraction": round(silent / len(frames), 3) if frames else None}
def summarize(per_item, texts):
    d = [per_item[k]["duration_s"] for k in sorted(per_item)]
    rate = [round(per_item[k]["duration_s"] / max(1, len(texts[k].replace(" ", ""))), 4) for k in sorted(per_item)]
    srt = sorted(d)
    return {"n": len(d), "duration_s_min": srt[0], "duration_s_median": srt[len(srt) // 2] if len(srt) % 2 else (srt[len(srt)//2-1] + srt[len(srt)//2]) / 2,
            "duration_s_max": srt[-1], "s_per_char_min": min(rate), "s_per_char_max": max(rate),
            "items_with_clipping": sum(1 for v in per_item.values() if v["clipped_samples"]),
            "items_silent_fraction_gt_0_5": sum(1 for v in per_item.values() if v["silent_frame_fraction"] > 0.5)}
