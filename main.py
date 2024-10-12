import tkinter as tk
from collections import OrderedDict, deque
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

# Page Replacement Algorithms

# FIFO Page Replacement
def fifo_page_replacement(pages, frame_size):
    frames = deque()
    page_faults = 0
    page_hits = 0
    table_data = []

    for page in pages:
        if page not in frames:
            if len(frames) < frame_size:
                frames.append(page)
            else:
                frames.popleft()
                frames.append(page)
            page_faults += 1
            status = "Fault"
        else:
            page_hits += 1
            status = "Hit"

        table_data.append((list(frames), page, page_faults, page_hits, status))

    return page_faults, page_hits, table_data


# LRU Page Replacement
def lru_page_replacement(pages, frame_size):
    frames = OrderedDict()
    page_faults = 0
    page_hits = 0
    table_data = []

    for page in pages:
        if page not in frames:
            if len(frames) < frame_size:
                frames[page] = True
            else:
                frames.popitem(last=False)
                frames[page] = True
            page_faults += 1
            status = "Fault"
        else:
            page_hits += 1
            frames.move_to_end(page)
            status = "Hit"

        table_data.append((list(frames.keys()), page, page_faults, page_hits, status))

    return page_faults, page_hits, table_data


# Optimal Page Replacement
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
                future_uses = [pages[i + 1:].index(frame) if frame in pages[i + 1:] else float('inf') for frame in frames]
                farthest_page = frames[future_uses.index(max(future_uses))]
                frames[frames.index(farthest_page)] = page
            page_faults += 1
            status = "Fault"
        else:
            page_hits += 1
            status = "Hit"

        table_data.append((list(frames), page, page_faults, page_hits, status))

    return page_faults, page_hits, table_data


# Clock Page Replacement
def clock_page_replacement(pages, frame_size):
    frames = [-1] * frame_size  # Initialize empty frames
    use_bit = [0] * frame_size  # Use bit for each frame
    pointer = 0  # Pointer for clock hand
    page_faults = 0
    page_hits = 0
    table_data = []

    for page in pages:
        if page in frames:  # If page already exists in memory
            page_hits += 1
            use_bit[frames.index(page)] = 1  # Set use bit to 1
            status = "Hit"
        else:
            # Clock algorithm to replace page
            while use_bit[pointer] == 1:
                use_bit[pointer] = 0
                pointer = (pointer + 1) % frame_size

            frames[pointer] = page
            use_bit[pointer] = 1
            pointer = (pointer + 1) % frame_size
            page_faults += 1
            status = "Fault"

        table_data.append((list(frames), page, page_faults, page_hits, status))

    return page_faults, page_hits, table_data


# Function to plot comparison charts
def plot_chart(fifo_faults, lru_faults, optimal_faults, clock_faults, fifo_hits, lru_hits, optimal_hits, clock_hits):
    algorithms = ['FIFO', 'LRU', 'Optimal', 'Clock']
    faults = [fifo_faults, lru_faults, optimal_faults, clock_faults]
    hits = [fifo_hits, lru_hits, optimal_hits, clock_hits]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Page Faults Comparison
    ax1.bar(algorithms, faults, color=['blue', 'green', 'red', 'purple'])
    ax1.set_title('Page Faults Comparison')
    ax1.set_xlabel('Algorithms')
    ax1.set_ylabel('Page Faults')

    # Hit Rates Comparison
    hit_rates = [hits[i] / (hits[i] + faults[i]) if (hits[i] + faults[i]) > 0 else 0 for i in range(4)]
    ax2.bar(algorithms, hit_rates, color=['purple', 'orange', 'cyan', 'blue'])
    ax2.set_title('Hit Rate Comparison')
    ax2.set_xlabel('Algorithms')
    ax2.set_ylabel('Hit Rate')

    plt.tight_layout()
    plt.show()


# Function to run the simulation and display results
def run_simulation():
    for row in tree.get_children():
        tree.delete(row)

    # Clear previous columns
    for col in tree["columns"]:
        tree.heading(col, text="")
        tree.column(col, width=0)

    try:
        reference_string = list(map(int, reference_entry.get().split()))
        frame_size = int(frame_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid input!")
        return

    # Define columns dynamically
    columns = ["Step", "Current Page"] + [f"Frame {i + 1}" for i in range(frame_size)] + ["Faults", "Hits", "Hit Rate", "Status"]
    tree["columns"] = columns

    # Set dynamic headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # Get results for all algorithms
    fifo_faults, fifo_hits, fifo_table = fifo_page_replacement(reference_string, frame_size)
    lru_faults, lru_hits, lru_table = lru_page_replacement(reference_string, frame_size)
    optimal_faults, optimal_hits, optimal_table = optimal_page_replacement(reference_string, frame_size)
    clock_faults, clock_hits, clock_table = clock_page_replacement(reference_string, frame_size)

    # Helper function to display table data
    def display_results(title, table_data, faults, hits):
        tree.insert("", "end", values=[f"{title} Results"] + [""] * (frame_size + 5))
        for i, (frame_state, current_page, faults, hits, status) in enumerate(table_data):
            hit_rate = hits / (hits + faults) if (hits + faults) > 0 else 0
            while len(frame_state) < frame_size:
                frame_state.append("-")
            row_values = ["Step " + str(i + 1), current_page] + frame_state + [faults, hits, f"{hit_rate:.2%}", status]
            tree.insert("", "end", values=row_values, tags=("hit" if status == "Hit" else "fault",))

        tree.insert("", "end", values=[""] * (frame_size + 7))  # Spacing

    # Display results for each algorithm
    display_results("FIFO", fifo_table, fifo_faults, fifo_hits)
    display_results("LRU", lru_table, lru_faults, lru_hits)
    display_results("Optimal", optimal_table, optimal_faults, optimal_hits)
    display_results("Clock", clock_table, clock_faults, clock_hits)

    # Display chart comparison
    plot_chart(fifo_faults, lru_faults, optimal_faults, clock_faults, fifo_hits, lru_hits, optimal_hits, clock_hits)


# Main GUI setup
root = tk.Tk()
root.title("Page Replacement Algorithms Simulation")
root.geometry("900x600")

# Input fields
tk.Label(root, text="Reference String (e.g. 7 0 1 2 0 3 0 4)").pack(pady=5)
reference_entry = tk.Entry(root, width=60)
reference_entry.pack(pady=5)

tk.Label(root, text="Frame Size (e.g. 3)").pack(pady=5)
frame_entry = tk.Entry(root, width=10)
frame_entry.pack(pady=5)

# Run simulation button
run_button = tk.Button(root, text="Run Simulation", command=run_simulation)
run_button.pack(pady=10)

# Treeview for displaying results
tree = ttk.Treeview(root, show="headings")
tree.pack(pady=10, expand=True, fill='both')

# Set colors for Hit and Fault results
tree.tag_configure('hit', background="#d4edda", foreground="green")  # Light green for Hits
tree.tag_configure('fault', background="#f8d7da", foreground="red")  # Light red for Faults

# Run the main application
root.mainloop()
