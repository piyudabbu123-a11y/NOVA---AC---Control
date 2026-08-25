import tkinter as tk
import math
import random
import datetime
import psutil
import socket

# ───────────────── COLORS ─────────────────
BG        = "#040d18"
CYAN      = "#00e5ff"
BLUE      = "#1565c0"
GLOW      = "#29b6f6"
WHITE     = "#ffffff"
GREY      = "#607d8b"
DARK      = "#0d1b2a"
GREEN     = "#00e676"
RED       = "#ff1744"
ORANGE    = "#ff9100"
BORDER    = "#1a3a5c"
SNOW      = "#e3f2fd"
DIM_CYAN  = "#004455"

# ───────────────── WINDOW ─────────────────
root = tk.Tk()
root.title("NOVA — Smart AC Control")
screen_w = root.winfo_screenwidth()
x = screen_w - 1020
y = 20

root.geometry(f"1000x1000+{x}+{y}")

root.configure(bg=BG)
root.resizable(False, False)

C = tk.Canvas(
    root,
    width=1000,
    height=900,
    bg=BG,
    highlightthickness=0
)
C.pack()

# ───────────────── GRID ─────────────────
for x in range(0, 1000, 40):
    C.create_line(x, 0, x, 900, fill="#08131f")

for y in range(0, 900, 40):
    C.create_line(0, y, 1000, y, fill="#08131f")

# ───────────────── PARTICLES ─────────────────
PTS = []

for _ in range(50):
    x = random.randint(0, 1000)
    y = random.randint(0, 900)

    size = random.choice([1, 2, 2, 3])

    p = C.create_oval(
        x, y,
        x + size,
        y + size,
        fill=random.choice(
            [CYAN, GLOW, BLUE, "#006688"]
        ),
        outline=""
    )

    PTS.append({
        "id": p,
        "x": x,
        "y": y,
        "sp": random.uniform(0.3, 1.3),
        "sz": size
    })

def _pts():
    for p in PTS:

        p["y"] -= p["sp"]

        if p["y"] < -5:
            p["y"] = 905
            p["x"] = random.randint(0, 1000)

        C.coords(
            p["id"],
            p["x"], p["y"],
            p["x"] + p["sz"],
            p["y"] + p["sz"]
        )

    root.after(30, _pts)

# ───────────────── SNOW ─────────────────
snow_on = False
SNOW_P = []

for _ in range(40):

    x = random.randint(0, 1000)
    y = random.randint(-900, 0)

    s = C.create_text(
        x,
        y,
        text="❄",
        fill=SNOW,
        font=("Arial", 10)
    )

    SNOW_P.append({
        "id": s,
        "x": x,
        "y": y,
        "sp": random.uniform(0.5, 2)
    })

    C.itemconfig(s, state="hidden")

def _snow():

    if snow_on:

        for s in SNOW_P:

            s["y"] += s["sp"]

            if s["y"] > 905:
                s["y"] = random.randint(-50, -5)
                s["x"] = random.randint(0, 1000)

            C.coords(
                s["id"],
                s["x"],
                s["y"]
            )

            C.itemconfig(
                s["id"],
                state="normal"
            )

    else:
        for s in SNOW_P:
            C.itemconfig(
                s["id"],
                state="hidden"
            )

    root.after(40, _snow)

# ───────────────── HEADER ─────────────────
C.create_rectangle(
    0, 0, 1000, 70,
    fill="#020912",
    outline=""
)

C.create_line(
    0, 70,
    1000, 70,
    fill=CYAN,
    width=2
)

title_obj = C.create_text(
    500,
    35,
    text="✦  N O V A   A C   C O N T R O L  ✦",
    fill=CYAN,
    font=("Courier", 18, "bold")
)

clk_h = C.create_text(
    920,
    22,
    text="",
    fill=GLOW,
    font=("Courier", 13, "bold")
)

clk_d = C.create_text(
    920,
    48,
    text="",
    fill=GREY,
    font=("Courier", 9)
)

