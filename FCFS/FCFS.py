import re
from collections import deque

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
            op = self.ops[self.current_op_index]
            self.remaining_time = op[1]
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
                time_val = int(m.group(1))
                resource_id = m.group(2)
                ops.append(("R", time_val, resource_id))
        else:
            ops.append(("CPU", int(token)))
    return Process(pid, arrival_time, ops)

def main():
    with open("input2.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    algo_identifier = lines[0]
    try:
        maybe = int(lines[1])
        num_processes = int(lines[2])
        process_lines = lines[3:3+num_processes]
    except:
        num_processes = int(lines[1])
        process_lines = lines[2:2+num_processes]

    processes = []
    for i, line in enumerate(process_lines):
        proc = parse_process_line(line, i+1)  
        processes.append(proc)

    ready_queue = deque()

    resources = {}
    for proc in processes:
        for op in proc.ops:
            if op[0] == "R":
                resource_id = op[2]
                if resource_id not in resources:
                    resources[resource_id] = {"queue": deque(), "current_process": None, "gantt": []}

    cpu_gantt = []        
    current_time = 0    
    current_cpu_process = None  

    def all_finished():
        return all(proc.is_finished() for proc in processes)

    while not all_finished():
        for proc in processes:
            if proc.arrival_time == current_time:
                ready_queue.append(proc)
                proc.ready_queue_entry_time = current_time

        for proc in ready_queue:
            proc.waiting_time += 1

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
                            proc_finished.ready_queue_entry_time = current_time
                            ready_queue.append(proc_finished)
                        elif next_op[0] == "R":
                            next_res = next_op[2]
                            resources[next_res]["queue"].append(proc_finished)
                    else:
                        proc_finished.finish_time = current_time
                    res["current_process"] = None
            else:
                if res["queue"]:
                    proc_res = res["queue"].popleft()
                    res["current_process"] = proc_res
                    res["gantt"].append(proc_res.pid)
                else:
                    res["gantt"].append("_")

        if current_cpu_process is None:
            if ready_queue:
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
                        current_cpu_process.ready_queue_entry_time = current_time + 1
                        ready_queue.append(current_cpu_process)
                    elif next_op[0] == "R":
                        res_id = next_op[2]
                        resources[res_id]["queue"].append(current_cpu_process)
                current_cpu_process = None

        current_time += 1

    turnaround_times = [proc.finish_time - proc.arrival_time for proc in processes]
    waiting_times = [proc.waiting_time for proc in processes]

    with open("output.txt", "w") as f:
        f.write(" ".join(str(x) for x in cpu_gantt) + "\n")
        for res_id in sorted(resources.keys()):
            f.write(" ".join(str(x) for x in resources[res_id]["gantt"]) + "\n")
        f.write(" ".join(str(x) for x in turnaround_times) + "\n")
        f.write(" ".join(str(x) for x in waiting_times) + "\n")

if __name__ == "__main__":
    main()
