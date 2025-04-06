# CPU Scheduling Simulator

An interactive CPU scheduling algorithm simulator that demonstrates various scheduling algorithms including FCFS, SJF, Round Robin, and Priority Scheduling.
 It also demonstrates real-time system monitoring, AI-driven recommendations, and 3D process visualization
 
![Screenshot 2025-03-29 191258](https://github.com/user-attachments/assets/9793beef-aaa2-460d-a149-6e7bed0c341d)

![Screenshot 2025-03-23 231207](https://github.com/user-attachments/assets/ee9bb555-c05e-4229-bdfa-22ccd1ee7c43)

![Screenshot 2025-03-23 231310](https://github.com/user-attachments/assets/11a3ee6b-e68c-4123-96fe-759f1708197a)

![Screenshot 2025-03-23 231402](https://github.com/user-attachments/assets/c97307e6-1373-4aba-be23-9601b28e8288)

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

```bash
OS_PROJECT/
├── __pycache__/                  # Compiled bytecode files
│   ├── scheduler.cpython-*.pyc
│   └── task_manager.cpython-*.pyc
│
├── main.py                       # Main entry point for the project
├── scheduler.py                  # Scheduling algorithms and logic
├── task_manager.py              # Handles task/process management
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
```

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
Clone the Repository ->
git clone https://github.com/ankan123basu/cpu-scheduler-simulator.git

cd cpu-scheduler-simulator

Install Dependencies ->
pip install -r requirements.txt

Run the Application ->
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

Create a New Branch: ->
git checkout -b feature/your-feature-name

Make Your Changes
Commit and Push: ->
git commit -m "Added new feature"
git push origin feature/your-feature-name
Create a Pull Request

