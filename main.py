import tkinter as tk
from tkinter import messagebox


# الگوریتم‌های جایگزینی صفحه
def fifo_page_replacement(pages, frame_size):
    frames = []
    page_faults = 0
    for page in pages:
        if page not in frames:
            if len(frames) < frame_size:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)
            page_faults += 1
    return page_faults


def lru_page_replacement(pages, frame_size):
    frames = []
    page_faults = 0
    recently_used = []

    for page in pages:
        if page not in frames:
            if len(frames) < frame_size:
                frames.append(page)
                recently_used.append(page)
            else:
                lru_page = recently_used.pop(0)
                frames[frames.index(lru_page)] = page
                recently_used.append(page)
            page_faults += 1
        else:
            recently_used.remove(page)
            recently_used.append(page)
    return page_faults


def optimal_page_replacement(pages, frame_size):
    frames = []
    page_faults = 0

    for i, page in enumerate(pages):
        if page not in frames:
            if len(frames) < frame_size:
                frames.append(page)
            else:
                future_uses = []
                for frame in frames:
                    if frame not in pages[i + 1:]:
                        future_uses.append(float('inf'))
                    else:
                        future_uses.append(pages[i + 1:].index(frame))
                farthest_page = frames[future_uses.index(max(future_uses))]
                frames[frames.index(farthest_page)] = page
            page_faults += 1
    return page_faults


# رابط گرافیکی
def run_simulation():
    try:
        reference_string = list(map(int, reference_entry.get().split()))
        frame_size = int(frame_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid input!")
        return

    fifo_faults = fifo_page_replacement(reference_string, frame_size)
    lru_faults = lru_page_replacement(reference_string, frame_size)
    optimal_faults = optimal_page_replacement(reference_string, frame_size)

    result_text = (
        f"FIFO Page Faults: {fifo_faults}\n"
        f"LRU Page Faults: {lru_faults}\n"
        f"Optimal Page Faults: {optimal_faults}"
    )
    result_label.config(text=result_text)


# ایجاد پنجره اصلی
root = tk.Tk()
root.title("Page Replacement Algorithms")

# لیبل‌ها و ورودی‌ها
tk.Label(root, text="Reference String (e.g. 7 0 1 2 0 3 0 4)").pack(pady=5)
reference_entry = tk.Entry(root, width=50)
reference_entry.pack(pady=5)

tk.Label(root, text="Frame Size (e.g. 3)").pack(pady=5)
frame_entry = tk.Entry(root, width=10)
frame_entry.pack(pady=5)

# دکمه اجرا
run_button = tk.Button(root, text="Run Simulation", command=run_simulation)
run_button.pack(pady=10)

# نمایش نتیجه
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

# اجرای پنجره
root.mainloop()