def _clk():
    now = datetime.datetime.now()

    C.itemconfig(
        clk_h,
        text=now.strftime("%I:%M %p")
    )

    C.itemconfig(
        clk_d,
        text=now.strftime("%d %b %Y")
    )

    root.after(1000, _clk)

    # ───────────────── AC UNIT ─────────────────

# Outer frame
for i in range(4, 0, -1):
    C.create_rectangle(
        20 - i, 80 - i,
        980 + i, 450 + i,
        outline=BORDER,
        width=1
    )

C.create_rectangle(
    20, 80, 980, 430,
    fill="#06111f",
    outline=CYAN,
    width=2
)

C.create_rectangle(
    28, 88, 972, 422,
    fill=DARK,
    outline=BORDER
)

# Brand bar
C.create_rectangle(
    28, 88, 972, 115,
    fill="#08131f",
    outline=BORDER
)

C.create_text(
    140, 101,
    text="NOVA",
    fill=CYAN,
    font=("Courier", 14, "bold")
)

C.create_text(
    500, 101,
    text="SMART SERIES v3.0",
    fill=GREY,
    font=("Courier", 10)
)

# ───────── LEFT PANEL ─────────

C.create_rectangle(
    35, 125,
    500, 300,
    fill="#020810",
    outline=BORDER
)

C.create_text(
    265, 140,
    text="CURRENT TEMPERATURE",
    fill=GREY,
    font=("Courier", 9)
)

# Snow icon
sf_cx = 100
sf_cy = 200

C.create_oval(
    60, 160,
    140, 240,
    outline=CYAN,
    width=2
)

sf_lines = []

for _ in range(6):
    ln = C.create_line(
        sf_cx, sf_cy,
        sf_cx, sf_cy,
        fill=CYAN,
        width=2
    )
    sf_lines.append(ln)

def _sf():

    global sf_angle

    try:
        sf_angle += 2
    except:
        sf_angle = 0

    for i, ln in enumerate(sf_lines):

        a = math.radians(
            sf_angle + i * 60
        )

        C.coords(
            ln,
            sf_cx,
            sf_cy,
            sf_cx + 35 * math.cos(a),
            sf_cy + 35 * math.sin(a)
        )

    root.after(30, _sf)

temp_cur = C.create_text(
    320,
    200,
    text="24",
    fill=CYAN,
    font=("Courier", 70, "bold")
)

C.create_text(
    420,
    160,
    text="°C",
    fill=CYAN,
    font=("Courier", 24, "bold")
)

C.create_text(
    270,
    280,
    text="COOL MODE",
    fill=CYAN,
    font=("Courier", 11, "bold")
)

# ───────── RIGHT PANEL ─────────

C.create_rectangle(
    520, 125,
    780, 300,
    fill="#020810",
    outline=BORDER
)

C.create_text(
    650,
    140,
    text="TARGET TEMPERATURE",
    fill=GREY,
    font=("Courier", 9)
)

C.create_text(
    650,
    205,
    text="24",
    fill=CYAN,
    font=("Courier", 58, "bold")
)

C.create_text(
    720,
    165,
    text="°C",
    fill=CYAN,
    font=("Courier", 22, "bold")
)

# Buttons
C.create_rectangle(
    535, 250,
    620, 285,
    fill="#0a1828",
    outline=BORDER
)

C.create_text(
    578, 268,
    text="-",
    fill=GREY,
    font=("Courier", 20, "bold")
)

C.create_rectangle(
    680, 250,
    765, 285,
    fill="#0a1828",
    outline=BORDER
)

C.create_text(
    722, 268,
    text="+",
    fill=GREY,
    font=("Courier", 20, "bold")
)

# ───────── MODE LIGHTS ─────────

C.create_rectangle(
    800, 125,
    972, 300,
    fill="#020810",
    outline=BORDER
)

MD = [
    ("COOL", 855, 155),
    ("FAN", 925, 155),
    ("AUTO", 855, 230),
    ("ECO", 925, 230)
]

ml = {}

