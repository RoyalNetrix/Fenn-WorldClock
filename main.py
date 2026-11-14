"""Fenn world clocks. Stdlib only, no network. On Windows run once: pip install tzdata"""
import json, os, sys, threading, time
from datetime import datetime
try:
    from zoneinfo import ZoneInfo, available_timezones
except ImportError:
    ZoneInfo = available_timezones = None

DATA = os.environ.get("FENN_DATA_DIR") or os.environ.get("NOOK_DATA_DIR") or "."   # NOOK_DATA_DIR is the older name
CFG_PATH = os.path.join(DATA, "config.json")
out_lock = threading.Lock()
cfg = {"zones": ["Europe/London", "America/New_York", "Asia/Tokyo", "Australia/Sydney"]}
tile_w, msg_note = 104, ""


def send(msg):
    with out_lock:
        sys.stdout.write(json.dumps(msg) + "\n")
        sys.stdout.flush()


def load_cfg():
    try:
        with open(CFG_PATH, encoding="utf-8") as f:
            cfg.update(json.load(f))
    except (OSError, ValueError):
        pass


def save_cfg():
    try:
        os.makedirs(DATA, exist_ok=True)
        with open(CFG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f)
    except OSError as e:
        print("save failed:", e, file=sys.stderr)


def txt(text, **kw):
    return {"type": "text", "text": text, **kw}


def rows():
    local = datetime.now().astimezone()
    res, missing = [], False
    for z in cfg["zones"]:
        name = z.split("/")[-1].replace("_", " ")
        try:
            t = datetime.now(ZoneInfo(z))
        except Exception:
            res.append((z, name, None, ""))
            missing = True
            continue
        mins = int((t.utcoffset() - local.utcoffset()).total_seconds() // 60)
        h, m = divmod(abs(mins), 60)
        off = ("+" if mins >= 0 else "-") + f"{h}h" + (f" {m}m" if m else "")
        day = {0: "Today", 1: "Tomorrow", -1: "Yesterday"}.get((t.date() - local.date()).days, "")
        sub = f"{day} · {off}" if mins else day
        res.append((z, name, t.strftime("%H:%M"), sub))
    return local, res, missing


def render():
    local, rs, missing = rows()
    if tile_w < 70:
        tile = txt(local.strftime("%H:%M"), size="title", bold=True)
    else:
        lines = [f"{t}  {n}" for _, n, t, _ in rs[:2] if t] or ["Open to add cities"]
        tile = {"type": "row", "align": "center", "gap": 10, "children": [
            {"type": "icon", "icon": "globe-hemisphere-west", "size": 26, "color": "accent"},
            {"type": "column", "gap": 0, "children": [txt(s, size="small") for s in lines]}]}
    send({"type": "tile", "view": tile})

    def row(zid, name, t, sub, removable):
        kids = [{"type": "column", "gap": 0, "children": [txt(name, bold=True), txt(sub, size="small", color="dim")]},
                {"type": "spacer"}, txt(t or "?", size="title")]
        if removable:
            kids.append({"type": "button", "id": "rm:" + zid, "icon": "x", "tooltip": "Remove"})
        return {"type": "row", "align": "center", "gap": 8, "children": kids}

    note = msg_note or ("Zone data missing. Run: pip install tzdata" if missing else "")
    page = {"type": "column", "gap": 8, "scroll": True, "children": [
        {"type": "input", "id": "add", "value": "", "hint": "Add a city or zone (Tokyo, Asia/Dubai) and press Enter", "width": 360},
        *([txt(note, size="small", color="red")] if note else []),
        row("local", "Local", local.strftime("%H:%M"), local.strftime("%a %d %b"), False),
        *[row(z, n, t, s, True) for z, n, t, s in rs]]}
    send({"type": "page", "view": page})


def lookup(name):
    n = name.strip().lower().replace(" ", "_")
    if not n or not available_timezones:
        return None
    for z in sorted(available_timezones()):
        zl = z.lower()
        if zl == n or zl.endswith("/" + n):
            return z
    return None


def ticker():
    while True:
        render()
        time.sleep(60 - time.time() % 60 + 0.2)


def main():
    global tile_w, msg_note
    try:
        sys.stdin.reconfigure(encoding="utf-8")
    except Exception:
        pass
    load_cfg()
    threading.Thread(target=ticker, daemon=True).start()
    for line in sys.stdin:
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        t = msg.get("type")
        if t == "event":
            i, v = str(msg.get("id")), msg.get("value")
            if i == "add" and msg.get("kind") == "submit":
                z = lookup(str(v or ""))
                if z and z not in cfg["zones"]:
                    cfg["zones"].append(z)
                    save_cfg()
                    msg_note = ""
                elif not z:
                    msg_note = "Unknown place. Try a city (Tokyo) or a zone (Asia/Dubai)."
                render()
            elif i.startswith("rm:") and i[3:] in cfg["zones"]:
                cfg["zones"].remove(i[3:])
                save_cfg()
                render()
        elif t == "layout" and msg.get("target") == "tile":
            tile_w = msg.get("width", tile_w)
            render()
        elif t == "shutdown":
            save_cfg()
            return


if __name__ == "__main__":
    main()
