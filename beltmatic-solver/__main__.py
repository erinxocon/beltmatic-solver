import time
from queue import PriorityQueue, Empty
import heapq


def p_queue():
    prior_queue = PriorityQueue()
    jobs = [(x, f"This is item: {x}") for x in range(1, 10**5 + 1)]
    for job in jobs:
        prior_queue.put(job)
    while 1:
        try:
            popped_item = prior_queue.get_nowait()
        except Empty:
            break


def heap_queue():
    jobs = [(x, f"This is item: {x}") for x in range(1, 10**5 + 1)]
    heapq.heapify(jobs)

    for _ in range(len(jobs)):
        popped_item = heapq.heappop(jobs)


def main():
    start_time = time.perf_counter_ns()
    heap_queue()
    end_time = time.perf_counter_ns()

    print(
        f"Adding and popping item using heapq \
	took: {(end_time - start_time) // 10 ** 6:.02f}ms"
    )

    start_time = time.perf_counter_ns()
    p_queue()
    end_time = time.perf_counter_ns()

    print(
        f"Adding and popping item using PriorityQueue\
	took: {(end_time - start_time) // 10e6:.02f}ms"
    )


if __name__ == "__main__":
    main()
