import tkinter as tk
from tkinter import ttk, messagebox

from file_manager import (
    initialize_data_files,
    load_airport_objects,
    load_flight_objects,
    read_airports_2d,
    read_flights_2d,
    write_booking,
    read_bookings,
)
from utils import APP_NAME


# ============================================================
#  THEME
# ============================================================
BG        = "#0B1020"   # app background
PANEL     = "#141B33"   # cards / sidebar
PANEL_2   = "#1B2447"   # hover / alt rows
ACCENT    = "#5B8DEF"   # primary
ACCENT_2  = "#7C5CFF"   # secondary
SUCCESS   = "#22C55E"
DANGER    = "#EF4444"
TEXT      = "#E6ECFF"
MUTED     = "#8A93B8"
BORDER    = "#222C53"

FONT_H1   = ("Segoe UI", 22, "bold")
FONT_H2   = ("Segoe UI", 14, "bold")
FONT_BODY = ("Segoe UI", 11)
FONT_BTN  = ("Segoe UI Semibold", 11)


# ============================================================
#  Reusable widgets
# ============================================================
class HoverButton(tk.Canvas):
    """Flat, rounded, hover-animated button."""
    def __init__(self, parent, text, command=None, width=220, height=44,
                 bg=ACCENT, fg="white", hover=ACCENT_2, icon=""):
        super().__init__(parent, width=width, height=height,
                         bg=parent["bg"], highlightthickness=0, bd=0)
        self.command = command
        self.bg, self.fg, self.hover = bg, fg, hover
        self.text = f"  {icon}   {text}" if icon else text
        self.width, self.height = width, height
        self._draw(bg)
        self.bind("<Enter>", lambda e: self._draw(self.hover))
        self.bind("<Leave>", lambda e: self._draw(self.bg))
        self.bind("<Button-1>", lambda e: command() if command else None)

    def _rounded(self, fill, r=12):
        self.delete("all")
        w, h = self.width, self.height
        self.create_oval(0, 0, 2*r, 2*r, fill=fill, outline=fill)
        self.create_oval(w-2*r, 0, w, 2*r, fill=fill, outline=fill)
        self.create_oval(0, h-2*r, 2*r, h, fill=fill, outline=fill)
        self.create_oval(w-2*r, h-2*r, w, h, fill=fill, outline=fill)
        self.create_rectangle(r, 0, w-r, h, fill=fill, outline=fill)
        self.create_rectangle(0, r, w, h-r, fill=fill, outline=fill)

    def _draw(self, fill):
        self._rounded(fill)
        self.create_text(self.width/2, self.height/2,
                         text=self.text, fill=self.fg, font=FONT_BTN)


def style_entry(entry):
    entry.configure(bg=PANEL_2, fg=TEXT, insertbackground=TEXT,
                    relief="flat", font=FONT_BODY,
                    highlightthickness=1, highlightbackground=BORDER,
                    highlightcolor=ACCENT)


def make_modal(root, title, w=560, h=480):
    win = tk.Toplevel(root)
    win.title(title)
    win.configure(bg=BG)
    win.geometry(f"{w}x{h}")
    win.transient(root)
    # Header bar
    header = tk.Frame(win, bg=PANEL, height=60)
    header.pack(fill="x")
    tk.Label(header, text=title, bg=PANEL, fg=TEXT,
             font=FONT_H2).pack(side="left", padx=20, pady=14)
    tk.Frame(win, bg=BORDER, height=1).pack(fill="x")
    body = tk.Frame(win, bg=BG)
    body.pack(fill="both", expand=True, padx=24, pady=20)
    return win, body


def scrollable_list(parent, items, empty_msg="Nothing to show"):
    if not items:
        tk.Label(parent, text=empty_msg, bg=BG, fg=MUTED,
                 font=FONT_BODY).pack(pady=30)
        return

    canvas = tk.Canvas(parent, bg=BG, highlightthickness=0)
    sb = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=BG)
    inner.bind("<Configure>",
               lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=sb.set)
    canvas.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")

    for i, text in enumerate(items):
        bg = PANEL if i % 2 == 0 else PANEL_2
        card = tk.Frame(inner, bg=bg)
        card.pack(fill="x", pady=4, padx=2)
        tk.Label(card, text="✈", bg=bg, fg=ACCENT,
                 font=("Segoe UI", 14)).pack(side="left", padx=12, pady=10)
        tk.Label(card, text=text, bg=bg, fg=TEXT, font=FONT_BODY,
                 anchor="w", justify="left",
                 wraplength=460).pack(side="left", fill="x",
                                      expand=True, pady=10, padx=(0, 12))


