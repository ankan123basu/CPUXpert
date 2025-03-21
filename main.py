import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scheduler import Process, Scheduler
import time
from task_manager import TaskManagerWindow

class CPUSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1200x800")
        
        # Initialize variables
        self.processes = []
        self.process_counter = 1
        self.scheduler = None
        self.selected_algorithm = "FCFS"
        
        # Initialize metrics variables
        self.avg_turnaround_var = tk.StringVar(value="0.0")
        self.avg_waiting_var = tk.StringVar(value="0.0")
        self.avg_response_var = tk.StringVar(value="0.0")
        self.cpu_util_var = tk.StringVar(value="0.0%")
        
        # Create main frames
        self.left_frame = ttk.Frame(self.root)
        self.left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.right_frame = ttk.Frame(self.root)
        self.right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        # Configure grid weights
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)  # Make the process list row expandable
        
        # Initialize scheduler
        self.scheduler = Scheduler()
        
        # Set default algorithm
        self.selected_algorithm = 'FCFS'
        
        # Initialize process list and counter
        self.processes = []
        self.process_counter = 1
        
        # Create sections
        self.create_input_section()
        self.create_algorithm_selection()
        self.create_control_section()
        self.create_visualization_section()
        self.create_task_manager_section()
        
        # Initial UI setup
        self.on_algorithm_change(None)
        
    def create_input_section(self):
        """Create the process input section"""
        # Create frame for process input
        input_frame = ttk.LabelFrame(self.left_frame, text="Process Input")
        input_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Process ID
        ttk.Label(input_frame, text="Process ID:").grid(row=0, column=0, padx=5, pady=5)
        self.pid_var = tk.StringVar(value=f"P{self.process_counter}")
        self.pid_entry = ttk.Entry(input_frame, textvariable=self.pid_var, state="readonly")
        self.pid_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Arrival Time
        ttk.Label(input_frame, text="Arrival Time:").grid(row=1, column=0, padx=5, pady=5)
        self.arrival_var = tk.StringVar(value="0")
        self.arrival_entry = ttk.Entry(input_frame, textvariable=self.arrival_var)
        self.arrival_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Burst Time
        ttk.Label(input_frame, text="Burst Time:").grid(row=2, column=0, padx=5, pady=5)
        self.burst_var = tk.StringVar(value="1")
        self.burst_entry = ttk.Entry(input_frame, textvariable=self.burst_var)
        self.burst_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Priority
        self.priority_label = ttk.Label(input_frame, text="Priority:")
        self.priority_label.grid(row=3, column=0, padx=5, pady=5)
        self.priority_var = tk.StringVar(value="1")
        self.priority_entry = ttk.Entry(input_frame, textvariable=self.priority_var)
        self.priority_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Priority note
        self.priority_note = ttk.Label(input_frame, text="(Higher value = Higher priority)", foreground="blue")
        self.priority_note.grid(row=3, column=2, padx=5, pady=5)
        
        # Initially hide priority input
        self.priority_label.grid_remove()
        self.priority_entry.grid_remove()
        self.priority_note.grid_remove()
        
        # Add Process button
        self.add_btn = ttk.Button(input_frame, text="Add Process", command=self.add_process)
        self.add_btn.grid(row=4, column=0, columnspan=3, pady=10)
        
        # Process List
        self.process_tree = ttk.Treeview(self.left_frame, columns=("PID", "Arrival", "Burst", "Priority"), show="headings", height=10)
        self.process_tree.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure headers
        for col in ("PID", "Arrival", "Burst", "Priority"):
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=70)
            
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.left_frame, orient="vertical", command=self.process_tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.process_tree.configure(yscrollcommand=scrollbar.set)
        
        # Delete process button
        self.delete_btn = ttk.Button(self.left_frame, text="Delete Selected Process", command=self.delete_process)
        self.delete_btn.grid(row=2, column=0, pady=5)
            
    def create_algorithm_selection(self):
        """Create the algorithm selection section"""
        # Algorithm selection section
        algorithm_frame = ttk.LabelFrame(self.left_frame, text="Algorithm Selection")
        algorithm_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        
        # Algorithm selection
        ttk.Label(algorithm_frame, text="Algorithm:").grid(row=0, column=0, padx=5, pady=5)
        self.algorithm_var = tk.StringVar(value="FCFS")
        self.algorithm_combo = ttk.Combobox(algorithm_frame, textvariable=self.algorithm_var)
        self.algorithm_combo['values'] = ("FCFS", "SJF", "SJF Preemptive", "Priority", "Priority Preemptive", "Round Robin")
        self.algorithm_combo.grid(row=0, column=1, padx=5, pady=5)
        self.algorithm_combo.bind("<<ComboboxSelected>>", self.on_algorithm_change)
        
        # Suggest Algorithm button
        self.suggest_btn = ttk.Button(algorithm_frame, text="Suggest Algorithm", command=self.suggest_algorithm)
        self.suggest_btn.grid(row=2, column=0, columnspan=2, pady=5)
        
    def create_control_section(self):
        # Create frame for controls
        control_frame = ttk.LabelFrame(self.left_frame, text="Controls")
        control_frame.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        
        # Time Quantum for RR
        ttk.Label(control_frame, text="Time Quantum:").grid(row=1, column=0, padx=5, pady=5)
        self.time_quantum_var = tk.StringVar(value="2")
        self.time_quantum_entry = ttk.Entry(control_frame, textvariable=self.time_quantum_var)
        self.time_quantum_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Control Buttons
        self.start_btn = ttk.Button(control_frame, text="Start Simulation", command=self.start_simulation)
        self.start_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.reset_btn = ttk.Button(control_frame, text="Reset", command=self.reset_simulation)
        self.reset_btn.grid(row=3, column=0, columnspan=2, pady=5)
        
    def on_algorithm_change(self, event=None):
        """Handle algorithm selection change"""
        self.selected_algorithm = self.algorithm_var.get()
        
        # Enable/disable time quantum based on algorithm
        if self.selected_algorithm == 'Round Robin':
            self.time_quantum_entry.config(state='normal')
        else:
            self.time_quantum_entry.config(state='disabled')
            
        # Show/hide priority input based on algorithm
        if "Priority" in self.selected_algorithm:
            self.priority_label.grid()
            self.priority_entry.grid()
            self.priority_note.grid()
        else:
            self.priority_label.grid_remove()
            self.priority_entry.grid_remove()
            self.priority_note.grid_remove()
            
        # Update the visualization if we have a schedule
        if hasattr(self, 'scheduler') and self.scheduler.schedule:
            self.update_visualization(self.scheduler.schedule)
            
    def create_visualization_section(self):
        """Create the visualization section"""
        # Create frame for visualization
        self.visualization_frame = ttk.Frame(self.right_frame)
        self.visualization_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create Gantt chart
        self.gantt_frame = ttk.LabelFrame(self.visualization_frame, text="Gantt Chart")
        self.gantt_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Increase the size of the Gantt chart
        self.gantt_fig = plt.Figure(figsize=(8, 4))
        self.gantt_ax = self.gantt_fig.add_subplot(111)
        self.gantt_canvas = FigureCanvasTkAgg(self.gantt_fig, master=self.gantt_frame)
        self.gantt_canvas.draw()
        self.gantt_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Create metrics visualization
        self.metrics_frame = ttk.LabelFrame(self.visualization_frame, text="Scheduling Metrics")
        self.metrics_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Increase the size of the metrics chart
        self.metrics_fig = plt.Figure(figsize=(8, 3))
        self.metrics_ax = self.metrics_fig.add_subplot(111)
        self.metrics_canvas = FigureCanvasTkAgg(self.metrics_fig, master=self.metrics_frame)
        self.metrics_canvas.draw()
        self.metrics_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Create performance metrics section
        self.performance_frame = ttk.LabelFrame(self.visualization_frame, text="Performance Metrics")
        self.performance_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # CPU Utilization
        self.cpu_utilization_var = tk.StringVar(value="CPU Utilization: 0.0%")
        self.cpu_utilization_label = ttk.Label(self.performance_frame, textvariable=self.cpu_utilization_var)
        self.cpu_utilization_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Throughput
        self.throughput_var = tk.StringVar(value="Throughput: 0.0 processes/unit time")
        self.throughput_label = ttk.Label(self.performance_frame, textvariable=self.throughput_var)
        self.throughput_label.pack(anchor=tk.W, padx=5, pady=2)
        
    def create_task_manager_section(self):
        # Task Manager section
        self.task_manager_frame = ttk.Frame(self.left_frame)
        self.task_manager_frame.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
        
        # Open Task Manager button
        self.open_task_manager_btn = ttk.Button(self.task_manager_frame, text="Open Performance Monitor", command=self.open_task_manager)
        self.open_task_manager_btn.pack(pady=5)
        
        # Task Manager section
        self.task_frame = ttk.LabelFrame(self.right_frame, text="Process Details", padding="10")
        self.task_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Process details table
        columns = ("PID", "State", "Arrival", "Burst", "Remaining", "Priority", "Start", "Completion", "TAT", "WT")
        self.task_tree = ttk.Treeview(self.task_frame, columns=columns, show="headings")
        
        # Configure headers
        for col in columns:
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=70)
            
        self.task_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(self.task_tree, orient="vertical", command=self.task_tree.yview)
        y_scrollbar.pack(side="right", fill="y")
        self.task_tree.configure(yscrollcommand=y_scrollbar.set)
        
        # Process state visualization
        self.state_frame = ttk.LabelFrame(self.task_frame, text="Process State Visualization", padding="10")
        self.state_frame.pack(fill=tk.X, pady=10)
        
        # Create a canvas for state visualization
        self.state_canvas = tk.Canvas(self.state_frame, height=100, bg="white")
        self.state_canvas.pack(fill=tk.X, expand=True)
        
    def add_process(self):
        """Add a process to the list"""
        try:
            pid = self.pid_var.get()
            arrival_time = int(self.arrival_var.get())
            burst_time = int(self.burst_var.get())
            priority = int(self.priority_var.get()) if "Priority" in self.selected_algorithm else 0
            
            # Validate inputs
            if burst_time <= 0:
                messagebox.showerror("Error", "Burst time must be greater than 0")
                return
                
            if arrival_time < 0:
                messagebox.showerror("Error", "Arrival time cannot be negative")
                return
                
            if "Priority" in self.selected_algorithm and priority < 1:
                messagebox.showerror("Error", "Priority must be greater than 0")
                return
            
            # Create process object
            process = Process(
                pid=pid,
                arrival_time=arrival_time,
                burst_time=burst_time,
                priority=priority
            )
            
            # Add to process list
            self.processes.append(process)
            
            # Update process table
            self.process_tree.insert('', 'end', values=(
                pid,
                arrival_time,
                burst_time,
                priority if "Priority" in self.selected_algorithm else "-"
            ))
            
            # Increment counter and update PID
            self.process_counter += 1
            self.pid_var.set(f"P{self.process_counter}")
            
            # Clear other inputs
            self.arrival_var.set("0")
            self.burst_var.set("1")
            self.priority_var.set("1")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")
            
    def delete_process(self):
        selected_item = self.process_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a process to delete")
            return
            
        # Get process ID
        pid = self.process_tree.item(selected_item[0], "values")[0]
        
        # Remove from process list
        self.processes = [p for p in self.processes if p.pid != pid]
        
        # Remove from treeview
        self.process_tree.delete(selected_item[0])
            
    def start_simulation(self):
        """Start the CPU scheduling simulation"""
        if not self.processes:
            messagebox.showerror("Error", "Please add at least one process before starting the simulation.")
            return
            
        # Get selected algorithm
        algorithm = self.selected_algorithm
        
        # Get time quantum for Round Robin
        time_quantum = None
        if algorithm == 'Round Robin':
            try:
                time_quantum = int(self.time_quantum_var.get())
                if time_quantum <= 0:
                    messagebox.showerror("Error", "Time quantum must be a positive integer.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Time quantum must be a valid integer.")
                return
                
        # Run the scheduling algorithm
        try:
            # Create a copy of processes to avoid modifying the original list
            process_copies = [Process(p.pid, p.arrival_time, p.burst_time, p.priority) for p in self.processes]
            
            # Set up the scheduler with the copied processes
            self.scheduler.processes = process_copies
            
            # Run the appropriate scheduling algorithm
            if algorithm == 'FCFS':
                schedule = self.scheduler.fcfs()
            elif algorithm == 'SJF':
                schedule = self.scheduler.sjf()
            elif algorithm == 'SJF Preemptive':
                schedule = self.scheduler.sjf_preemptive()
            elif algorithm == 'Round Robin':
                schedule = self.scheduler.round_robin(time_quantum)
            elif algorithm == 'Priority':
                schedule = self.scheduler.priority()
            elif algorithm == 'Priority Preemptive':
                schedule = self.scheduler.priority_preemptive()
            else:
                messagebox.showerror("Error", "Invalid algorithm selected.")
                return
                
            # Update the visualization with the schedule
            self.update_visualization(schedule)
            
            # Update the task manager with process states
            self.update_task_manager()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during simulation: {str(e)}")
            
    def update_visualization(self, schedule):
        # Clear previous plots
        self.gantt_ax.clear()
        self.metrics_ax.clear()
        
        # Set title
        self.gantt_ax.set_title(f"Gantt Chart - {self.selected_algorithm}")
        
        # Draw Gantt chart
        self.draw_gantt_chart(schedule)
        
        # Draw metrics
        self.draw_metrics()
        
        # Refresh canvas
        self.gantt_canvas.draw()
        
        # Update metrics text
        self.update_metrics()
        
    def draw_gantt_chart(self, schedule):
        # Sort processes by start time for consistent coloring
        processes = sorted(self.processes, key=lambda p: p.arrival_time)
        
        # Create color map
        colors = plt.cm.get_cmap('tab10', len(processes))
        process_colors = {p.pid: colors(i) for i, p in enumerate(processes)}
        
        # Draw each process execution
        for slot in schedule:
            process = slot['process']
            start = slot['start']
            end = slot['end']
            
            self.gantt_ax.barh(
                y=0, 
                width=end-start, 
                left=start, 
                height=0.5, 
                color=process_colors[process.pid],
                edgecolor='black'
            )
            
            # Add process ID text
            self.gantt_ax.text(
                x=start + (end-start)/2,
                y=0,
                s=process.pid,
                ha='center',
                va='center',
                color='black',
                fontweight='bold'
            )
            
        # Set y-axis
        self.gantt_ax.set_yticks([])
        
        # Set x-axis
        max_time = max(slot['end'] for slot in schedule)
        self.gantt_ax.set_xlim(0, max_time)
        self.gantt_ax.set_xlabel("Time")
        
        # Add grid
        self.gantt_ax.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Add legend
        handles = [plt.Rectangle((0,0),1,1, color=process_colors[p.pid]) for p in processes]
        self.gantt_ax.legend(handles, [p.pid for p in processes], loc='upper right')
        
    def draw_metrics(self):
        """Draw performance metrics"""
        try:
            metrics = self.scheduler.get_metrics()
            
            # Clear previous metrics
            for widget in self.metrics_frame.winfo_children():
                widget.destroy()
                
            # Create a figure for metrics
            fig, ax = plt.subplots(figsize=(5, 3))
            
            # Metrics to display
            labels = ['Avg Turnaround', 'Avg Waiting', 'Avg Response']
            values = [
                metrics.get('avg_turnaround', 0),
                metrics.get('avg_waiting', 0),
                metrics.get('avg_response', 0)
            ]
            
            # Create bar chart
            bars = ax.bar(labels, values, color=['#3498db', '#2ecc71', '#e74c3c'])
            
            # Add values on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{height:.2f}', ha='center', va='bottom')
                        
            # Set title and labels
            ax.set_title('Performance Metrics')
            ax.set_ylabel('Time Units')
            
            # Add CPU utilization
            cpu_utilization = metrics.get('cpu_utilization', 0)
            ttk.Label(
                self.metrics_frame, 
                text=f"CPU Utilization: {cpu_utilization:.2f}%",
                font=("Arial", 10, "bold")
            ).pack(anchor=tk.W, pady=5)
            
            # Add the figure to the tkinter window
            canvas = FigureCanvasTkAgg(fig, master=self.metrics_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Update the second graph with real-time metrics
            self.update_metrics_graph()
            
        except Exception as e:
            print(f"Error drawing metrics: {str(e)}")
            
    def update_metrics_graph(self):
        """Update the second graph with real-time metrics"""
        # Get metrics
        metrics = self.scheduler.get_metrics()
        
        # Clear previous plot
        self.metrics_ax.clear()
        
        # Metrics data
        metrics_data = {
            'AWT': metrics.get('avg_waiting', 0),
            'ATAT': metrics.get('avg_turnaround', 0),
            'ART': metrics.get('avg_response', 0)
        }
        
        # Create line plot for metrics
        x = list(range(len(metrics_data)))
        values = list(metrics_data.values())
        
        # Create bar chart
        bars = self.metrics_ax.bar(
            x, 
            values, 
            color=['#2ecc71', '#3498db', '#e74c3c'],
            width=0.6
        )
        
        # Add labels on top of bars
        for bar in bars:
            height = bar.get_height()
            self.metrics_ax.text(
                bar.get_x() + bar.get_width()/2., 
                height + 0.1,
                f'{height:.2f}', 
                ha='center', 
                va='bottom',
                fontsize=9
            )
        
        # Set labels and title
        self.metrics_ax.set_title('Scheduling Metrics')
        self.metrics_ax.set_xticks(x)
        self.metrics_ax.set_xticklabels(list(metrics_data.keys()))
        self.metrics_ax.set_ylabel('Time Units')
        
        # Add grid
        self.metrics_ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Refresh canvas
        self.gantt_canvas.draw()
        
    def update_metrics(self):
        metrics = self.scheduler.get_metrics()
        
        # Update metrics display
        self.avg_turnaround_var.set(f"{metrics.get('avg_turnaround', 0):.2f}")
        self.avg_waiting_var.set(f"{metrics.get('avg_waiting', 0):.2f}")
        self.avg_response_var.set(f"{metrics.get('avg_response', 0):.2f}")
        
        # Calculate CPU utilization
        if self.scheduler.schedule:
            total_time = max(slot['end'] for slot in self.scheduler.schedule)
            total_burst = sum(p.burst_time for p in self.processes)
            utilization = (total_burst / total_time) * 100 if total_time > 0 else 0
            self.cpu_util_var.set(f"{utilization:.2f}%")
        
    def update_task_manager(self):
        # Clear previous entries
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
            
        # Add process details
        for process in self.processes:
            # Calculate metrics for each process
            if process.completion_time is not None:
                tat = process.completion_time - process.arrival_time
                wt = tat - process.burst_time
                state = "Completed"
                remaining = 0
            else:
                tat = "-"
                wt = "-"
                state = "Waiting"
                remaining = process.remaining_time
                
            # Add to treeview
            self.task_tree.insert("", "end", values=(
                process.pid, 
                state,
                process.arrival_time,
                process.burst_time,
                remaining,
                process.priority,
                process.start_time if process.start_time is not None else "-",
                process.completion_time if process.completion_time is not None else "-",
                tat,
                wt
            ))
        
        # Update state visualization
        self.update_state_visualization()
        
    def update_state_visualization(self):
        """Visualize the state of each process"""
        self.state_canvas.delete("all")
        
        if not self.processes:
            return
            
        # Define colors for different states
        colors = {
            "Waiting": "#FFC107",  # Amber
            "Running": "#4CAF50",  # Green
            "Completed": "#2196F3"  # Blue
        }
        
        # Calculate canvas dimensions
        canvas_width = self.state_canvas.winfo_width()
        canvas_height = self.state_canvas.winfo_height()
        
        # Calculate box dimensions
        num_processes = len(self.processes)
        box_width = min(100, (canvas_width - 20) / num_processes)
        box_height = canvas_height - 40
        
        # Draw process boxes
        for i, process in enumerate(self.processes):
            # Determine process state
            if process.completion_time is not None:
                state = "Completed"
            elif process.start_time is not None and process.remaining_time > 0:
                state = "Running"
            else:
                state = "Waiting"
                
            # Calculate position
            x = 10 + i * (box_width + 10)
            y = 10
            
            # Draw box
            self.state_canvas.create_rectangle(
                x, y, x + box_width, y + box_height,
                fill=colors[state],
                outline="black"
            )
            
            # Draw process ID
            self.state_canvas.create_text(
                x + box_width/2, y + 15,
                text=process.pid,
                fill="black",
                font=("Arial", 10, "bold")
            )
            
            # Draw state
            self.state_canvas.create_text(
                x + box_width/2, y + box_height/2,
                text=state,
                fill="black",
                font=("Arial", 8)
            )
            
            # Draw progress if running
            if state == "Running" and process.burst_time > 0:
                progress = (process.burst_time - process.remaining_time) / process.burst_time
                progress_height = progress * (box_height - 30)
                
                self.state_canvas.create_rectangle(
                    x + 5, y + box_height - 5 - progress_height,
                    x + box_width - 5, y + box_height - 5,
                    fill="#81C784",
                    outline=""
                )
                
                # Draw progress percentage
                self.state_canvas.create_text(
                    x + box_width/2, y + box_height - 15,
                    text=f"{int(progress * 100)}%",
                    fill="black",
                    font=("Arial", 8)
                )
        
    def reset_simulation(self):
        self.processes.clear()
        self.process_tree.delete(*self.process_tree.get_children())
        self.task_tree.delete(*self.task_tree.get_children())
        self.gantt_ax.clear()
        self.metrics_ax.clear()
        self.gantt_canvas.draw()
        
        # Reset metrics
        self.avg_turnaround_var.set("0")
        self.avg_waiting_var.set("0")
        self.avg_response_var.set("0")
        self.cpu_util_var.set("0%")
        
        # Reset process counter
        self.process_counter = 1
        self.pid_var.set(f"P{self.process_counter}")

    def suggest_algorithm(self):
        """Suggest the best scheduling algorithm based on process characteristics"""
        if not self.processes:
            messagebox.showwarning("No Processes", "Please add some processes first!")
            return
            
        # Analyze process characteristics
        total_processes = len(self.processes)
        avg_burst_time = sum(p.burst_time for p in self.processes) / total_processes
        avg_arrival_time = sum(p.arrival_time for p in self.processes) / total_processes
        burst_variance = sum((p.burst_time - avg_burst_time) ** 2 for p in self.processes) / total_processes
        has_priority = any(p.priority > 0 for p in self.processes)
        arrival_pattern = "Bulk" if all(p.arrival_time == 0 for p in self.processes) else "Scattered"
        burst_pattern = "Uniform" if burst_variance < 5 else "Varied"
        
        # Initialize scores for each algorithm
        scores = {
            "FCFS": 0,
            "SJF": 0,
            "Priority": 0,
            "Round Robin": 0,
            "SJF Preemptive": 0,
            "Priority Preemptive": 0
        }
        
        reasons = []
        
        # FCFS Analysis
        if arrival_pattern == "Bulk":
            scores["FCFS"] += 30
            reasons.append("✓ FCFS works well for bulk arrivals")
        if burst_pattern == "Uniform":
            scores["FCFS"] += 20
            reasons.append("✓ FCFS is fair when processes have similar burst times")
        
        # SJF Analysis
        if burst_pattern == "Varied":
            scores["SJF"] += 35
            scores["SJF Preemptive"] += 40
            reasons.append("✓ SJF/SRTF optimal for varied burst times")
        if avg_burst_time < 10:
            scores["SJF"] += 15
            reasons.append("✓ SJF efficient for short processes")
        
        # Priority Analysis
        if has_priority:
            scores["Priority"] += 35
            scores["Priority Preemptive"] += 40
            reasons.append("✓ Priority-based scheduling optimal for prioritized workload")
        
        # Round Robin Analysis
        if arrival_pattern == "Scattered":
            scores["Round Robin"] += 25
            reasons.append("✓ Round Robin ensures fairness for scattered arrivals")
        if total_processes > 5:
            scores["Round Robin"] += 15
            reasons.append("✓ Round Robin good for many concurrent processes")
        
        # Preemptive vs Non-preemptive
        if arrival_pattern == "Scattered" and burst_pattern == "Varied":
            scores["SJF Preemptive"] += 20
            scores["Priority Preemptive"] += 20
            reasons.append("✓ Preemptive scheduling better for varied workloads")
        
        # Find best algorithm
        best_algorithm = max(scores.items(), key=lambda x: x[1])
        algorithm_name = best_algorithm[0]
        confidence_score = min(best_algorithm[1], 100)
        
        # Generate star rating
        star_rating = "⭐" * (confidence_score // 20)
        
        # Create detailed recommendation message
        recommendation = f"""
🤖 AI Algorithm Recommendation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ Suggested Algorithm: {algorithm_name}
📊 Confidence Score: {confidence_score}/100 {star_rating}

📝 Workload Analysis:
• Number of Processes: {total_processes}
• Average Burst Time: {avg_burst_time:.1f}
• Arrival Pattern: {arrival_pattern}
• Burst Pattern: {burst_pattern}
• Priority-based Tasks: {"Yes" if has_priority else "No"}

🎯 Reasoning:
{chr(10).join(reasons)}

💡 Key Benefits:
• {"Optimal for priority-based execution" if "Priority" in algorithm_name else
   "Minimizes average waiting time" if "SJF" in algorithm_name else
   "Fair CPU distribution" if algorithm_name == "Round Robin" else
   "Simple and predictable execution"}
• {"Responsive to high-priority tasks" if "Preemptive" in algorithm_name else
   "No context switching overhead" if algorithm_name == "FCFS" else
   "Balanced resource utilization"}
"""
        
        # Show recommendation in a custom dialog
        recommendation_dialog = tk.Toplevel(self.root)
        recommendation_dialog.title("AI Algorithm Recommendation")
        recommendation_dialog.geometry("600x500")
        
        # Add text widget with recommendation
        text_widget = tk.Text(recommendation_dialog, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, recommendation)
        text_widget.config(state=tk.DISABLED)
        
        # Add Apply button
        def apply_suggestion():
            self.algorithm_var.set(algorithm_name)
            self.on_algorithm_change()
            recommendation_dialog.destroy()
            
        apply_btn = ttk.Button(recommendation_dialog, text="Apply Suggestion", command=apply_suggestion)
        apply_btn.pack(pady=10)
        
    def get_suggestion_reasoning(self, algorithm):
        if algorithm == 'FCFS':
            return "- Simple workload with similar process characteristics\n- Good for fairness when processes have similar requirements"
        elif algorithm == 'SJF':
            return "- Short burst times detected\n- Minimizes average waiting time\n- Best for workloads with varying burst times"
        elif algorithm == 'Round Robin':
            return "- Large number of processes detected\n- Provides fair CPU time sharing\n- Good for interactive systems"
        elif algorithm == 'Priority':
            return "- Processes with different priorities detected\n- Critical processes can be executed first\n- Good for systems with varying process importance"
        elif algorithm == 'SJF Preemptive':
            return "- Short burst times detected\n- Minimizes average waiting time\n- Best for workloads with varying burst times and high priority processes"
        elif algorithm == 'Priority Preemptive':
            return "- Processes with different priorities detected\n- Critical processes can be executed first\n- Good for systems with varying process importance and high priority processes"
        
    def open_task_manager(self):
        """Open the task manager window"""
        task_manager = TaskManagerWindow(parent=self.root, scheduler=self.scheduler)
        
        # Pass the current algorithm and processes to the task manager
        if hasattr(self, 'algorithm_var'):
            current_algo = self.algorithm_var.get()
            task_manager.set_current_algorithm(current_algo)
            
        task_manager.show()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulerGUI(root)
    root.mainloop()
