import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt


# Page Replacement Algorithms
def fifo_page_replacement(pages, frame_size):
    frames = []
    page_faults = 0
    page_hits = 0
    table_data = []

    for page in pages:
        if page not in frames:
            if len(frames) < frame_size:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)
            page_faults += 1
        else:
            page_hits += 1  # Increase hit count if page is already in frames
        table_data.append((list(frames), page, page_faults, page_hits))

    return page_faults, page_hits, table_data


def lru_page_replacement(pages, frame_size):
    frames = []
    page_faults = 0
    page_hits = 0
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
            page_hits += 1  # Increase hit count if page is already in frames
            recently_used.remove(page)
            recently_used.append(page)
        table_data.append((list(frames), page, page_faults, page_hits))

    return page_faults, page_hits, table_data


def optimal_page_replacement(pages, frame_size):
    frames = []
    page_faults = 0
    page_hits = 0
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
        else:
            page_hits += 1  # Increase hit count if page is already in frames
        table_data.append((list(frames), page, page_faults, page_hits))

    return page_faults, page_hits, table_data


# Function to plot the chart
def plot_chart(fifo_faults, lru_faults, optimal_faults, fifo_hits, lru_hits, optimal_hits):
    algorithms = ['FIFO', 'LRU', 'Optimal']
    faults = [fifo_faults, lru_faults, optimal_faults]
    hits = [fifo_hits, lru_hits, optimal_hits]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Plot page faults
    ax1.bar(algorithms, faults, color=['blue', 'green', 'red'])
    ax1.set_title('Page Faults Comparison')
    ax1.set_xlabel('Algorithms')
    ax1.set_ylabel('Page Faults')

    # Plot hit rates
    hit_rates = [hits[i] / (hits[i] + faults[i]) if (hits[i] + faults[i]) > 0 else 0 for i in range(3)]
    ax2.bar(algorithms, hit_rates, color=['purple', 'orange', 'cyan'])
    ax2.set_title('Hit Rate Comparison')
    ax2.set_xlabel('Algorithms')
    ax2.set_ylabel('Hit Rate')

    plt.tight_layout()
    plt.show()


# GUI
def run_simulation():
    for row in tree.get_children():
        tree.delete(row)

    try:
        reference_string = list(map(int, reference_entry.get().split()))
        frame_size = int(frame_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid input!")
        return

    fifo_faults, fifo_hits, fifo_table = fifo_page_replacement(reference_string, frame_size)
    lru_faults, lru_hits, lru_table = lru_page_replacement(reference_string, frame_size)
    optimal_faults, optimal_hits, optimal_table = optimal_page_replacement(reference_string, frame_size)

    # Display table for FIFO algorithm
    for i, (frame_state, current_page, faults, hits) in enumerate(fifo_table):
        hit_rate = hits / (hits + faults) if (hits + faults) > 0 else 0  # Calculate hit rate
        tree.insert("", "end", values=[i + 1, current_page] + frame_state + [faults, hits, f"{hit_rate:.2%}"])

    # Display chart
    plot_chart(fifo_faults, lru_faults, optimal_faults, fifo_hits, lru_hits, optimal_hits)


# Create main window
root = tk.Tk()
root.title("Page Replacement Algorithms")
root.geometry("900x600")  # Adjusted size for larger window

# Labels and inputs
tk.Label(root, text="Reference String (e.g. 7 0 1 2 0 3 0 4)").pack(pady=5)
reference_entry = tk.Entry(root, width=60)  # Increased input width
reference_entry.pack(pady=5)

tk.Label(root, text="Frame Size (e.g. 3)").pack(pady=5)
frame_entry = tk.Entry(root, width=10)
frame_entry.pack(pady=5)

# Run button
run_button = tk.Button(root, text="Run Simulation", command=run_simulation)
run_button.pack(pady=10)

# Treeview to display page replacement steps
tree = ttk.Treeview(root,
                    columns=("Step", "Current Page", "Frame 1", "Frame 2", "Frame 3", "Faults", "Hits", "Hit Rate"),
                    show="headings")
tree.heading("Step", text="Step")
tree.heading("Current Page", text="Current Page")
tree.heading("Frame 1", text="Frame 1")
tree.heading("Frame 2", text="Frame 2")
tree.heading("Frame 3", text="Frame 3")
tree.heading("Faults", text="Page Faults")
tree.heading("Hits", text="Page Hits")
tree.heading("Hit Rate", text="Hit Rate")

# Increase width of columns
tree.column("Step", width=100)
tree.column("Current Page", width=100)
tree.column("Frame 1", width=100)
tree.column("Frame 2", width=100)
tree.column("Frame 3", width=100)
tree.column("Faults", width=100)
tree.column("Hits", width=100)
tree.column("Hit Rate", width=100)

# Change colors and appearance of the table
tree.tag_configure('even', background="#f0f0f0")
tree.tag_configure('odd', background="#ffffff")
tree.pack(pady=10, expand=True, fill='both')

# Run the main window
root.mainloop()
