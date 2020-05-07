import json
import re
from collections import defaultdict
import operator 
import heapq
import random
import itertools
from sklearn.utils import murmurhash3_32
from html.parser import HTMLParser
from urllib.request import Request, urlopen
import urllib.request
from heapq import heappush, heappop, heapify    
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
random.seed(123)

# class item:
#     name = ""
#     count = 0

#     def __init__(self, name_in, count_in):
#         self.name = name_in
#         self.count  = count_in

#     def __lt__(self, other):
#         return self.count < other.count
    
#     def __str__(self):
#         return (self.name + ": " + str(self.count))

#     def changeCount(self, count_in):
#         self.count= count_in;

def SetUpTrendFiles():
    filename = ""
    for i in range(0, 24):
        if i < 10:
            filename = "data0" + str(i) + ".txt"
        else:
            filename = "data" + str(i) + ".txt";

        req = Request("https://getdaytrends.com/2019-05-01/" + str(i) + "/", headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read().decode("utf-8") 
        f= open(filename,"w+")
        f.write(webpage)





trendsByHour = []
allTrends = []
matchesEveryFewMinutes = []
matchesEveryFewMinutes2 = []



def GetTrendsByHour(hour):
    
    if hour < 10:
        filename = "data0" + str(hour) + ".txt"
    else:
        filename = "data" + str(hour) + ".txt";

    print(filename)
    f= open(filename,"r")
    contents = f.read()
    parser = MyHTMLParser()
    parser.feed(contents)



class MyHTMLParser(HTMLParser):
    titleOpen = 0

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        if (tag == "title"):
            self.titleOpen = 1

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        if (tag == "title"):
            self.titleOpen = 0

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        if (self.titleOpen == 1):
            title = data.split(":")[0]
            title = title.replace(" ", "")
            title = title.strip("#")
            trendsByHour.append(title)

def GetTrends():
    global trendsByHour
    for i in range(0,24):
        GetTrendsByHour(i)
        trendsByHour.pop(0)
        allTrends.append(trendsByHour)
        trendsByHour = []

GetTrends()


class PriorityQueueUpdateable(object):
    """
    Updateable Priority Queue implemented with heapq module and standard python dictionary
    """
    def __init__(self):
        self._heap = []
        self._dict = dict()
        heapify(self._heap)

    def _clear_heap(self):
        """
        Removes obsolete entries from heap
        """
        value, key = self._heap[0]
        while (key not in self._dict) or (self._dict[key] != value):
            heappop(self._heap)
            if not self._heap:
                break
            value, key = self._heap[0]

    def pop(self):
        if not self:
            raise IndexError("Queue is empty")

        self._clear_heap()

        value, key = heappop(self._heap)
        del self._dict[key]

        self._clear_heap()

        return key, value

    def peek(self):
        if not self:
            raise IndexError("Queue is empty")
        self._clear_heap()
        value, key = self._heap[0]
        return key, value

    def __contains__(self, key):
        return key in self._dict

    def __getitem__(self, key):
        if(key not in self._dict):
            return None
        return self._dict[key]

    def __len__(self):
        return len(self._dict)

    def __setitem__(self, key, value):
        self._dict[key] = value
        heappush(self._heap, (value, key))

pq = PriorityQueueUpdateable()
pq2 = PriorityQueueUpdateable()
# pq = PriorityQueueUpdateable()
# pq["hi"] = 6
# pq[1] = 5
# pq["look"] = 4
# pq[3] = 7

# print(pq.pop())
# print(pq.peek())
# print(pq.__getitem__(8))


def addToPQ(tup, was_in):
    item = tup[0]
    incrememnt = tup[1]
    if was_in:
        pq[item] = incrememnt
    else:
        val = 0
        if(pq.__getitem__(item) != None):
            val = pq.__getitem__(item)
        val = val -incrememnt
        pq[item] = val

def addToPQ2(tup, was_in):
    item = tup[0]
    incrememnt = tup[1]
    if was_in:
        pq2[item] = incrememnt
    else:
        val = 0
        if(pq2.__getitem__(item) != None):
            val = pq2.__getitem__(item)
        val = val -incrememnt
        pq2[item] = val


# addToPQ(1, 4)
# addToPQ(3, 10)
# addToPQ("cat", 100)
# print(pq.pop())
# exit(1)

class AdaptiveCountSketch:
    hashmaps = []
    d = 0
    r = 0

    def __init__(self, d_in, r_in):
        self.d = d_in
        self.r = r_in
        for i in range(0, self.d):
            self.hashmaps.append([])
        for i in range(0, self.d):
            for j in range(0,self.r):
                self.hashmaps[i].append(0)

    def insert(self, name, incrememnt):
        for i in range(0, self.d):
            spot = murmurhash3_32(name, i) % self.r
            self.hashmaps[i][spot] -= incrememnt

    def getCount(self, name):
        totals = []
        for i in range(0, self.d):
            totals.append(self.hashmaps[i][murmurhash3_32(name, i) % self.r])
        return min(totals)
            


def helper():
    acs = AdaptiveCountSketch(10, 500)
    acs.insert("greg", 500)
    acs.insert("greg", 5)
    print(acs.getCount("greg"))


def main():
    tweets = []
    hashtags = defaultdict(int)
    acs = AdaptiveCountSketch(10, 10000)
    i = 0
    a = 1
    f = open("allTags.txt", "w+")

    for x in range(1, 13):
        f1 = ''
        if x < 10:
            f1 = '0' + str(x)
        else:
            f1 = str(x)
        for y in range(0,59):
            f2 = ''
            if y < 10:
                f2 = '0' + str(y)
            else:
                f2 = str(y)
            print('01/' +f1 + '/' + f2 + '.json')
            for line in open('01/' +f1 + '/' + f2 + '.json', 'r'):
                # tweets.append(json.loads(line))
                tweet = json.loads(line)
                if('text' in tweet.keys()):
                    text = tweet['text']
                    if('#' in text):
                        for tag in (re.findall(r"#(\w+)", text)):
                            acs.insert(tag, a)
                            addToPQ((tag, 1), False)
                            addToPQ2((tag, a), False)
                            f.write(tag + " ")
                            
            if(y %  5 == 0):
                print("Comparing: " + str(x)+ " : " +str(y))
                CountAndCompare(x, y)

    # f = open("allTags.txt", 'r')
    # contents = f.read
    # contents.split(" ")
    # for tag in contents:
    #     acs.insert(tag, a)
    #     addToPQ((tag, 1), False)
    #     addToPQ2((tag, a), False)
    #     f.write(tag + " ")


    # # sorted_d = sorted(hashtags.items(), key=operator.itemgetter(1), reverse=True)

    print("NumMatches");
    print(matchesEveryFewMinutes)
    print(matchesEveryFewMinutes2)

    for i in range(0,20):
        print(i)
        print(pq.pop())




def CountAndCompare(x, y):
    vals = []
    tups = []
    vals2 = []
    tups2 = []

    for i in range(0, 500):
        tup = pq.pop()
        tups.append(tup)
        vals.append(tup[0])
    for i in range(0, 500):
        tup = pq2.pop()
        tups2.append(tup)
        vals2.append(tup[0])
    
    matches = 0
    matches2 = 0
    for val in vals:
        if val in allTrends[x]:
            matches+=1
            print("Match: " + str(val))
    for val in vals2:
        if val in allTrends[x]:
            matches2+=1
            print("Match: " + str(val))
    matchesEveryFewMinutes.append(matches)
    matchesEveryFewMinutes2.append(matches2)
    for tup in tups:
        addToPQ(tup, True)
    for tup in tups:
        addToPQ(tup, True)


def makeLineGraph():
    plt.plot(matchesEveryFewMinutes, 'r-', label = 'Summed')
    plt.plot(matchesEveryFewMinutes2,'b-', label = 'Time Adaptive')
    plt.title('Num Matches in top 500: First 12 Hours')
    plt.ylabel('Matches')
    plt.xlabel('Timestamp every 5 mins')
    # red_patch = mpatches.Patch(color='red', label='')
    # blue_patch = mpatches.Patch(color='red', label='The red data')
    plt.legend()
    plt.show()





SetUpTrendFiles()
main()
makeLineGraph()