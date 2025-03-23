# CPU Scheduling Simulator

An interactive CPU scheduling algorithm simulator that demonstrates various scheduling algorithms including FCFS, SJF, Round Robin, and Priority Scheduling.
 It also demonstrates real-time system monitoring, AI-driven recommendations, and 3D process visualization

🚀 Features

✅ CPU Scheduling Algorithm Simulation

Supports FCFS, SJF (Preemptive & Non-Preemptive), Round Robin, and Priority Scheduling
Dynamic Gantt chart visualization for process execution
Real-time performance metrics: Average Waiting Time, Turnaround Time, and CPU Utilization


✅ Real-Time System Monitoring

Displays CPU usage, memory consumption, disk I/O, and network activity
Task Manager-like interface to pause, resume, or terminate processes

✅ 3D Process Visualization

Animated process states: Ready, Running, Waiting, and Terminated
Graphical representation of queue transitions and scheduling execution

✅ AI-Driven Scheduling Recommendations

Analyzes system workload and process characteristics
Suggests the most efficient scheduling algorithm dynamically
Adaptive scheduling that optimizes based on real-time performance


🛠 Technologies Used

Programming Languages
Python (Backend & Logic)
JavaScript (Visualization & UI Enhancements)

Libraries and Tools

Matplotlib (>=3.7.1) → Gantt chart and CPU load graphs
NumPy (>=1.24.3) → Performance analysis and data processing
Pillow (>=9.5.0) → Image processing for UI enhancements
Tkinter / PyQt → GUI implementation
Psutil → System monitoring (CPU, memory, processes)
OpenGL / Three.js → 3D visualization of processes

Other Tools

GitHub → Version control and project management
Jupyter Notebook → Testing and algorithm validation

📦 Installation
Clone the Repository
git clone https://github.com/yourusername/cpu-scheduler-simulator.git

cd cpu-scheduler-simulator

Install Dependencies
pip install -r requirements.txt

Run the Application
python main.py

🎮 Usage
Input Processes: Define Arrival Time, Burst Time, and Priority

Select Scheduling Algorithm: Choose from FCFS, SJF, Round Robin, or Priority Scheduling

Start Simulation: Click Start Simulation to execute

Visualize Execution: Observe real-time Gantt charts and 3D process states

Analyze Performance: View Waiting Time, Turnaround Time, and Throughput

AI Recommendations: Receive optimal scheduling algorithm suggestions based on system workload

📊 Example Outputs
Gantt Chart Example
Performance Metrics Display

📌 Future Scope
🔹 Support for additional scheduling algorithms
🔹 Improved AI-based adaptive scheduling using deep learning
🔹 More detailed process execution statistics and logging
🔹 Cloud-based execution for multi-user simulation

🤝 Contributing
Fork the Repository

Create a New Branch:
git checkout -b feature/your-feature-name

Make Your Changes
Commit and Push:
git commit -m "Added new feature"
git push origin feature/your-feature-name
Create a Pull Request


## Usage

1. Add processes using the input form
2. Select desired scheduling algorithm
3. Click "Start Simulation" to run
4. View results in real-time through Gantt chart
5. Analyze performance metrics
