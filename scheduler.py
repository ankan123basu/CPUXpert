from dataclasses import dataclass
from typing import List, Dict, Any
import copy

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.start_time = None
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = None
        
    def __lt__(self, other):
        """Comparison method for sorting processes"""
        if isinstance(other, Process):
            # For Priority scheduling, higher priority value means higher priority
            if hasattr(self, 'priority') and hasattr(other, 'priority'):
                return self.priority > other.priority
            return self.burst_time < other.burst_time
        return NotImplemented

    def reset(self):
        self.remaining_time = self.burst_time
        self.start_time = None
        self.completion_time = None

class Scheduler:
    def __init__(self):
        self.processes: List[Process] = []
        self.algorithm: str = None
        self.time_quantum: int = None
        self.current_time: int = 0
        self.schedule: List[Dict[str, Any]] = []
        
    def set_processes(self, processes: List[Process]):
        self.processes = copy.deepcopy(processes)
        
    def set_algorithm(self, algorithm: str, time_quantum: int = None):
        self.algorithm = algorithm
        self.time_quantum = time_quantum
        
    def run(self) -> List[Dict[str, Any]]:
        if self.algorithm == "FCFS":
            return self.fcfs()
        elif self.algorithm == "SJF":
            return self.sjf()
        elif self.algorithm == "Round Robin":
            return self.round_robin(self.time_quantum)
        elif self.algorithm == "Priority":
            return self.priority()
        elif self.algorithm == "Priority Preemptive":
            return self.priority_preemptive()
        elif self.algorithm == "SJF Preemptive":
            return self.sjf_preemptive()
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")
            
    def fcfs(self):
        """First Come First Served scheduling algorithm"""
        # Sort processes by arrival time
        sorted_processes = sorted(self.processes, key=lambda p: p.arrival_time)
        
        # Reset all processes
        for process in self.processes:
            process.reset()
            
        current_time = 0
        schedule = []
        
        for process in sorted_processes:
            # If there's a gap between processes, advance the time
            if current_time < process.arrival_time:
                current_time = process.arrival_time
                
            # Set start time if this is the first time the process runs
            if process.start_time is None:
                process.start_time = current_time
                
            # Add to schedule
            schedule.append({
                'process': process,
                'start': current_time,
                'end': current_time + process.burst_time
            })
            
            # Update current time
            current_time += process.burst_time
            
            # Set completion time
            process.completion_time = current_time
            process.remaining_time = 0
            
        self.schedule = schedule
        return schedule
        
    def sjf(self):
        """Shortest Job First scheduling algorithm (non-preemptive)"""
        # Reset all processes
        for process in self.processes:
            process.reset()
            
        # Create a copy of processes
        remaining_processes = self.processes.copy()
        
        current_time = 0
        schedule = []
        
        while remaining_processes:
            # Find available processes at current time
            available_processes = [p for p in remaining_processes if p.arrival_time <= current_time]
            
            if not available_processes:
                # No processes available, advance time to next arrival
                next_arrival = min(p.arrival_time for p in remaining_processes)
                current_time = next_arrival
                continue
                
            # Find the process with shortest burst time
            next_process = min(available_processes, key=lambda p: p.burst_time)
            
            # Set start time if this is the first time the process runs
            if next_process.start_time is None:
                next_process.start_time = current_time
                
            # Add to schedule
            schedule.append({
                'process': next_process,
                'start': current_time,
                'end': current_time + next_process.burst_time
            })
            
            # Update current time
            current_time += next_process.burst_time
            
            # Set completion time
            next_process.completion_time = current_time
            next_process.remaining_time = 0
            
            # Remove from remaining processes
            remaining_processes.remove(next_process)
            
        self.schedule = schedule
        return schedule
        
    def round_robin(self, time_quantum):
        """Round Robin scheduling algorithm"""
        # Reset all processes
        for process in self.processes:
            process.reset()
            
        # Create a copy of processes
        remaining_processes = self.processes.copy()
        
        current_time = 0
        schedule = []
        
        # Sort by arrival time initially
        ready_queue = []
        
        while remaining_processes or ready_queue:
            # Add newly arrived processes to ready queue
            newly_arrived = [p for p in remaining_processes if p.arrival_time <= current_time]
            for process in newly_arrived:
                ready_queue.append(process)
                remaining_processes.remove(process)
                
            if not ready_queue:
                # No processes in ready queue, advance time to next arrival
                if remaining_processes:
                    current_time = min(p.arrival_time for p in remaining_processes)
                continue
                
            # Get next process from ready queue
            current_process = ready_queue.pop(0)
            
            # Set start time if this is the first time the process runs
            if current_process.start_time is None:
                current_process.start_time = current_time
                
            # Calculate execution time for this quantum
            execution_time = min(time_quantum, current_process.remaining_time)
            
            # Add to schedule
            schedule.append({
                'process': current_process,
                'start': current_time,
                'end': current_time + execution_time
            })
            
            # Update current time
            current_time += execution_time
            
            # Update remaining time
            current_process.remaining_time -= execution_time
            
            # Check if process is completed
            if current_process.remaining_time <= 0:
                current_process.completion_time = current_time
            else:
                # Add newly arrived processes before re-adding current process
                newly_arrived = [p for p in remaining_processes if p.arrival_time <= current_time]
                for process in newly_arrived:
                    ready_queue.append(process)
                    remaining_processes.remove(process)
                    
                # Add back to ready queue
                ready_queue.append(current_process)
                
        self.schedule = schedule
        return schedule
        
    def priority(self):
        """Priority scheduling algorithm (non-preemptive)"""
        # Reset all processes
        for process in self.processes:
            process.reset()
            
        # Create a copy of processes
        remaining_processes = self.processes.copy()
        
        current_time = 0
        schedule = []
        
        while remaining_processes:
            # Find available processes at current time
            available_processes = [p for p in remaining_processes if p.arrival_time <= current_time]
            
            if not available_processes:
                # No processes available, advance time to next arrival
                next_arrival = min(p.arrival_time for p in remaining_processes)
                current_time = next_arrival
                continue
                
            # Find the process with highest priority (higher value = higher priority)
            next_process = max(available_processes, key=lambda p: p.priority)
            
            # Set start time if this is the first time the process runs
            if next_process.start_time is None:
                next_process.start_time = current_time
                
            # Add to schedule
            schedule.append({
                'process': next_process,
                'start': current_time,
                'end': current_time + next_process.burst_time
            })
            
            # Update current time
            current_time += next_process.burst_time
            
            # Set completion time
            next_process.completion_time = current_time
            next_process.remaining_time = 0
            
            # Remove from remaining processes
            remaining_processes.remove(next_process)
            
        self.schedule = schedule
        return schedule
        
    def priority_preemptive(self):
        """Priority scheduling algorithm (preemptive)"""
        # Reset all processes
        for process in self.processes:
            process.reset()
            
        # Create a copy of processes
        remaining_processes = self.processes.copy()
        ready_queue = []
        current_time = 0
        schedule = []
        
        while remaining_processes or ready_queue:
            # Add newly arrived processes to ready queue
            newly_arrived = [p for p in remaining_processes if p.arrival_time <= current_time]
            for process in newly_arrived:
                ready_queue.append(process)
                remaining_processes.remove(process)
                
            if not ready_queue:
                # No processes in ready queue, advance time to next arrival
                if remaining_processes:
                    current_time = min(p.arrival_time for p in remaining_processes)
                continue
                
            # Sort ready queue by priority (higher value = higher priority)
            ready_queue.sort(key=lambda p: p.priority, reverse=True)
            
            # Get highest priority process
            current_process = ready_queue[0]
            
            # Set start time if this is the first time the process runs
            if current_process.start_time is None:
                current_process.start_time = current_time
                
            # Calculate how long to run this process
            time_slice = 1  # Run for 1 time unit
            
            # Add to schedule
            schedule.append({
                'process': current_process,
                'start': current_time,
                'end': current_time + time_slice
            })
            
            # Update process state
            current_process.remaining_time -= time_slice
            current_time += time_slice
            
            # Check if process is completed
            if current_process.remaining_time <= 0:
                current_process.completion_time = current_time
                ready_queue.remove(current_process)
            
        self.schedule = schedule
        return schedule
        
    def sjf_preemptive(self):
        """Shortest Job First scheduling algorithm (preemptive)"""
        # Reset all processes
        for process in self.processes:
            process.reset()
            
        # Create a copy of processes
        remaining_processes = self.processes.copy()
        ready_queue = []
        current_time = 0
        schedule = []
        
        while remaining_processes or ready_queue:
            # Add newly arrived processes to ready queue
            newly_arrived = [p for p in remaining_processes if p.arrival_time <= current_time]
            for process in newly_arrived:
                ready_queue.append(process)
                remaining_processes.remove(process)
                
            if not ready_queue:
                # No processes in ready queue, advance time to next arrival
                if remaining_processes:
                    current_time = min(p.arrival_time for p in remaining_processes)
                continue
                
            # Sort ready queue by remaining time
            ready_queue.sort(key=lambda p: p.remaining_time)
            
            # Get process with shortest remaining time
            current_process = ready_queue[0]
            
            # Set start time if this is the first time the process runs
            if current_process.start_time is None:
                current_process.start_time = current_time
                
            # Calculate how long to run this process
            time_slice = 1  # Run for 1 time unit
            
            # Add to schedule
            schedule.append({
                'process': current_process,
                'start': current_time,
                'end': current_time + time_slice
            })
            
            # Update process state
            current_process.remaining_time -= time_slice
            current_time += time_slice
            
            # Check if process is completed
            if current_process.remaining_time <= 0:
                current_process.completion_time = current_time
                ready_queue.remove(current_process)
            
        self.schedule = schedule
        return schedule
        
    def suggest_algorithm(self) -> str:
        """Suggest the best algorithm based on process characteristics"""
        # Check if there are processes with different priorities
        priorities = [p.priority for p in self.processes]
        if len(set(priorities)) > 1:
            return 'Priority'
            
        # Check if processes have short burst times
        burst_times = [p.burst_time for p in self.processes]
        if all(bt < 5 for bt in burst_times) and len(burst_times) > 1 and max(burst_times) != min(burst_times):
            return 'SJF'
            
        # Check for many processes with similar arrival times
        if len(self.processes) > 5:
            arrival_times = [p.arrival_time for p in self.processes]
            if max(arrival_times) - min(arrival_times) < 10:  # If arrivals are clustered
                return 'Round Robin'
                
        # Default to FCFS for simple workloads or when no specific pattern is detected
        return 'FCFS'

    def get_metrics(self) -> Dict[str, float]:
        if not self.schedule:
            return {
                'avg_turnaround': 0.0,
                'avg_waiting': 0.0,
                'avg_response': 0.0,
                'cpu_utilization': 0.0
            }
            
        total_turnaround = 0
        total_waiting = 0
        total_response = 0
        completed_processes = 0
        
        for process in self.processes:
            # Only calculate metrics for processes that have completed
            if process.completion_time is not None:
                completed_processes += 1
                turnaround = process.completion_time - process.arrival_time
                waiting = turnaround - process.burst_time
                response = process.start_time - process.arrival_time if process.start_time is not None else 0
                
                total_turnaround += turnaround
                total_waiting += waiting
                total_response += response
        
        # Avoid division by zero
        if completed_processes == 0:
            return {
                'avg_turnaround': 0.0,
                'avg_waiting': 0.0,
                'avg_response': 0.0,
                'cpu_utilization': 0.0
            }
            
        avg_turnaround = total_turnaround / completed_processes
        avg_waiting = total_waiting / completed_processes
        avg_response = total_response / completed_processes
        
        # Calculate CPU utilization
        total_burst_time = sum(p.burst_time for p in self.processes)
        total_time = max(p.completion_time for p in self.processes if p.completion_time is not None)
        cpu_utilization = (total_burst_time / total_time) * 100 if total_time > 0 else 0
        
        return {
            'avg_turnaround': avg_turnaround,
            'avg_waiting': avg_waiting,
            'avg_response': avg_response,
            'cpu_utilization': cpu_utilization
        }