for name, x, y in MD:

    C.create_text(
        x, y,
        text=name,
        fill=GREY,
        font=("Courier", 9)
    )

    dot = C.create_oval(
        x - 12,
        y + 15,
        x + 12,
        y + 39,
        fill=GREY,
        outline=BORDER
    )

    ml[name] = dot

# ───────── VENTS ─────────

vents = []

for i in range(8):

    y = 320 + i * 10

    v = C.create_rectangle(
        35, y,
        740, y + 6,
        fill="#102030",
        outline=BORDER
    )

    vents.append(v)

    C.create_rectangle(
        875, y,
        972, y + 6,
        fill="#102030",
        outline=BORDER
    )

# ───────── POWER BUTTON ─────────

pb_cx = 805
pb_cy = 355

for r in [46, 42, 38, 34]:

    C.create_oval(
        pb_cx - r,
        pb_cy - r,
        pb_cx + r,
        pb_cy + r,
        outline=RED
    )

pwr_ring = C.create_oval(
    pb_cx - 36,
    pb_cy - 36,
    pb_cx + 36,
    pb_cy + 36,
    outline=RED,
    width=4,
    fill="#0a0010"
)

pwr_btn = C.create_oval(
    pb_cx - 24,
    pb_cy - 24,
    pb_cx + 24,
    pb_cy + 24,
    fill=RED,
    outline=""
)

C.create_text(
    pb_cx,
    pb_cy,
    text="⏻",
    fill=WHITE,
    font=("Courier", 20, "bold")
)

# ───────── STATUS BAR ─────────

C.create_line(
    20, 465,
    980, 465,
    fill=BORDER
)

st_dot = C.create_oval(
    30, 475,
    46, 491,
    fill=RED,
    outline=""
)

st_txt = C.create_text(
    500,
    483,
    text="SYSTEM STATUS : OFFLINE",
    fill=RED,
    font=("Courier", 13, "bold")
)

# ═══════════════════════════════════════════════════════
# BOTTOM PANEL
# ═══════════════════════════════════════════════════════

C.create_rectangle(
    20, 470,
    980, 640,
    fill="#050e1c",
    outline=BORDER,
    width=1
)

# ───────────────── TIMER PANEL ─────────────────

C.create_rectangle(
    20, 470,
    300, 640,
    fill="#030b16",
    outline=BORDER
)

C.create_text(
    160, 520,
    text="FUTURISTIC TIMER",
    fill=CYAN,
    font=("Courier", 11, "bold")
)

tc_x = 160
tc_y = 585
tc_r = 52

# Outer circle
C.create_oval(
    tc_x - tc_r,
    tc_y - tc_r,
    tc_x + tc_r,
    tc_y + tc_r,
    outline=CYAN,
    width=2
)

# Tick marks
for i in range(60):

    a = math.radians(i * 6 - 90)

    r1 = tc_r - (10 if i % 5 == 0 else 5)

    x1 = tc_x + r1 * math.cos(a)
    y1 = tc_y + r1 * math.sin(a)

    x2 = tc_x + tc_r * math.cos(a)
    y2 = tc_y + tc_r * math.sin(a)

    C.create_line(
        x1, y1,
        x2, y2,
        fill=CYAN if i % 5 == 0 else BORDER
    )

# Progress Arc
t_arc = C.create_arc(
    tc_x - tc_r + 8,
    tc_y - tc_r + 8,
    tc_x + tc_r - 8,
    tc_y + tc_r - 8,
    start=90,
    extent=360,
    style="arc",
    outline=CYAN,
    width=5
)

# Center icon
C.create_text(
    tc_x,
    tc_y - 8,
    text="◔",
    fill=CYAN,
    font=("Courier", 18, "bold")
)

t_txt = C.create_text(
    tc_x,
    tc_y + 25,
    text="15:00",
    fill=CYAN,
    font=("Courier", 18, "bold")
)

t_lbl = C.create_text(
    tc_x,
    650,
    text="TIMER INACTIVE",
    fill=GREY,
    font=("Courier", 8)
)

t_hand = C.create_line(
    tc_x,
    tc_y,
    tc_x,
    tc_y - 35,
    fill=CYAN,
    width=2
)

