Here's the text for the README file without Markdown formatting:

# Page Replacement Visualizer

This project simulates different page replacement algorithms using a graphical user interface (GUI). It allows users to visualize the workings of FIFO, LRU, and Optimal page replacement algorithms.

## Features

- **Graphical Interface**: User-friendly interface for inputting reference strings and frame sizes.
- **Algorithm Simulation**: Implements FIFO, LRU, and Optimal page replacement algorithms.
- **Results Visualization**: Displays step-by-step changes in page frames, along with page faults and hits.
- **Dynamic Table**: Generates a table that updates based on the input frame size and reference string.
- **Hit Rate Calculation**: Shows hit rates for each algorithm, allowing for performance comparison.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Page-Replacement-Visualizer
   ```

2. Install the required packages:
   ```bash
   pip install matplotlib
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Enter a reference string in the input field (e.g., `7 0 1 2 0 3 0 4`).
3. Specify the frame size (e.g., `3`).
4. Click the "Run Simulation" button to see the results.

## Algorithms

- **FIFO (First In First Out)**: Replaces the oldest page in memory.
- **LRU (Least Recently Used)**: Replaces the page that has not been used for the longest time.
- **Optimal**: Replaces the page that will not be used for the longest time in the future.

## Contributions

Feel free to contribute by creating issues or pull requests.

## License

This project is licensed under the MIT License.