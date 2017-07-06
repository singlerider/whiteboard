import random
import unittest
from bisect import bisect_left
from collections import deque

"""
Create a queue that assigns priority based on some predefined value set

Assume it will run on a single machine with limited resources
"""


# higher priority means higher weight

# the priority map is completely arbitrary
# the value should never be higher than the number of queues
# this remains constant
PRIORITY_MAP = {
    "yahoo": 1,
    "google": 2,
    "apple": 3,
    "facebook": 4,
    "myspace": 5
}


class PriorityQueue(object):
    """
    A priority-based set of queues that allow for a single API to appendleft()
        and pop()
    """

    def __init__(self, queues_count=1):
        self.priority_indices = set()  # contains unique values
        self.probabilities = []  # sorted list of integers
        self.priority_map = PRIORITY_MAP
        self.queues = []  # list of deque objects, accessed by index (priority - 1)  # noqa
        self.priority_lookup = {}  # used to map the set() of priority indices to a priority queue (from PRIORITY_MAP)  # noqa
        self.total_count = 0  # used to maintain a len(queues) count of total
        for n in range(queues_count):
            self.queues.append(deque())  # create n queues

    def __len__(self):  # resolve a call to len(PriorityQueue())
        return self.total_count  # integer incrementor

    def update_priorities(self):
        """
        When a queue becomes empty OR stops being empty, this will determines
            which queues should be considered for random lookups
        """
        self.priority_lookup = {}  # map unsorted set() of priority_indices to a priority  # noqa
        probabilities = []  # list of integers
        running_total = 0  # incrementor
        for index, priority in enumerate(self.priority_indices):
            running_total += priority
            probabilities.append(running_total)
            self.priority_lookup[index] = priority  # map index to corresponding priority  # noqa
        self.probabilities = probabilities  # overwrite previous probabilities

    def select_queue(self):
        """
        Randomly determines which queue to pop a value from

        The selected queue will be directly influenced by the priroty value
            assigned in the PRIORITY_MAP and have a corresponding weight
        """
        random_number = random.randint(  # a random number between the
            self.probabilities[0], self.probabilities[-1]  # lowest probability (first) and the highest (last)  # noqa
        )
        # the following does a binary search in O(log n) of the sorted
        # self.probabilities list, choosing a value based on the random_number
        # generated and determines the closest value that is greater
        # than the random_number:
        random_selection = bisect_left(self.probabilities, random_number)
        # the order of the set() of self.probability_indices is not
        # necessarily sorted, so use this map to determine the appropriate
        # priority based on the index of random_selection
        priority = self.priority_lookup[random_selection]
        return priority

    def appendleft(self, data):
        priority = self.priority_map[data["sender"]]
        self.queues[priority - 1].appendleft(data)
        self.total_count += 1
        # when the queue has a value when it previously did not, update
        if len(self.queues[priority - 1]) == 1:
            self.priority_indices.add(priority)
            self.update_priorities()

    def pop(self):
        priority = self.select_queue()
        if priority:
            data = self.queues[priority - 1].pop()
            self.total_count -= 1
            # when the queue has no values when it previously did, update
            if (len(self.queues[priority - 1])) == 0:
                self.priority_indices.remove(priority)
                self.update_priorities()
            return data


class PriorityQueueTestCase(unittest.TestCase):

    def setUp(self):
        self.NUMBER_OF_QUEUES = 5
        self.QUEUE_MODIFIER = self.NUMBER_OF_QUEUES ** 2  # 25
        self.QUEUE_MULTIPLIER = 10000
        self.NUMBER_OF_INSERTS = self.QUEUE_MULTIPLIER * self.QUEUE_MODIFIER  # 25000  # noqa
        self.queues = PriorityQueue(queues_count=self.NUMBER_OF_QUEUES)
        self.detailed_senders = sorted([x for x in PRIORITY_MAP.items()], key=lambda x: x[1], reverse=True)  # noqa
        self.senders = [x[0] for x in self.detailed_senders]
        self.distribution = {x: 0 for x in self.senders}
        for n in range(self.NUMBER_OF_INSERTS):
            sender = random.choice(self.senders)
            self.queues.appendleft({"sender": sender})

    def test_distribution(self):
        self.assertTrue(len(self.queues), self.NUMBER_OF_INSERTS)
        # no point in checking more than the first 1/5th
        # if the distribution is checked all the way, the numbers will match
        # and the only thing being tested would be the random module
        for n in range(self.NUMBER_OF_INSERTS):
            if n < self.NUMBER_OF_QUEUES * self.QUEUE_MULTIPLIER:
                self.distribution[self.queues.pop()["sender"]] += 1
        for sender, priority in self.detailed_senders:
            self.assertTrue(
                self.distribution[sender] >= 0.333333333 *
                priority * self.QUEUE_MULTIPLIER * 0.9 and
                self.distribution[sender] <= 0.333333333 *
                priority * self.QUEUE_MULTIPLIER * 1.1
            )  # distribution within an acceptable margin
        print(self.distribution)


if __name__ == '__main__':
    unittest.main()
