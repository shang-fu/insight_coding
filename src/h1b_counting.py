import sys
import collections
from heapq import heappush, heappop


# create a class for the object inside heap, sorting by counting times. If times are equal, then sorting alphabetically.
class Element:

    def __init__(self, count, word):
        self.count = count
        self.word = word

    def __lt__(self, other):
        if self.count == other.count:
            return self.word > other.word
        return self.count < other.count

    def __eq__(self, other):
        return self.count == other.count and self.word == other.word


class Classification:

    def __init__(self):

        # total number of applications certified
        self.numOfCertifiedApplications = 0

        # hash map for recording types of occupations and their number of applications
        self.occupations = collections.defaultdict(int)

        # hash map for recording types of working states and their number of applications
        self.states = collections.defaultdict(int)

    def process(self):

        with open(sys.argv[1], 'r') as file:

            # find out which columns of data needed
            headers = file.readline().split(';')
            statusIndex = occupationIndex = stateIndex = -1

            for i in range(len(headers)):
                if headers[i][-6:] == 'STATUS':
                    statusIndex = i
                if headers[i][-8:] == 'SOC_NAME':
                    occupationIndex = i
                if headers[i][-14:] == 'WORKLOC1_STATE' or headers[i] == 'WORKSITE_STATE':
                    stateIndex = i
                if statusIndex != -1 and occupationIndex != -1 and stateIndex != -1:
                    break

            for line in file:
                data = line.split(';')

                if data[statusIndex] == 'CERTIFIED':
                    data[occupationIndex] = data[occupationIndex].lstrip('\"').rstrip('\"')
                    self.numOfCertifiedApplications += 1
                    self.occupations[data[occupationIndex]] += 1
                    self.states[data[stateIndex]] += 1

    def generateTopTenOccupations(self):

        heap = []
        topTen = []

        # using a heap to sorting top 10 occupations, if the heap size is larger than 10, pop out the smallest
        for occupation, times in self.occupations.items():
            heappush(heap, Element(times, occupation))
            if len(heap) > 10:
                heappop(heap)

        # pop out top 10 occupations each by each
        while heap:
            topTen.append(heappop(heap))

        # create output file
        with open(sys.argv[2], 'w+') as file:
            file.write("TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n")
            for element in topTen[::-1]:
                file.write(element.word + ';' + str(element.count) + ';' + str(round(element.count / self.numOfCertifiedApplications * 100, 1)) + '%\n')

    def generateTopTenStates(self):

        heap = []
        topTen = []

        # using a heap to sorting top 10 states, if the heap size is larger than 10, pop out the smallest
        for state, times in self.states.items():
            heappush(heap, Element(times, state))
            if len(heap) > 10:
                heappop(heap)

        # pop out top 10 states each by each
        while heap:
            topTen.append(heappop(heap))

        # create output file
        with open(sys.argv[3], 'w+') as file:
            file.write("TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n")
            for element in topTen[::-1]:
                file.write(element.word + ';' + str(element.count) + ';' + str(round(element.count / self.numOfCertifiedApplications * 100, 1)) + '%\n')


def main():

    # initial a Classfication object
    classification = Classification()

    # process the raw data
    classification.process()

    # generate a file for top 10 occupations
    classification.generateTopTenOccupations()

    # generate a file for top 10 states
    classification.generateTopTenStates()


main()
