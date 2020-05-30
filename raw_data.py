tasks_data = {
    "t1": {"skill": "Carpentry A", "duration": 1},
    "t2": {"skill": "Carpentry A", "duration": 4},
    "t3": {"skill": "Plumber", "duration": 8},
    "t4": {"skill": "Electrician", "duration": 8},
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
