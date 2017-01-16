#!/usr/bin/env python
"""Generate play/pause/seeked event heatmaps from raw Coursera event data.

Usage: grep 'user\.video\.lecture\.action.*\(play\|pause\|seeked\)' *ClickStreamData_NonPII.csv | cut -d, -f3,10,13 | sed -E 's/https:\/\/class.coursera.org\/.*\/lecture\/view\?lecture_id\=([0-9]+).*$/\1/' | awk 'BEGIN{FS=OFS=","} { print $3,$1,$2 }' | ./gen_heatmaps.py
Usage (normalization with num users): grep 'user\.video\.lecture\.action.*\(play\|pause\|seeked\)' *ClickStreamData_NonPII.csv | cut -d, -f3,10,11,13 | sed -E 's/https:\/\/class.coursera.org\/.*\/lecture\/view\?lecture_id\=([0-9]+).*$/\1/' | awk 'BEGIN{FS=OFS=","} { print $4,$1,$2,$3 }' | ./gen_heatmaps.py
"""

from collections import defaultdict, Counter
import csv
import json
import sys

lectures = defaultdict(Counter)
lecture_mins = defaultdict(int)

watchers = {}

reader = csv.reader(sys.stdin)
for row in reader:
    lecture_id = int(row[0])
    user_id = row[3]
    if lecture_id not in watchers:
        watchers[lecture_id] = []
    if user_id not in watchers[lecture_id]:
        watchers[lecture_id].append(user_id)

    try:
        if float(row[1]) > 0:
            minute = int(float(row[1])) / 60
            if minute > 60:
                print lecture_id, minute
                continue
            lectures[lecture_id][minute] += 1
            lecture_mins[lecture_id] = max(lecture_mins[lecture_id], minute + 1)
    except ValueError:
        continue

lectidmap = {11:'1-1', 23:'1-2',
25:'2-1',27:'2-2', 29:'2-3',31:'2-4',19:'2-5',33:'2-6',35:'2-7',37:'2-8',39:'2-9',
41:'3-1',43:'3-2',45:'3-3',47:'3-4',49:'3-5',51:'3-6',59:'3-7',53:'3-8',55:'3-9',
61:'4-1',67:'4-2',65:'4-3',77:'4-4',79:'4-5',69:'4-6',117:'4-7',73:'4-8',75:'4-9',81:'4-10',
101:'5-1',99:'5-2',97:'5-3', 103:'5-4',105:'5-5',95:'5-6',107:'5-7',109:'5-8',93:'5-9',91:'5-10',111:'5-11',89:'5-12',113:'5-13',115:'5-14',
87:'5-15'}
#keys '71':'003', and '63':'004' don't exist in current course
# lectidmap[lecture_id]

heatmaps = {}
for lecture_id, counts in lectures.iteritems():
    try:
        sortedlecture_id = lectidmap[lecture_id]
        heatmaps[sortedlecture_id] = [0] * lecture_mins[lecture_id]
        for minute in sorted(lectures[lecture_id]):
            heatmaps[sortedlecture_id][minute] = lectures[lecture_id][minute]/float(len(watchers[lecture_id]))
    except KeyError:
        print lecture_id
        continue
    
print "#lects: ", len(heatmaps)
with open('textretrieval_normalized_heatmaps.json','w') as f:
    json.dump(heatmaps, f, sort_keys=True, indent=4)
#print json.dumps(heatmaps)
