import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt


# الگوریتم‌های جایگزینی صفحه
def fifo_page_replacement(pages, frame_size):
    frames = []
    page_faults = 0
    table_data = []

    for page in pages:
        if page not in frames:
            if len(frames) < frame_size:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)
            page_faults += 1
        table_data.append((list(frames), page))  # ذخیره فریم‌ها و صفحه فعلی

    return page_faults, table_data


def lru_page_replacement(pages, frame_size):
    frames = []
    page_faults = 0
    recently_used = []
    table_data = []

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
        table_data.append((list(frames), page))  # ذخیره فریم‌ها و صفحه فعلی

    return page_faults, table_data


def optimal_page_replacement(pages, frame_size):
    frames = []
    page_faults = 0
    table_data = []

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
        table_data.append((list(frames), page))  # ذخیره فریم‌ها و صفحه فعلی

    return page_faults, table_data


# تابع برای رسم نمودار
def plot_chart(fifo_faults, lru_faults, optimal_faults):
    algorithms = ['FIFO', 'LRU', 'Optimal']
    faults = [fifo_faults, lru_faults, optimal_faults]

    plt.bar(algorithms, faults, color=['blue', 'green', 'red'])
    plt.xlabel('Algorithms')
    plt.ylabel('Page Faults')
    plt.title('Page Faults Comparison')
    plt.show()


# رابط گرافیکی
def run_simulation():
    try:
        reference_string = list(map(int, reference_entry.get().split()))
        frame_size = int(frame_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid input!")
        return

    fifo_faults, fifo_table = fifo_page_replacement(reference_string, frame_size)
    lru_faults, lru_table = lru_page_replacement(reference_string, frame_size)
    optimal_faults, optimal_table = optimal_page_replacement(reference_string, frame_size)

    # نمایش جدول برای الگوریتم FIFO
    for row in tree.get_children():
        tree.delete(row)

    # جزئیات بیشتر در جدول
    for i, (frame_state, current_page) in enumerate(fifo_table):
        tree.insert("", "end", values=[i + 1, current_page] + frame_state)

    # نمایش نمودار
    plot_chart(fifo_faults, lru_faults, optimal_faults)


# ایجاد پنجره اصلی
root = tk.Tk()
root.title("Page Replacement Algorithms")
root.geometry("800x500")  # تعیین اندازه بزرگ‌تر برای پنجره

# لیبل‌ها و ورودی‌ها
tk.Label(root, text="Reference String (e.g. 7 0 1 2 0 3 0 4)").pack(pady=5)
reference_entry = tk.Entry(root, width=60)  # افزایش عرض ورودی
reference_entry.pack(pady=5)

tk.Label(root, text="Frame Size (e.g. 3)").pack(pady=5)
frame_entry = tk.Entry(root, width=10)
frame_entry.pack(pady=5)

# دکمه اجرا
run_button = tk.Button(root, text="Run Simulation", command=run_simulation)
run_button.pack(pady=10)

# جدول برای نمایش صفحات جایگزینی (FIFO به عنوان نمونه)
tree = ttk.Treeview(root, columns=("Step", "Current Page", "Frame 1", "Frame 2", "Frame 3"), show="headings")
tree.heading("Step", text="Step")
tree.heading("Current Page", text="Current Page")
tree.heading("Frame 1", text="Frame 1")
tree.heading("Frame 2", text="Frame 2")
tree.heading("Frame 3", text="Frame 3")

# افزایش عرض و ارتفاع ستون‌ها
tree.column("Step", width=100)
tree.column("Current Page", width=100)
tree.column("Frame 1", width=100)
tree.column("Frame 2", width=100)
tree.column("Frame 3", width=100)

tree.pack(pady=10, expand=True, fill='both')

# افزایش ارتفاع ردیف‌ها
tree.tag_configure('big_row', font=('Arial', 12))  # تعیین فونت بزرگ‌تر
tree.bind("<Configure>", lambda e: tree.bind("<Configure>", lambda e: tree.see(tree.get_children())))

# اجرای پنجره
root.mainloop()
