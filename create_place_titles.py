from csv import DictReader
from pickle import dump

from config import path_to_pickled_set, path_to_output


place_titles = set()
with open(path_to_output) as f:
  for line in DictReader(f, delimiter="\t"):
    enwiki_title = line["enwiki_title"]
    if enwiki_title: # probably unnecessary, but playing it safe
      place_titles.add(enwiki_title)

print("created place_titles")
with open(path_to_pickled_set, "wb") as f:
  dump(place_titles, f)