'''schedule.py: Greedy Algorithms'''

'''Given a list of jobs with respective weights(priorities) and lengths(time taken by job),
compute an optimal ordering i.e. a schedule for these jobs so that the objective func, sum of 
weighted completion times is minimized, thus proving that calculated schedule is optimal!
Completion times of jobs being time elapsed since start of first job or sum of lengths of all
previous jobs'''

'''Run time of both algorithms is dominated by comparasion-based sorting steps; O(nlogn),
n being num of jobs'''

'''dict.items returns a view object whereas dict.items() returns an iterator'''

from operator import itemgetter

'''good greedy criteria of taking the ratio of job-length and job-weight (w/l). 
Always correct!'''
def schedule(jobs):
	greedyOrder = []

	#getting greedy scores (w/l)
	for job in jobs:
		greedyOrder.append((jobs[job][0], jobs[job][1], jobs[job][0] / jobs[job][1]))

	'''
	side-note: sort() and sorted() maintain original ordering of unsorted list in case
	of ties among keys. First sort step sorts jobs so that jobs with larger weights have 
	lower indices. Second sort step sorts this new ordering in decending order of greedy 
	scores, yet preserving the property that in case of ties in this step, jobs with larger 
	weights will be considered first in result!
	'''
	greedyOrder.sort(key=itemgetter(0), reverse=True)
	greedyOrder.sort(key=itemgetter(2), reverse=True)

	#calculating sum of weighted completion times of schedule!
	result = completionTime = 0
	for job in greedyOrder:
		completionTime += job[1]
		result += job[0] * completionTime

	return result

'''bad greedy criteria of taking the difference of job-length from job-weight (w - l)
Not always correct!'''
def badSchedule(jobs):
	greedyOrder = []

	#getting greedy scores (w - l)
	for job in jobs:
		greedyOrder.append((jobs[job][0], jobs[job][1], jobs[job][0] - jobs[job][1]))

	greedyOrder.sort(key=itemgetter(0), reverse=True)
	greedyOrder.sort(key=itemgetter(2), reverse=True)

	result = completionTime = 0
	for job in greedyOrder:
		completionTime += job[1]
		result += job[0] * completionTime

	return result

#init
if __name__ == '__main__':
	draft, jobs = open('jobs.txt').read().splitlines(), {}

	for i in range(1, 10000 + 1):
		jobs[i] = list(map(int, draft[i].split()))

	
	print('Objective func value for bad scheduling: ' + str(badSchedule(jobs)))
	print('Objective func value for good scheduling: ' + str(schedule(jobs)))

