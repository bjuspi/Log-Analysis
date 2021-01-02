#!/usr/bin/env python3

import re
import csv
import operator

error_ranking = {}
user_entries = {}

info_pattern = r"ticky: INFO ([\w ]*) .*\(([\w\.]+)\)"
error_pattern = r"ticky: ERROR ([\w ]*) .*\(([\w\.]+)\)"

with open("syslog.log") as f:
  for line in f.readlines():
    print(line.strip())
    error = re.search(error_pattern, line)
    info = re.search(info_pattern, line)
    if not error is None:
      error_ranking[error.group(1)] = error_ranking.get(error.group(1), 0) + 1
      if error.group(2) in user_entries.keys():
        user_entries[error.group(2)]["ERROR"] = user_entries[error.group(2)].get("ERROR", 0) + 1
      else:
        user_entries[error.group(2)] = {}
        user_entries[error.group(2)]["ERROR"] = 1
        user_entries[error.group(2)]["INFO"] = 0
    if not info is None:
      if info.group(2) in user_entries.keys():
        user_entries[info.group(2)]["INFO"] = user_entries[info.group(2)].get("INFO", 0) + 1
      else:
        user_entries[info.group(2)] = {}
        user_entries[info.group(2)]["INFO"] = 1
        user_entries[info.group(2)]["ERROR"] = 0

  f.close()

error_ranking = sorted(error_ranking.items(), key=operator.itemgetter(1), reverse=True)
user_entries = sorted(user_entries.items(), key=operator.itemgetter(0))

with open("error_message.csv", "w") as error_file:
  writer = csv.DictWriter(error_file, fieldnames=["Error", "Count"])
  writer.writeheader()
  for error in error_ranking:
    writer.writerow({"Error": error[0], "Count": error[1]})
  error_file.close()

with open("user_statistics.csv", "w") as user_file:
  writer = csv.DictWriter(user_file, fieldnames=["Username", "INFO", "ERROR"])
  writer.writeheader()
  for user in user_entries:
    writer.writerow({"Username": user[0], "INFO": user[1]["INFO"], "ERROR": user[1]["ERROR"]})
  user_file.close()