# ============================================================
#  Main App
# ============================================================
class AirToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("960x620")
        self.root.configure(bg=BG)
        self.root.minsize(880, 560)

        initialize_data_files()
        self.airports = load_airport_objects(read_airports_2d())
        self.flights  = load_flight_objects(read_flights_2d())

        self._build_layout()

    # ----------------------------------------------------------
    def _build_layout(self):
        # Sidebar
        sidebar = tk.Frame(self.root, bg=PANEL, width=260)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="✈  AirTool", bg=PANEL, fg=TEXT,
                 font=FONT_H1).pack(pady=(28, 6), padx=24, anchor="w")
        tk.Label(sidebar, text="Flight Management Suite",
                 bg=PANEL, fg=MUTED, font=("Segoe UI", 10)
                 ).pack(padx=24, anchor="w")
        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", pady=20, padx=20)

        nav = [
            ("🛬", "View Airports",   self.view_airports),
            ("🔎", "Search Airport",  self.search_airport),
            ("🛫", "View Flights",    self.view_flights),
            ("🧭", "Search Flight",   self.search_flight),
            ("🎟️", "Book Flight",     self.book_flight),
            ("📒", "View Bookings",   self.view_bookings),
        ]
        for icon, label, cmd in nav:
            HoverButton(sidebar, label, command=cmd, icon=icon,
                        width=220, bg=PANEL, hover=PANEL_2,
                        fg=TEXT).pack(pady=4, padx=20)

        HoverButton(sidebar, "Exit", command=self.root.quit, icon="⏻",
                    width=220, bg=PANEL, hover=DANGER,
                    fg=MUTED).pack(side="bottom", pady=24, padx=20)

        # Main content
        main = tk.Frame(self.root, bg=BG)
        main.pack(side="left", fill="both", expand=True)

        tk.Label(main, text="Dashboard", bg=BG, fg=TEXT,
                 font=FONT_H1).pack(anchor="w", padx=32, pady=(28, 4))
        tk.Label(main, text="Manage airports, flights and bookings at a glance.",
                 bg=BG, fg=MUTED, font=FONT_BODY).pack(anchor="w", padx=32)

        # Stat cards
        stats = tk.Frame(main, bg=BG)
        stats.pack(fill="x", padx=24, pady=24)
        self._stat_card(stats, "Airports", len(self.airports), ACCENT)
        self._stat_card(stats, "Flights",  len(self.flights),  ACCENT_2)
        self._stat_card(stats, "Bookings", len(read_bookings()), SUCCESS)

        # Hint panel
        hint = tk.Frame(main, bg=PANEL)
        hint.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        tk.Label(hint, text="Quick Start", bg=PANEL, fg=TEXT,
                 font=FONT_H2).pack(anchor="w", padx=24, pady=(20, 6))
        tk.Label(hint,
                 text="Use the sidebar to browse airports, search flights,\n"
                      "or book a seat. Everything is saved automatically.",
                 bg=PANEL, fg=MUTED, font=FONT_BODY,
                 justify="left").pack(anchor="w", padx=24, pady=(0, 20))

    def _stat_card(self, parent, label, value, color):
        card = tk.Frame(parent, bg=PANEL, width=200, height=110)
        card.pack(side="left", padx=8, fill="both", expand=True)
        card.pack_propagate(False)
        tk.Label(card, text=label, bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 11)).pack(anchor="w", padx=20, pady=(18, 0))
        tk.Label(card, text=str(value), bg=PANEL, fg=color,
                 font=("Segoe UI", 28, "bold")).pack(anchor="w", padx=20)

    # ----------------------------------------------------------
    #  Actions
    # ----------------------------------------------------------
    def view_airports(self):
        _, body = make_modal(self.root, "All Airports", 620, 520)
        scrollable_list(body, [a.get_summary() for a in self.airports],
                        "No airports found")

    def view_flights(self):
        _, body = make_modal(self.root, "All Flights", 620, 520)
        scrollable_list(body, [f.get_summary() for f in self.flights],
                        "No flights found")

    def search_airport(self):
        self._search_modal("Search Airport", "Airport name or city",
                           self._airport_match)

    def search_flight(self):
        self._search_modal("Search Flight", "Destination",
                           self._flight_match)

    def _airport_match(self, q):
        q = q.lower()
        return [a.get_summary() for a in self.airports
                if (hasattr(a, "name") and q in a.name.lower())
                or (hasattr(a, "city") and q in a.city.lower())]

    def _flight_match(self, q):
        q = q.lower()
        return [f.get_summary() for f in self.flights
                if hasattr(f, "destination") and q in f.destination.lower()]

    def _search_modal(self, title, placeholder, matcher):
        win, body = make_modal(self.root, title, 620, 540)
        tk.Label(body, text=placeholder, bg=BG, fg=MUTED,
                 font=FONT_BODY).pack(anchor="w")
        entry = tk.Entry(body)
        style_entry(entry)
        entry.pack(fill="x", ipady=8, pady=(6, 14))

        results_frame = tk.Frame(body, bg=BG)
        results_frame.pack(fill="both", expand=True)

        def run():
            for w in results_frame.winfo_children():
                w.destroy()
            scrollable_list(results_frame, matcher(entry.get()),
                            "No results found")

        HoverButton(body, "Search", command=run, icon="🔍",
                    width=140, height=40).pack(anchor="e", pady=10)
        entry.bind("<Return>", lambda e: run())
        entry.focus()

    def book_flight(self):
        win, body = make_modal(self.root, "Book a Flight", 520, 320)
        tk.Label(body, text="Flight Number", bg=BG, fg=MUTED,
                 font=FONT_BODY).pack(anchor="w")
        entry = tk.Entry(body)
        style_entry(entry)
        entry.pack(fill="x", ipady=8, pady=(6, 20))
        entry.focus()

        def book():
            fn = entry.get().strip()
            for f in self.flights:
                if hasattr(f, "flight_number") and f.flight_number == fn:
                    write_booking(fn)
                    messagebox.showinfo("Booked ✅",
                                        f"Flight {fn} booked successfully!")
                    win.destroy()
                    return
            messagebox.showerror("Not found", f"Flight '{fn}' was not found.")

        HoverButton(body, "Confirm Booking", command=book, icon="🎟️",
                    width=200, height=44, bg=SUCCESS,
                    hover="#16A34A").pack(anchor="e")

    def view_bookings(self):
        _, body = make_modal(self.root, "Your Bookings", 620, 520)
        bookings = read_bookings()
        scrollable_list(body, [str(b) for b in bookings],
                        "No bookings yet")


# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    AirToolGUI(root)
    root.mainloop()
