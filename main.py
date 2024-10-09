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
            status = "Fault"  # Set status to "Fault"
        else:
            page_hits += 1
            status = "Hit"  # Set status to "Hit"
        table_data.append((list(frames), page, page_faults, page_hits, status))

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
            status = "Fault"
        else:
            page_hits += 1
            recently_used.remove(page)
            recently_used.append(page)
            status = "Hit"
        table_data.append((list(frames), page, page_faults, page_hits, status))

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
            status = "Fault"
        else:
            page_hits += 1
            status = "Hit"
        table_data.append((list(frames), page, page_faults, page_hits, status))

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

    # Clear the previous columns
    for col in tree["columns"]:
        tree.heading(col, text="")
        tree.column(col, width=0)

    try:
        reference_string = list(map(int, reference_entry.get().split()))
        frame_size = int(frame_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid input!")
        return

    # Define new columns based on the frame size
    columns = ["Step", "Current Page"] + [f"Frame {i+1}" for i in range(frame_size)] + ["Faults", "Hits", "Hit Rate", "Status"]
    tree["columns"] = columns

    # Set the headings dynamically
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # Get results for all algorithms
    fifo_faults, fifo_hits, fifo_table = fifo_page_replacement(reference_string, frame_size)
    lru_faults, lru_hits, lru_table = lru_page_replacement(reference_string, frame_size)
    optimal_faults, optimal_hits, optimal_table = optimal_page_replacement(reference_string, frame_size)

    # Display FIFO results
    tree.insert("", "end", values=["FIFO Results"] + [""] * (frame_size + 5))  # Adjust header row for FIFO
    for i, (frame_state, current_page, faults, hits, status) in enumerate(fifo_table):
        hit_rate = hits / (hits + faults) if (hits + faults) > 0 else 0
        while len(frame_state) < frame_size:  # Ensure frame_state has frame_size length
            frame_state.append("-")  # Fill empty frames with "-"
        row_values = ["Step " + str(i + 1), current_page] + frame_state + [faults, hits, f"{hit_rate:.2%}", status]
        tree.insert("", "end", values=row_values, tags=("hit" if status == "Hit" else "fault",))

    tree.insert("", "end", values=[""] * (frame_size + 7))  # Add a blank row for spacing

    # Display LRU results
    tree.insert("", "end", values=["LRU Results"] + [""] * (frame_size + 5))  # Adjust header row for LRU
    for i, (frame_state, current_page, faults, hits, status) in enumerate(lru_table):
        hit_rate = hits / (hits + faults) if (hits + faults) > 0 else 0
        while len(frame_state) < frame_size:  # Ensure frame_state has frame_size length
            frame_state.append("-")  # Fill empty frames with "-"
        row_values = ["Step " + str(i + 1), current_page] + frame_state + [faults, hits, f"{hit_rate:.2%}", status]
        tree.insert("", "end", values=row_values, tags=("hit" if status == "Hit" else "fault",))

    tree.insert("", "end", values=[""] * (frame_size + 7))  # Add a blank row for spacing

    # Display Optimal results
    tree.insert("", "end", values=["Optimal Results"] + [""] * (frame_size + 5))  # Adjust header row for Optimal
    for i, (frame_state, current_page, faults, hits, status) in enumerate(optimal_table):
        hit_rate = hits / (hits + faults) if (hits + faults) > 0 else 0
        while len(frame_state) < frame_size:  # Ensure frame_state has frame_size length
            frame_state.append("-")  # Fill empty frames with "-"
        row_values = ["Step " + str(i + 1), current_page] + frame_state + [faults, hits, f"{hit_rate:.2%}", status]
        tree.insert("", "end", values=row_values, tags=("hit" if status == "Hit" else "fault",))

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
tree = ttk.Treeview(root, show="headings")
tree.pack(pady=10, expand=True, fill='both')

# Change colors and appearance of the table
tree.tag_configure('hit', background="#d4edda", foreground="green")  # Light green for Hits
tree.tag_configure('fault', background="#f8d7da", foreground="red")  # Light red for Faults

# Run the main window
root.mainloop()
