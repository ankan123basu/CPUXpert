import tkinter as tk
from tkinter import ttk
import random
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class TaskManagerWindow:
    def __init__(self, parent=None, scheduler=None):
        self.window = tk.Toplevel(parent)
        self.window.title("Process Performance Monitor")
        self.window.geometry("1000x800")
        
        self.scheduler = scheduler
        self.running = True
        self.start_time = time.time()
        self.current_algorithm = "FCFS"  # Default algorithm
        
        # Initialize data structures
        self.cpu_history = [0] * 60  # 60 seconds of history
        self.memory_history = [0] * 60
        self.disk_history = [0] * 60
        self.network_history = [0] * 60
        
        # Initialize scheduling metrics history
        self.tat_history = [0]
        self.wt_history = [0]
        self.rt_history = [0]
        self.time_points = [0]
        
        # Process-specific performance data
        self.process_data = {}
        
        # Create notebook
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.performance_tab = ttk.Frame(self.notebook)
        self.processes_tab = ttk.Frame(self.notebook)
        self.metrics_tab = ttk.Frame(self.notebook)
        self.queue_tab = ttk.Frame(self.notebook)
        self.visualization_3d_tab = ttk.Frame(self.notebook)
        self.timeline_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.performance_tab, text="Performance")
        self.notebook.add(self.processes_tab, text="Processes")
        self.notebook.add(self.metrics_tab, text="Scheduling Metrics")
        self.notebook.add(self.queue_tab, text="Process Queues")
        self.notebook.add(self.visualization_3d_tab, text="3D Visualization")
        self.notebook.add(self.timeline_tab, text="Timeline Analysis")
        
        # Initialize tabs
        self.setup_performance_tab()
        self.setup_processes_tab()
        self.setup_metrics_tab()
        self.setup_queue_tab()
        self.setup_3d_visualization_tab()
        self.setup_timeline_tab()
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.update_metrics)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        # Bind closing event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_performance_tab(self):
        # System metrics at the top
        metrics_frame = ttk.Frame(self.performance_tab)
        metrics_frame.pack(fill=tk.X, pady=10)
        
        self.cpu_var = tk.StringVar(value="CPU: 0%")
        self.memory_var = tk.StringVar(value="Memory: 0%")
        self.disk_var = tk.StringVar(value="Disk: 0 MB/s")
        self.network_var = tk.StringVar(value="Network: 0 Mbps")
        
        ttk.Label(metrics_frame, textvariable=self.cpu_var, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=20)
        ttk.Label(metrics_frame, textvariable=self.memory_var, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=20)
        ttk.Label(metrics_frame, textvariable=self.disk_var, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=20)
        ttk.Label(metrics_frame, textvariable=self.network_var, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=20)
        
        # Progress bars
        progress_frame = ttk.LabelFrame(self.performance_tab, text="System Resources")
        progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(progress_frame, text="CPU Usage:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.cpu_progress = ttk.Progressbar(progress_frame, length=300, mode='determinate')
        self.cpu_progress.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(progress_frame, text="Memory Usage:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.memory_progress = ttk.Progressbar(progress_frame, length=300, mode='determinate')
        self.memory_progress.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(progress_frame, text="Disk Usage:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.disk_progress = ttk.Progressbar(progress_frame, length=300, mode='determinate')
        self.disk_progress.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(progress_frame, text="Network Usage:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.network_progress = ttk.Progressbar(progress_frame, length=300, mode='determinate')
        self.network_progress.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Create graphs
        graphs_frame = ttk.Frame(self.performance_tab)
        graphs_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create a 2x2 grid of graphs
        self.perf_fig = Figure(figsize=(8, 6))
        
        # CPU Usage Graph
        self.cpu_ax = self.perf_fig.add_subplot(221)
        self.cpu_ax.set_title("CPU Usage")
        self.cpu_ax.set_ylim(0, 100)
        self.cpu_ax.set_xlabel("Time (s)")
        self.cpu_ax.set_ylabel("Usage (%)")
        self.cpu_line, = self.cpu_ax.plot(range(60), self.cpu_history, 'b-')
        self.cpu_ax.grid(True)
        
        # Memory Usage Graph
        self.memory_ax = self.perf_fig.add_subplot(222)
        self.memory_ax.set_title("Memory Usage")
        self.memory_ax.set_ylim(0, 100)
        self.memory_ax.set_xlabel("Time (s)")
        self.memory_ax.set_ylabel("Usage (%)")
        self.memory_line, = self.memory_ax.plot(range(60), self.memory_history, 'g-')
        self.memory_ax.grid(True)
        
        # Disk Usage Graph
        self.disk_ax = self.perf_fig.add_subplot(223)
        self.disk_ax.set_title("Disk I/O")
        self.disk_ax.set_ylim(0, 100)
        self.disk_ax.set_xlabel("Time (s)")
        self.disk_ax.set_ylabel("MB/s")
        self.disk_line, = self.disk_ax.plot(range(60), self.disk_history, 'r-')
        self.disk_ax.grid(True)
        
        # Network Usage Graph
        self.network_ax = self.perf_fig.add_subplot(224)
        self.network_ax.set_title("Network Usage")
        self.network_ax.set_ylim(0, 100)
        self.network_ax.set_xlabel("Time (s)")
        self.network_ax.set_ylabel("Mbps")
        self.network_line, = self.network_ax.plot(range(60), self.network_history, 'y-')
        self.network_ax.grid(True)
        
        self.perf_fig.tight_layout()
        
        # Add the figure to the tkinter window
        self.perf_canvas = FigureCanvasTkAgg(self.perf_fig, master=graphs_frame)
        self.perf_canvas.draw()
        self.perf_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def setup_processes_tab(self):
        # Create treeview for processes
        processes_frame = ttk.Frame(self.processes_tab)
        processes_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)
        
        columns = ('PID', 'Name', 'Status', 'CPU', 'Memory', 'Disk', 'Network')
        self.processes_tree = ttk.Treeview(processes_frame, columns=columns, show='headings', height=4)
        
        # Set column headings
        for col in columns:
            self.processes_tree.heading(col, text=col)
            self.processes_tree.column(col, width=100)
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(processes_frame, orient="vertical", command=self.processes_tree.yview)
        y_scrollbar.pack(side="right", fill="y")
        self.processes_tree.configure(yscrollcommand=y_scrollbar.set)
        
        self.processes_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add process-specific graphs
        graphs_frame = ttk.LabelFrame(self.processes_tab, text="Process Performance Graphs")
        graphs_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a 2x2 grid of graphs for individual process metrics
        self.process_fig = Figure(figsize=(8, 6))
        
        # Process CPU Usage Graph
        self.process_cpu_ax = self.process_fig.add_subplot(221)
        self.process_cpu_ax.set_title("Process CPU Usage")
        self.process_cpu_ax.set_ylim(0, 100)
        self.process_cpu_ax.set_xlabel("Time (s)")
        self.process_cpu_ax.set_ylabel("Usage (%)")
        self.process_cpu_lines = {}
        self.process_cpu_ax.grid(True)
        
        # Process Memory Usage Graph
        self.process_memory_ax = self.process_fig.add_subplot(222)
        self.process_memory_ax.set_title("Process Memory Usage")
        self.process_memory_ax.set_ylim(0, 500)
        self.process_memory_ax.set_xlabel("Time (s)")
        self.process_memory_ax.set_ylabel("MB")
        self.process_memory_lines = {}
        self.process_memory_ax.grid(True)
        
        # Process Disk Usage Graph
        self.process_disk_ax = self.process_fig.add_subplot(223)
        self.process_disk_ax.set_title("Process Disk I/O")
        self.process_disk_ax.set_ylim(0, 50)
        self.process_disk_ax.set_xlabel("Time (s)")
        self.process_disk_ax.set_ylabel("MB/s")
        self.process_disk_lines = {}
        self.process_disk_ax.grid(True)
        
        # Process Network Usage Graph
        self.process_network_ax = self.process_fig.add_subplot(224)
        self.process_network_ax.set_title("Process Network Usage")
        self.process_network_ax.set_ylim(0, 20)
        self.process_network_ax.set_xlabel("Time (s)")
        self.process_network_ax.set_ylabel("Mbps")
        self.process_network_lines = {}
        self.process_network_ax.grid(True)
        
        self.process_fig.tight_layout()
        
        # Add the figure to the tkinter window
        self.process_canvas = FigureCanvasTkAgg(self.process_fig, master=graphs_frame)
        self.process_canvas.draw()
        self.process_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def setup_metrics_tab(self):
        # Create frame for metrics graphs
        metrics_frame = ttk.Frame(self.metrics_tab)
        metrics_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create figure with subplots for each metric
        self.metrics_fig = Figure(figsize=(8, 6))
        
        # Create subplots for each metric
        self.tat_ax = self.metrics_fig.add_subplot(311)
        self.wt_ax = self.metrics_fig.add_subplot(312)
        self.rt_ax = self.metrics_fig.add_subplot(313)
        
        # Set up the plots
        self.tat_ax.set_title('Average Turnaround Time')
        self.wt_ax.set_title('Average Waiting Time')
        self.rt_ax.set_title('Average Response Time')
        
        # Create initial empty lines
        self.tat_line, = self.tat_ax.plot(self.time_points, self.tat_history, 'b-o', label='TAT')
        self.wt_line, = self.wt_ax.plot(self.time_points, self.wt_history, 'g-o', label='WT')
        self.rt_line, = self.rt_ax.plot(self.time_points, self.rt_history, 'r-o', label='RT')
        
        # Add legends
        self.tat_ax.legend()
        self.wt_ax.legend()
        self.rt_ax.legend()
        
        # Add grid
        self.tat_ax.grid(True)
        self.wt_ax.grid(True)
        self.rt_ax.grid(True)
        
        # Adjust layout
        self.metrics_fig.tight_layout()
        
        # Create canvas
        self.metrics_canvas = FigureCanvasTkAgg(self.metrics_fig, metrics_frame)
        self.metrics_canvas.draw()
        self.metrics_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def setup_queue_tab(self):
        # Create canvas for drawing queues
        self.queue_canvas = tk.Canvas(self.queue_tab, bg='white')
        self.queue_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create frame for queue labels
        self.queue_labels = ttk.LabelFrame(self.queue_tab, text="Queue Information")
        self.queue_labels.pack(fill=tk.X, padx=10, pady=5)
        
        # Labels for different queues
        self.ready_queue_label = ttk.Label(self.queue_labels, text="Ready Queue: 0 processes")
        self.ready_queue_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.running_label = ttk.Label(self.queue_labels, text="Running: 0 process")
        self.running_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.blocked_queue_label = ttk.Label(self.queue_labels, text="Blocked Queue: 0 processes")
        self.blocked_queue_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.completed_label = ttk.Label(self.queue_labels, text="Completed: 0 processes")
        self.completed_label.pack(anchor=tk.W, padx=5, pady=2)
        
    def setup_3d_visualization_tab(self):
        """Setup the 3D visualization tab"""
        # Create frame for 3D visualization
        visualization_frame = ttk.Frame(self.visualization_3d_tab)
        visualization_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create 3D figure
        self.fig_3d = plt.Figure(figsize=(8, 6), dpi=100)
        self.ax_3d = self.fig_3d.add_subplot(111, projection='3d')
        self.ax_3d.set_title("3D CPU Scheduling Visualization")
        
        # Set labels
        self.ax_3d.set_xlabel("Process ID")
        self.ax_3d.set_ylabel("Time")
        self.ax_3d.set_zlabel("CPU Usage")
        
        # Create canvas
        self.canvas_3d = FigureCanvasTkAgg(self.fig_3d, master=visualization_frame)
        self.canvas_3d.draw()
        self.canvas_3d.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize data structures for 3D visualization
        self.process_history = {}  # Store process execution history
        self.current_time = 0
        
    def setup_timeline_tab(self):
        """Setup the timeline analysis tab"""
        # Create main frame
        timeline_frame = ttk.Frame(self.timeline_tab)
        timeline_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create canvas for timeline visualization
        self.timeline_canvas = tk.Canvas(timeline_frame, bg='white', height=400)
        self.timeline_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Process colors and patterns
        self.process_colors = {
            'P1': '#FF6B6B',  # Coral Red
            'P2': '#4ECDC4',  # Turquoise
            'P3': '#45B7D1',  # Sky Blue
            'P4': '#96CEB4',  # Sage Green
            'P5': '#FFEEAD'   # Light Yellow
        }
        
        self.process_patterns = {
            'P1': '',         # Solid
            'P2': 'gray12',   # Dots
            'P3': 'gray25',   # Light stipple
            'P4': 'gray50',   # Medium stipple
            'P5': 'gray75'    # Heavy stipple
        }
        
        # Initialize timeline data
        self.timeline_data = {pid: [] for pid in range(1, 6)}  # For 5 processes
        self.prediction_data = {pid: [] for pid in range(1, 6)}
        
        # Add legend
        self.create_timeline_legend(timeline_frame)
        
        # Add metrics panel
        self.create_timeline_metrics(timeline_frame)
        
    def create_timeline_legend(self, parent):
        """Create legend for timeline visualization"""
        legend_frame = ttk.LabelFrame(parent, text="Process States")
        legend_frame.pack(fill=tk.X, padx=5, pady=5)
        
        states = [
            ("Running", "#32CD32"),
            ("Ready", "#FFD700"),
            ("Blocked", "#FF6347"),
            ("Predicted", "#A0A0A0")
        ]
        
        for i, (state, color) in enumerate(states):
            canvas = tk.Canvas(legend_frame, width=20, height=20, bg='white')
            canvas.grid(row=0, column=i*2, padx=5, pady=5)
            canvas.create_rectangle(2, 2, 18, 18, fill=color, outline='black')
            
            ttk.Label(legend_frame, text=state).grid(row=0, column=i*2+1, padx=5, pady=5)
            
    def create_timeline_metrics(self, parent):
        """Create metrics panel for timeline analysis"""
        metrics_frame = ttk.LabelFrame(parent, text="Timeline Metrics")
        metrics_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Process efficiency indicators
        self.efficiency_labels = {}
        for i in range(1, 6):
            pid = f"P{i}"
            frame = ttk.Frame(metrics_frame)
            frame.pack(side=tk.LEFT, padx=10)
            
            ttk.Label(frame, text=pid).pack()
            
            self.efficiency_labels[pid] = ttk.Label(frame, text="100%")
            self.efficiency_labels[pid].pack()
            
    def update_metrics(self):
        """Update all metrics in real-time"""
        counter = 0
        while self.running:
            try:
                # Update system metrics
                cpu = random.randint(0, 100)
                memory = random.randint(0, 100)
                disk = random.randint(0, 100)
                network = random.randint(0, 100)
                
                # Update history
                self.cpu_history.append(cpu)
                self.cpu_history = self.cpu_history[-60:]  # Keep last 60 seconds
                
                self.memory_history.append(memory)
                self.memory_history = self.memory_history[-60:]
                
                self.disk_history.append(disk)
                self.disk_history = self.disk_history[-60:]
                
                self.network_history.append(network)
                self.network_history = self.network_history[-60:]
                
                # Update system metrics display
                self.cpu_var.set(f"CPU: {cpu}%")
                self.memory_var.set(f"Memory: {memory}%")
                self.disk_var.set(f"Disk: {disk} MB/s")
                self.network_var.set(f"Network: {network} Mbps")
                
                # Update progress bars
                self.cpu_progress['value'] = cpu
                self.memory_progress['value'] = memory
                self.disk_progress['value'] = disk
                self.network_progress['value'] = network
                
                # Update graphs
                x = list(range(len(self.cpu_history)))
                
                self.cpu_line.set_data(x, self.cpu_history)
                self.memory_line.set_data(x, self.memory_history)
                self.disk_line.set_data(x, self.disk_history)
                self.network_line.set_data(x, self.network_history)
                
                # Adjust y-axis limits if needed
                self.cpu_ax.set_xlim(0, len(x) - 1)
                self.memory_ax.set_xlim(0, len(x) - 1)
                self.disk_ax.set_xlim(0, len(x) - 1)
                self.network_ax.set_xlim(0, len(x) - 1)
                
                # Redraw canvas
                self.perf_canvas.draw()
                
                # Update process list
                self.update_process_list()
                
                # Update scheduling metrics
                self.update_scheduling_metrics()
                
                # Update process queues
                self.update_process_queues()
                
                # Update 3D visualization
                self.update_3d_visualization()
                
                # Update timeline analysis
                self.update_timeline()
                
                counter += 1
                time.sleep(0.5)
            except tk.TclError:
                # Window was closed
                break
            except Exception as e:
                print(f"Error updating metrics: {e}")
                
    def update_process_list(self):
        # Clear existing items
        for item in self.processes_tree.get_children():
            self.processes_tree.delete(item)
        
        # Get processes from scheduler if available, otherwise use random data
        processes = []
        if self.scheduler and hasattr(self.scheduler, 'processes'):
            processes = self.scheduler.processes[:4]  # Limit to 4 processes
        
        # If no processes from scheduler, generate random ones
        if not processes:
            max_processes = 4
            for i in range(max_processes):
                pid = i
                name = f"Process {i}"
                status = "Running" if random.random() > 0.3 else "Completed"
                cpu = random.randint(0, 100)
                memory = random.randint(50, 300)
                disk = random.randint(0, 50)
                network = random.randint(0, 20)
                
                processes.append({
                    'pid': pid,
                    'name': name,
                    'status': status,
                    'cpu': cpu,
                    'memory': memory,
                    'disk': disk,
                    'network': network
                })
                
                # Store process data for graphs
                if pid not in self.process_data:
                    self.process_data[pid] = {
                        'cpu_history': [0] * 30,
                        'memory_history': [0] * 30,
                        'disk_history': [0] * 30,
                        'network_history': [0] * 30
                    }
                
                # Update process history
                self.process_data[pid]['cpu_history'].append(cpu)
                self.process_data[pid]['cpu_history'] = self.process_data[pid]['cpu_history'][-30:]
                
                self.process_data[pid]['memory_history'].append(memory)
                self.process_data[pid]['memory_history'] = self.process_data[pid]['memory_history'][-30:]
                
                self.process_data[pid]['disk_history'].append(disk)
                self.process_data[pid]['disk_history'] = self.process_data[pid]['disk_history'][-30:]
                
                self.process_data[pid]['network_history'].append(network)
                self.process_data[pid]['network_history'] = self.process_data[pid]['network_history'][-30:]
                
                # Store current values
                self.process_data[pid]['cpu'] = cpu
                self.process_data[pid]['memory'] = memory
                self.process_data[pid]['disk'] = disk
                self.process_data[pid]['network'] = network
                self.process_data[pid]['status'] = status
        
        # Add processes to treeview
        for i, process in enumerate(processes):
            if isinstance(process, dict):
                # For random data
                pid = process['pid']
                name = process['name']
                status = process['status']
                cpu = process['cpu']
                memory = process['memory']
                disk = process['disk']
                network = process['network']
            else:
                # For scheduler data
                pid = process.pid if hasattr(process, 'pid') else i
                name = process.name if hasattr(process, 'name') else f"Process {i}"
                status = process.status if hasattr(process, 'status') else "Running"
                cpu = random.randint(0, 100)  # Simulate CPU usage
                memory = random.randint(50, 300)  # Simulate memory usage
                disk = random.randint(0, 50)  # Simulate disk usage
                network = random.randint(0, 20)  # Simulate network usage
                
                # Store process data for graphs
                if pid not in self.process_data:
                    self.process_data[pid] = {
                        'cpu_history': [0] * 30,
                        'memory_history': [0] * 30,
                        'disk_history': [0] * 30,
                        'network_history': [0] * 30
                    }
                
                # Update process history
                self.process_data[pid]['cpu_history'].append(cpu)
                self.process_data[pid]['cpu_history'] = self.process_data[pid]['cpu_history'][-30:]
                
                self.process_data[pid]['memory_history'].append(memory)
                self.process_data[pid]['memory_history'] = self.process_data[pid]['memory_history'][-30:]
                
                self.process_data[pid]['disk_history'].append(disk)
                self.process_data[pid]['disk_history'] = self.process_data[pid]['disk_history'][-30:]
                
                self.process_data[pid]['network_history'].append(network)
                self.process_data[pid]['network_history'] = self.process_data[pid]['network_history'][-30:]
                
                # Store current values
                self.process_data[pid]['cpu'] = cpu
                self.process_data[pid]['memory'] = memory
                self.process_data[pid]['disk'] = disk
                self.process_data[pid]['network'] = network
                self.process_data[pid]['status'] = status
            
            self.processes_tree.insert('', 'end', values=(pid, name, status, f"{cpu}%", f"{memory} MB", f"{disk} MB/s", f"{network} Mbps"))
        
        # Update process graphs
        self.update_process_graphs()
    
    def update_process_graphs(self):
        """Update the process-specific performance graphs"""
        # Clear previous lines
        self.process_cpu_ax.clear()
        self.process_memory_ax.clear()
        self.process_disk_ax.clear()
        self.process_network_ax.clear()
        
        # Set titles and labels
        self.process_cpu_ax.set_title("Process CPU Usage")
        self.process_cpu_ax.set_ylim(0, 100)
        self.process_cpu_ax.set_xlabel("Time (s)")
        self.process_cpu_ax.set_ylabel("Usage (%)")
        self.process_cpu_ax.grid(True)
        
        self.process_memory_ax.set_title("Process Memory Usage")
        self.process_memory_ax.set_ylim(0, 500)
        self.process_memory_ax.set_xlabel("Time (s)")
        self.process_memory_ax.set_ylabel("MB")
        self.process_memory_ax.grid(True)
        
        self.process_disk_ax.set_title("Process Disk I/O")
        self.process_disk_ax.set_ylim(0, 100)
        self.process_disk_ax.set_xlabel("Time (s)")
        self.process_disk_ax.set_ylabel("MB/s")
        self.process_disk_ax.grid(True)
        
        self.process_network_ax.set_title("Process Network Usage")
        self.process_network_ax.set_ylim(0, 100)
        self.process_network_ax.set_xlabel("Time (s)")
        self.process_network_ax.set_ylabel("Mbps")
        self.process_network_ax.grid(True)
        
        # Plot process data
        colors = ['b', 'g', 'r', 'y']
        x = list(range(30))
        
        for i, (pid, data) in enumerate(self.process_data.items()):
            if i >= 4:  # Limit to 4 processes
                break
                
            color = colors[i % len(colors)]
            label = f"Process {pid}"
            
            # Plot CPU usage
            self.process_cpu_ax.plot(x, data['cpu_history'], color=color, label=label)
            
            # Plot Memory usage
            self.process_memory_ax.plot(x, data['memory_history'], color=color, label=label)
            
            # Plot Disk usage
            self.process_disk_ax.plot(x, data['disk_history'], color=color, label=label)
            
            # Plot Network usage
            self.process_network_ax.plot(x, data['network_history'], color=color, label=label)
        
        # Add legends
        self.process_cpu_ax.legend(loc='upper left', fontsize='small')
        self.process_memory_ax.legend(loc='upper left', fontsize='small')
        self.process_disk_ax.legend(loc='upper left', fontsize='small')
        self.process_network_ax.legend(loc='upper left', fontsize='small')
        
        # Update layout
        self.process_fig.tight_layout()
        
        # Redraw canvas
        self.process_canvas.draw()
    
    def update_scheduling_metrics(self):
        """Update scheduling metrics graphs"""
        try:
            if self.scheduler:
                metrics = self.scheduler.get_metrics()
                tat = metrics.get('avg_turnaround', 0)
                wt = metrics.get('avg_waiting', 0)
                rt = metrics.get('avg_response', 0)
            else:
                # Simulate metrics if scheduler not available
                tat = random.uniform(1.0, 10.0)
                wt = random.uniform(0.5, 5.0)
                rt = random.uniform(0.1, 3.0)
            
            # Add new time point
            new_time = len(self.time_points)
            self.time_points.append(new_time)
            
            # Add new metrics
            self.tat_history.append(tat)
            self.wt_history.append(wt)
            self.rt_history.append(rt)
            
            # Limit data points to prevent memory issues
            max_points = 20
            if len(self.time_points) > max_points:
                self.time_points = self.time_points[-max_points:]
                self.tat_history = self.tat_history[-max_points:]
                self.wt_history = self.wt_history[-max_points:]
                self.rt_history = self.rt_history[-max_points:]
            
            # Update plot data
            self.tat_line.set_data(self.time_points, self.tat_history)
            self.wt_line.set_data(self.time_points, self.wt_history)
            self.rt_line.set_data(self.time_points, self.rt_history)
            
            # Adjust axes limits
            for ax in [self.tat_ax, self.wt_ax, self.rt_ax]:
                ax.relim()
                ax.autoscale_view()
            
            # Redraw canvas
            self.metrics_fig.tight_layout()
            self.metrics_canvas.draw_idle()
            
        except Exception as e:
            print(f"Error updating scheduling metrics: {e}")
            
    def update_process_queues(self):
        """Update process queues visualization"""
        try:
            # Clear canvas
            self.queue_canvas.delete('all')
            
            # Get processes from scheduler or simulate if not available
            if self.scheduler and hasattr(self.scheduler, 'processes'):
                processes = self.scheduler.processes
            else:
                # Simulate processes
                processes = []
                for i in range(10):
                    state = random.choice(['ready', 'running', 'blocked', 'completed'])
                    processes.append({'pid': i, 'state': state})
            
            # Calculate positions
            canvas_width = self.queue_canvas.winfo_width()
            canvas_height = self.queue_canvas.winfo_height()
            
            if canvas_width < 50 or canvas_height < 50:  # Canvas not ready yet
                return
                
            # Define queue positions
            ready_y = canvas_height * 0.2
            running_y = canvas_height * 0.4
            blocked_y = canvas_height * 0.6
            completed_y = canvas_height * 0.8
            
            # Group processes by state
            ready_processes = [p for p in processes if getattr(p, 'state', '') == 'ready']
            running_processes = [p for p in processes if getattr(p, 'state', '') == 'running']
            blocked_processes = [p for p in processes if getattr(p, 'state', '') == 'blocked']
            completed_processes = [p for p in processes if getattr(p, 'state', '') == 'completed']
            
            # If using simulated data
            if not ready_processes and not running_processes and not blocked_processes and not completed_processes:
                # Randomly assign processes to queues
                num_ready = random.randint(1, 3)
                num_running = random.randint(0, 1)
                num_blocked = random.randint(0, 2)
                num_completed = random.randint(1, 4)
                
                ready_processes = [{'pid': i, 'remaining': random.randint(1, 10)} for i in range(num_ready)]
                running_processes = [{'pid': num_ready, 'remaining': random.randint(1, 10)}] if num_running else []
                blocked_processes = [{'pid': num_ready + 1 + i, 'remaining': random.randint(1, 10)} for i in range(num_blocked)]
                completed_processes = [{'pid': num_ready + num_blocked + 1 + i, 'remaining': 0} for i in range(num_completed)]
            
            # Draw queue headers
            self.queue_canvas.create_text(50, ready_y - 30, text="Ready Queue", font=("Arial", 12, "bold"), anchor=tk.W)
            self.queue_canvas.create_text(50, running_y - 30, text="Running", font=("Arial", 12, "bold"), anchor=tk.W)
            self.queue_canvas.create_text(50, blocked_y - 30, text="Blocked Queue", font=("Arial", 12, "bold"), anchor=tk.W)
            self.queue_canvas.create_text(50, completed_y - 30, text="Completed", font=("Arial", 12, "bold"), anchor=tk.W)
            
            # Draw ready queue
            x = 50
            for process in ready_processes:
                self.draw_process_box(x, ready_y, process, 'ready')
                x += 100
                
            # Draw running process
            x = 50
            for process in running_processes:
                self.draw_process_box(x, running_y, process, 'running')
                x += 100
                
            # Draw blocked queue
            x = 50
            for process in blocked_processes:
                self.draw_process_box(x, blocked_y, process, 'blocked')
                x += 100
                
            # Draw completed processes
            x = 50
            for process in completed_processes:
                self.draw_process_box(x, completed_y, process, 'completed')
                x += 100
                
            # Update queue labels
            self.ready_queue_label['text'] = f"Ready Queue: {len(ready_processes)} processes"
            self.running_label['text'] = f"Running: {len(running_processes)} processes"
            self.blocked_queue_label['text'] = f"Blocked Queue: {len(blocked_processes)} processes"
            self.completed_label['text'] = f"Completed: {len(completed_processes)} processes"
            
        except Exception as e:
            print(f"Error updating process queues: {e}")
            
    def draw_process_box(self, x, y, process, state):
        """Draw a box representing a process"""
        # Box dimensions
        width = 80
        height = 40
        
        # Colors for different states
        colors = {
            'ready': '#3498db',     # Blue
            'running': '#2ecc71',   # Green
            'blocked': '#e74c3c',   # Red
            'completed': '#95a5a6'  # Gray
        }
        
        # Get process ID and remaining time
        if isinstance(process, dict):
            pid = process.get('pid', '?')
            remaining = process.get('remaining', '?')
        else:
            pid = getattr(process, 'pid', '?')
            remaining = getattr(process, 'remaining_time', '?')
        
        # Draw box
        self.queue_canvas.create_rectangle(
            x, y - height/2,
            x + width, y + height/2,
            fill=colors[state],
            outline='black'
        )
        
        # Draw process ID and remaining time
        self.queue_canvas.create_text(
            x + width/2, y - 5,
            text=f"P{pid}",
            font=('Arial', 10, 'bold'),
            fill='white'
        )
        
        self.queue_canvas.create_text(
            x + width/2, y + 10,
            text=f"Time: {remaining}",
            font=('Arial', 8),
            fill='white'
        )
            
    def update_3d_visualization(self):
        """Update the 3D visualization with real-time data"""
        try:
            self.ax_3d.clear()
            
            # Update process history
            for pid, data in self.process_data.items():
                if pid not in self.process_history:
                    self.process_history[pid] = {'times': [], 'cpu_usage': [], 'process_id': []}
                
                self.process_history[pid]['times'].append(self.current_time)
                self.process_history[pid]['cpu_usage'].append(data.get('cpu', 0))
                
                # Extract numeric part from process ID (handle both string and int)
                if isinstance(pid, str) and pid.startswith('P'):
                    process_id = float(pid[1:])  # Remove 'P' prefix and convert to float
                else:
                    process_id = float(pid)  # Just convert to float if it's already numeric
                
                self.process_history[pid]['process_id'].append(process_id)
                
                # Keep only last 30 data points for performance
                if len(self.process_history[pid]['times']) > 30:
                    self.process_history[pid]['times'] = self.process_history[pid]['times'][-30:]
                    self.process_history[pid]['cpu_usage'] = self.process_history[pid]['cpu_usage'][-30:]
                    self.process_history[pid]['process_id'] = self.process_history[pid]['process_id'][-30:]
            
            # Plot 3D lines for each process
            colors = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow']
            for i, (pid, history) in enumerate(self.process_history.items()):
                if not history['times']:  # Skip if no data
                    continue
                    
                color = colors[i % len(colors)]
                
                # Get process ID for label
                if isinstance(pid, str) and pid.startswith('P'):
                    label_id = pid
                else:
                    label_id = f"P{pid}"
                
                self.ax_3d.plot3D(
                    history['process_id'],
                    history['times'],
                    history['cpu_usage'],
                    color=color,
                    label=label_id,
                    marker='o'
                )
            
            # Set labels and title
            self.ax_3d.set_xlabel("Process ID")
            self.ax_3d.set_ylabel("Time")
            self.ax_3d.set_zlabel("CPU Usage")
            self.ax_3d.set_title("3D CPU Scheduling Visualization")
            
            # Add legend
            self.ax_3d.legend()
            
            # Set axis limits
            self.ax_3d.set_xlim(0, 5)
            self.ax_3d.set_ylim(0, 30)
            self.ax_3d.set_zlim(0, 100)
            
            # Add grid
            self.ax_3d.grid(True)
            
            # Update canvas
            self.canvas_3d.draw()
            
            # Increment time
            self.current_time += 1
            
        except Exception as e:
            print(f"Error updating 3D visualization: {e}")
            
    def update_timeline(self):
        """Update the timeline visualization"""
        try:
            self.timeline_canvas.delete("all")
            
            # Canvas dimensions
            width = self.timeline_canvas.winfo_width()
            height = self.timeline_canvas.winfo_height()
            
            # Timeline parameters
            timeline_start = 50
            timeline_end = width - 50
            row_height = 50
            row_spacing = 20
            
            # Draw time axis
            self.timeline_canvas.create_line(
                timeline_start, height - 30,
                timeline_end, height - 30,
                width=2, arrow=tk.LAST
            )
            
            # Draw current time marker
            time_x = timeline_start + (self.current_time % 30) * ((timeline_end - timeline_start) / 30)
            self.timeline_canvas.create_line(
                time_x, 20, time_x, height - 40,
                fill='red', width=2, dash=(4, 4)
            )
            self.timeline_canvas.create_text(
                time_x, height - 15,
                text=f"Time: {self.current_time}s",
                fill='red'
            )
            
            # Draw process timelines
            for i, (pid, data) in enumerate(self.process_data.items()):
                if i >= 5:  # Limit to 5 processes
                    break
                    
                y = 30 + i * (row_height + row_spacing)
                
                # Draw process label
                self.timeline_canvas.create_text(
                    30, y + row_height/2,
                    text=pid, anchor='e'
                )
                
                # Draw timeline base
                self.timeline_canvas.create_rectangle(
                    timeline_start, y,
                    timeline_end, y + row_height,
                    fill='#f0f0f0', outline='gray'
                )
                
                # Draw process states
                cpu_usage = data.get('cpu', 0)
                state_width = (timeline_end - timeline_start) / 30
                
                # Current state
                state_x = timeline_start + (self.current_time % 30) * state_width
                state_color = '#32CD32' if cpu_usage > 50 else '#FFD700'
                
                self.timeline_canvas.create_rectangle(
                    state_x, y,
                    state_x + state_width, y + row_height,
                    fill=state_color,
                    outline='black'
                )
                
                # Predicted states (next 5 time units)
                for t in range(1, 6):
                    pred_x = state_x + t * state_width
                    if pred_x < timeline_end:
                        # Predict future CPU usage based on current trend
                        pred_usage = min(100, max(0, cpu_usage + random.randint(-20, 20)))
                        pred_color = '#32CD32' if pred_usage > 50 else '#FFD700'
                        
                        self.timeline_canvas.create_rectangle(
                            pred_x, y,
                            pred_x + state_width, y + row_height,
                            fill=pred_color,
                            outline='black',
                            stipple='gray50'  # Make predicted states semi-transparent
                        )
                
                # Update efficiency metric
                if pid in self.efficiency_labels:
                    efficiency = (cpu_usage / 100) * 100
                    self.efficiency_labels[pid].config(
                        text=f"{efficiency:.1f}%",
                        foreground='green' if efficiency > 70 else 'red'
                    )
            
        except Exception as e:
            print(f"Error updating timeline: {e}")
            
    def set_current_algorithm(self, algorithm):
        """Set the current algorithm being used"""
        self.current_algorithm = algorithm

    def on_closing(self):
        """Handle window closing"""
        self.running = False
        self.window.destroy()
        
    def show(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = TaskManagerWindow()
    app.show()
