import pandas as pd
from docplex.cp.model import CpoModel, INTERVAL_MIN
from docplex.cp import modeler

# https://dataplatform.cloud.ibm.com/analytics/notebooks/v2/d0d471a5-7198-4290-9392-7086eb818957/view?access_token=0c58f505135323bf710370eb93199eab578994c2d5d3d0779a0d3fdc14b5a62f
# https://www.ibm.com/developerworks/community/forums/html/topic?id=77777777-0000-0000-0000-000014544248

tasks_data = {
    "a1": {"skill": "Carpentry A", "duration": 1},
    "a2": {"skill": "Carpentry A", "duration": 4},
    "a3": {"skill": "Plumber", "duration": 8},
    "a4": {"skill": "Electrician", "duration": 8},
}

# Prepare input.
workers_skills = {
    "r1": ["Carpentry A"],
    "r2": ["Carpentry A"],
    "r3": ["Carpentry A"],
    "r4": ["Carpentry A"],
    "r5": ["Carpentry A"],
    "r6": ["Carpentry B"],
    "r7": ["Carpentry B"],
    "r8": ["Carpentry B"],
    "r9": ["Carpentry B"],
    "r10": ["Carpentry B"],
    "r11": ["Plumber"],
    "r12": ["Electrician"],
    "r13": ["Tiler"],
    "r14": ["Drywaller"],
    "r15": ["Trades Apprentice"],
    "r16": ["Construction Associate"],
}

# Encodes whether a worker has the skill to do a task.
workers_tasks_eligibility = {
    worker_id: [
        task_id
        for task_id, task_data in tasks_data.items()
        if (task_data["skill"] in skills_of_this_worker)
    ]
    for worker_id, skills_of_this_worker in workers_skills.items()
}

deadline = 1000  # in hours

# Create model
mdl = CpoModel(name="scheduling")

# tasks

tasks = {
    task_id: mdl.interval_var(
        name=f"{task_id}, {task_data['skill']}",
        size=task_data["duration"],
        end=(INTERVAL_MIN, deadline),
    )
    for task_id, task_data in tasks_data.items()
}

allocs = {}  # key: task id, value: list of worker-task assignment variables
worker_tasks = {}  # key: worker id, value: list of worker-task assignment variables


for worker_id, task_ids in workers_tasks_eligibility.items():
    for task_id in task_ids:
        wt = mdl.interval_var(name=f"{worker_id}, {task_id}", optional=True)
        worker_tasks[worker_id] = worker_tasks.get(worker_id, [])
        worker_tasks[worker_id].append(wt)
        allocs[task_id] = allocs.get(task_id, [])
        allocs[task_id].append(wt)

for task_id, worker_task_vars in allocs.items():
    mdl.add(modeler.alternative(tasks[task_id], allocs[task_id]))

# Non-overlapping constraints. Avoid overlapping between tasks of each worker.
for worker_id, assignments in worker_tasks.items():
    mdl.add(modeler.no_overlap(assignments))


#  Create the Decision Optimization objective¶
# In this case, the sum of the skills of the assigned workers to each task will be maximized.

makespan = mdl.max(
    [
        modeler.end_of(assignment)
        for assignment in assignments
        for worker_id, assignments in worker_tasks.items()
    ]
)
mdl.add_kpi(makespan, "makespan")

total_skill = 0
for worker_id, assignments in worker_tasks.items():
    for a in assignments:
        total_skill += modeler.presence_of(a)


mdl.add(mdl.maximize(total_skill))
mdl.print_information()


msol = mdl.solve(TimeLimit=10)
msol.print_solution()
