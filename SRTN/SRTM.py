import re
from collections import deque

# Global variables
time_quantum =0


class Process:
    def __init__(self, pid, arrival_time, ops):
        self.pid = pid            
        self.arrival_time = arrival_time                
        self.ops = ops                                 
        self.current_op_index = 0                       
        self.remaining_time = ops[0][1] if ops else 0     
        self.waiting_time = 0                           
        self.finish_time = None                         
        self.ready_queue_entry_time = arrival_time      

    def current_op(self):
        if self.current_op_index < len(self.ops):
            return self.ops[self.current_op_index]
        return None

    def advance_op(self):
        self.current_op_index += 1
        if self.current_op_index < len(self.ops):
            self.remaining_time = self.ops[self.current_op_index][1]
        else:
            self.remaining_time = 0

    def is_finished(self):
        return self.current_op_index >= len(self.ops)

def parse_process_line(line, pid):
    tokens = line.split()
    arrival_time = int(tokens[0])
    ops = []
    for token in tokens[1:]:
        if '(' in token:
            m = re.match(r"(\d+)\((R\d*)\)", token)
            if m:
                ops.append(("R", int(m.group(1)), m.group(2)))
        else:
            ops.append(("CPU", int(token)))
    return Process(pid,  arrival_time, ops)

def read_input(filename):
    global time_quantum
    with open(filename, "r") as f:
        algo_identifier = int(f.readline().strip())
        time_quantum = int(f.readline().strip()) if algo_identifier == 2 else None
        num_processes = int(f.readline().strip())
        process_lines = [f.readline().strip() for _ in range(num_processes)]
    return algo_identifier, time_quantum, num_processes, process_lines

def initialize_processes(process_lines):
    return [parse_process_line(line, i+1) for i, line in enumerate(process_lines)]

def initialize_resources(processes):
    resources = {}
    for proc in processes:
        for op in proc.ops:
            if op[0] == "R":
                resource_id = op[2]
                if resource_id not in resources:
                    resources[resource_id] = {"queue": deque(), "current_process": None, "gantt": []}
    return resources

def all_finished(processes):
    return all(proc.is_finished() for proc in processes)

def schedule_processes(processes, resources):
    ready_queue = deque()
    cpu_gantt = []        
    current_time = 0    
    current_cpu_process = None  

    while not all_finished(processes):
        for proc in processes:
            if proc.arrival_time == current_time:
                ready_queue.append(proc)
                proc.ready_queue_entry_time = current_time

        for proc in ready_queue:
            proc.waiting_time += 1

        process_resources(resources, ready_queue, current_time)

        if current_cpu_process is None and ready_queue:
            current_cpu_process = ready_queue.popleft()

        if current_cpu_process is None:
            cpu_gantt.append("_")
        else:
            cpu_gantt.append(current_cpu_process.pid)
            current_cpu_process.remaining_time -= 1
            if current_cpu_process.remaining_time == 0:
                current_cpu_process.advance_op()
                if current_cpu_process.is_finished():
                    current_cpu_process.finish_time = current_time + 1
                else:
                    next_op = current_cpu_process.current_op()
                    if next_op[0] == "CPU":
                        ready_queue.append(current_cpu_process)
                    elif next_op[0] == "R":
                        resources[next_op[2]]["queue"].append(current_cpu_process)
                current_cpu_process = None
        current_time += 1
    return cpu_gantt

def process_resources(resources, ready_queue, current_time):
    for res_id, res in resources.items():
        if res["current_process"]:
            res["current_process"].remaining_time -= 1
            res["gantt"].append(res["current_process"].pid)
            if res["current_process"].remaining_time == 0:
                proc_finished = res["current_process"]
                proc_finished.advance_op()
                if not proc_finished.is_finished():
                    next_op = proc_finished.current_op()
                    if next_op[0] == "CPU":
                        proc_finished.ready_queue_entry_time = current_time+1
                        ready_queue.append(proc_finished)
                    elif next_op[0] == "R":
                        resources[next_op[2]]["queue"].append(proc_finished)
                proc_finished.finish_time = current_time+1
                res["current_process"] = None
        else:
            if res["queue"]:
                proc_res = res["queue"].popleft()
                res["current_process"] = proc_res
                res["gantt"].append(proc_res.pid) 
                res["current_process"].remaining_time -= 1     
            else:
                res["gantt"].append("_")

def update_waiting_time(ready_queue, current_cpu_process, resources):
    for proc in ready_queue:
        if proc is not current_cpu_process and all(proc is not res["current_process"] for res in resources.values()):
            proc.waiting_time += 1
            if (proc.pid == 1):
                print(proc.waiting_time)

def shortest_remaining_time(processes, resources):
    ready_queue = deque()
    cpu_gantt = []        
    current_time = 0    
    current_cpu_process = None  

    while not all_finished(processes):
        for proc in processes:
            if proc.arrival_time == current_time:
                ready_queue.append(proc)
                proc.ready_queue_entry_time = current_time


        if current_time == 34:
            print("debug")
        if current_cpu_process is None and ready_queue:
            ready_queue = deque(sorted(ready_queue, key=lambda x: x.remaining_time))
            current_cpu_process = ready_queue.popleft()
            if (current_cpu_process.ready_queue_entry_time > current_time):
                ready_queue.appendleft(current_cpu_process)
                current_cpu_process = None
        
        update_waiting_time(ready_queue, current_cpu_process, resources)
        
        process_resources(resources, ready_queue, current_time)

        if current_cpu_process is None:
            cpu_gantt.append("_")
        else:
            cpu_gantt.append(current_cpu_process.pid)
            current_cpu_process.remaining_time -= 1
            if current_cpu_process.remaining_time == 0:
                current_cpu_process.advance_op()
                if current_cpu_process.is_finished():
                    current_cpu_process.finish_time = current_time + 1
                else:
                    next_op = current_cpu_process.current_op()
                    if next_op[0] == "CPU":
                        ready_queue.append(current_cpu_process)
                    elif next_op[0] == "R":
                        resources[next_op[2]]["queue"].append(current_cpu_process)
            else :
                ready_queue.append(current_cpu_process)
                ready_queue = deque(sorted(ready_queue, key=lambda x: x.remaining_time))
            current_cpu_process = None
        
        current_time += 1
    return cpu_gantt
         


def write_output(filename,cpu_gantt, resources, processes):
    turnaround_times = [proc.finish_time - proc.arrival_time for proc in processes]
    waiting_times = [proc.waiting_time for proc in processes]
    
    with open(filename, "w") as f:
        f.write(" ".join(str(x) for x in cpu_gantt) + "\n")
        for res_id in sorted(resources.keys()):
            f.write(" ".join(str(x) for x in resources[res_id]["gantt"]) + "\n")
        f.write(" ".join(str(x) for x in turnaround_times) + "\n")
        f.write(" ".join(str(x) for x in waiting_times) + "\n")

def main():
    algo_identifier, time_quantum, num_processes, process_lines = read_input("input.txt")
    processes = initialize_processes(process_lines)
    resources = initialize_resources(processes)
    cpu_gantt = shortest_remaining_time(processes, resources)
    write_output("output.txt", cpu_gantt, resources, processes)

if __name__ == "__main__":
    main()
