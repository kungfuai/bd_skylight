# Also see: https://developers.google.com/optimization/mip/integer_opt
# https://towardsdatascience.com/modeling-and-optimization-of-a-weekly-workforce-with-python-and-pyomo-29484ba065bb
from pyschedule import Scenario, solvers, plotters, alt, plotters
from raw_data import tasks_data, workers_tasks_eligibility, workers_skills

# the planning horizon has 10 periods
S = Scenario("construction", horizon=10)

# resources
resources = {worker_id: S.Resource(worker_id, size=1) for worker_id in workers_skills}

# tasks
tasks = {
    task_id: S.Task(task_id, length=task_data["duration"], delay_cost=1)
    for task_id, task_data in tasks_data.items()
}
# for t in tasks.values():
#     print(t.length)

# Worker-Task eligibility.
for task_id in tasks:
    eligible_workers = []
    for worker_id, task_ids in workers_tasks_eligibility.items():
        if task_id in task_ids:
            eligible_workers.append(resources[worker_id])
    if len(eligible_workers) == 0:
        continue
    print(f"{task_id}: {eligible_workers}")
    for worker in eligible_workers:
        tasks[task_id] += alt(worker)

# # three tasks: cook, wash, and clean
# cook = S.Task("cook", length=1, delay_cost=1)
# wash = S.Task("wash", length=2, delay_cost=1)
# clean = S.Task("clean", length=3, delay_cost=2)

# every task can be done either by Alice or Bob
# cook += Alice | Bob
# wash += Alice | Bob
# clean += Alice | Bob

# compute and print a schedule
solvers.mip.solve(S, msg=1)
print(S.solution())
plotters.matplotlib.plot(S, img_filename="tmp.png", fig_size=(10, 10), hide_tasks=[])