tr = [0]
tt = [900]
af_run = [False]

def _timer_dial():

    if tr[0] > 0 and af_run[0]:

        prog = tr[0] / tt[0]

        extent = prog * 360

        color = (
            GREEN if prog > 0.5
            else ORANGE if prog > 0.2
            else RED
        )

        C.itemconfig(
            t_arc,
            extent=extent,
            outline=color
        )

        m = tr[0] // 60
        s = tr[0] % 60

        C.itemconfig(
            t_txt,
            text=f"{m:02d}:{s:02d}",
            fill=color
        )

        angle = math.radians(
            90 - (1 - prog) * 360
        )

        hx = tc_x + 35 * math.cos(angle)
        hy = tc_y - 35 * math.sin(angle)

        C.coords(
            t_hand,
            tc_x,
            tc_y,
            hx,
            hy
        )

        C.itemconfig(
            t_hand,
            fill=color
        )

        C.itemconfig(
            t_lbl,
            text="TIMER ACTIVE",
            fill=GREEN
        )

        tr[0] -= 1

        root.after(
            1000,
            _timer_dial
        )

    else:

        C.itemconfig(
            t_arc,
            extent=360,
            outline=GREY
        )

        C.itemconfig(
            t_txt,
            text="15:00",
            fill=GREY
        )

        C.itemconfig(
            t_lbl,
            text="TIMER INACTIVE",
            fill=GREY
        )

# ───────────────── RIGHT PANEL ─────────────────

C.create_rectangle(
    320, 470,
    980, 640,
    fill="#030b16",
    outline=BORDER
)

# Airflow
C.create_text(
    650, 525,
    text="A I R F L O W",
    fill=GREY,
    font=("Courier", 8)
)

af_disp = C.create_text(
    650,
    550,
    text="",
    fill=CYAN,
    font=("Courier", 12, "bold")
)

AF = [
    "▷ ▷ ▷ ▷ ▷ ▷ ▷",
    " ▷ ▷ ▷ ▷ ▷ ▷ ",
    "  ▷ ▷ ▷ ▷ ▷  ",
    "   ▷ ▷ ▷ ▷   "
]

af_i = [0]

def _af():

    if af_run[0]:

        C.itemconfig(
            af_disp,
            text=AF[af_i[0]]
        )

        af_i[0] = (
            af_i[0] + 1
        ) % len(AF)

    else:
        C.itemconfig(
            af_disp,
            text=""
        )

    root.after(
        150,
        _af
    )

# Voice bars
C.create_text(
    650,
    585,
    text="VOICE INPUT",
    fill=GREY,
    font=("Courier", 8)
)

lm = [False]

vb = []
vbh = [0] * 30

for i in range(30):

    x = 350 + i * 18

    b = C.create_rectangle(
        x,
        640,
        x + 5,
        640,
        fill=GREY,
        outline=""
    )

    vb.append(b)

def _vb():

    for i, b in enumerate(vb):

        target = (
            random.randint(8, 45)
            if lm[0]
            else random.randint(1, 5)
        )

        vbh[i] = int(
            vbh[i] * 0.55
            + target * 0.45
        )

        h = vbh[i]

        x = 350 + i * 18

        C.coords(
            b,
            x,
            640 - h,
            x + 5,
            640
        )

        C.itemconfig(
            b,
            fill=CYAN if lm[0]
            else GREY
        )

    root.after(
        70,
        _vb
    )

    # ═══════════════════════════════════════════════════════
# SYSTEM DIAGNOSTICS
# ═══════════════════════════════════════════════════════

C.create_line(
    20, 660,
    980, 660,
    fill=BORDER,
    width=1
)

C.create_text(
    160,
    675,
    text="[ SYSTEM DIAGNOSTICS ]",
    fill=GREY,
    font=("Courier", 8)
)

d_cpu = C.create_text(
    90, 695,
    text="CPU: --",
    fill=GLOW,
    font=("Courier", 10)
)

d_mem = C.create_text(
    300, 695,
    text="MEM: --",
    fill=GLOW,
    font=("Courier", 10)
)

d_net = C.create_text(
    550, 695,
    text="NET: --",
    fill=GLOW,
    font=("Courier", 10)
)

d_sys = C.create_text(
    820, 695,
    text="SYS: --",
    fill=GLOW,
    font=("Courier", 10)
)

def _diag():

    try:

        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent

        C.itemconfig(
            d_cpu,
            text=f"CPU: {cpu:.0f}%"
        )

        C.itemconfig(
            d_mem,
            text=f"MEM: {mem:.0f}%"
        )

        try:
            socket.create_connection(
                ("8.8.8.8", 53),
                timeout=1
            )

            C.itemconfig(
                d_net,
                text="NET: ONLINE",
                fill=GREEN
            )

        except:
            C.itemconfig(
                d_net,
                text="NET: OFFLINE",
                fill=RED
            )

        C.itemconfig(
            d_sys,
            text="SYS: OK",
            fill=GREEN
        )

    except:
        pass

    root.after(3000, _diag)

# ═══════════════════════════════════════════════════════
# NOVA LOG
# ═══════════════════════════════════════════════════════

C.create_line(
    20, 710,
    980, 710,
    fill=BORDER,
    width=1
)

C.create_text(
    110,
    725,
    text="[ NOVA LOG ]",
    fill=GREY,
    font=("Courier", 8)
)

C.create_rectangle(
    28,
    735,
    972,
    785,
    fill="#060c17",
    outline=BORDER
)

log_t = C.create_text(
    500,
    760,
    text="⚡ Initializing NOVA AI Core...",
    fill=CYAN,
    font=("Courier", 10),
    width=920,
    justify="center"
)

# ═══════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════

C.create_text(
    500,
    820,
    text="Say 'Nova' to wake me up",
    fill=CYAN,
    font=("Courier", 16, "bold")
)

C.create_text(
    500,
    845,
    text="Turn On AC | Turn Off AC | Change Temperature | Status",
    fill=GREY,
    font=("Courier", 9)
)

# ═══════════════════════════════════════════════════════
# UPDATE UI
# ═══════════════════════════════════════════════════════

def updateUI(
    ac_on,
    current_temp,
    timer_seconds=None,
    log=""
):

    global snow_on

    if ac_on:

        snow_on = True
        af_run[0] = True

        C.itemconfig(
            temp_cur,
            text=str(current_temp),
            fill=CYAN
        )

        C.itemconfig(
            pwr_btn,
            fill=GREEN
        )

        C.itemconfig(
            pwr_ring,
            outline=GREEN
        )

        C.itemconfig(
            st_dot,
            fill=GREEN
        )

        C.itemconfig(
            st_txt,
            text="SYSTEM STATUS : ONLINE",
            fill=GREEN
        )

        C.itemconfig(
            ml["COOL"],
            fill=CYAN
        )

        C.itemconfig(
            ml["AUTO"],
            fill=GLOW
        )

        C.itemconfig(
            ml["ECO"],
            fill=GREEN
        )

        if timer_seconds:
            tr[0] = timer_seconds
            tt[0] = timer_seconds
            _timer_dial()

    else:

        snow_on = False
        af_run[0] = False
        tr[0] = 0

        C.itemconfig(
            pwr_btn,
            fill=RED
        )

        C.itemconfig(
            pwr_ring,
            outline=RED
        )

        C.itemconfig(
            st_dot,
            fill=RED
        )

        C.itemconfig(
            st_txt,
            text="SYSTEM STATUS : OFFLINE",
            fill=RED
        )

    if log:
        C.itemconfig(
            log_t,
            text=f"» {log}"
        )

# ═══════════════════════════════════════════════════════
# LISTENING
# ═══════════════════════════════════════════════════════

def setListening(val):

    lm[0] = val


def startUI():

    root.after(100, _pts)
    root.after(100, _snow)
    root.after(100, _clk)
    root.after(100, _sf)
    root.after(100, _af)
    root.after(100, _vb)
    root.after(100, _diag)

    root.mainloop()