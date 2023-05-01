"""Export dataset(s)

usage: see README.md

"""

JUST_PYTHON3 = False

import io
import sys
import os
import json
import gzip


from attr import attr

import riegeli

import contest_problem_pb2

from collections import Counter


def save_json(obj, filename, make_dirs_if_necessary=False, indent=2, **kwargs):
    """Saves compressed file if filename ends with '.gz'"""
    if make_dirs_if_necessary:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    if str(filename).endswith(".gz"):
        with gzip.open(filename, "wt") as f:
            return json.dump(obj, f, indent=indent, **kwargs)
    with open(filename, "w", encoding="utf8") as f:
        return json.dump(obj, f, indent=indent, **kwargs)



def convert_tests(tests):
  return [{"input": t.input, "output": t.output} for t in tests]

def convert_solutions(sols):  
    ans = {'PYTHON3': []} # just to make sure it's first
    for s in sols:
      name = s.Language.Name(s.language)
      if name not in ans:
        ans[name] = []
      ans[name].append(s.solution)
    return ans
    # return [
    #   {
    #     "language": s.Language.Name(s.language),
    #     "solution": s.solution
    #   } for s in sols]

def convert_solutions_py3(sols):  
  return [s.solution for s in sols if s.Language.Name(s.language)=='PYTHON3']


def convert_problem(prob):
  ans = {
      "name": prob.name,
      "source": prob.Source.Name(prob.source),
      "is_description_translated": prob.is_description_translated,
      "cf_contest_id": prob.cf_contest_id,
      "cf_index": prob.cf_index,
      "cf_points": prob.cf_points,
      "cf_rating": prob.cf_rating,
      "cf_tags": [t for t in prob.cf_tags if t],
      "difficulty": prob.Difficulty.Name(prob.difficulty),
      "input_file": prob.input_file,
      "output_file": prob.output_file,
      "memory_limit_bytes": prob.memory_limit_bytes,
      "time_limit_seconds": prob.time_limit.ToNanoseconds()/10**9,
      "description": prob.description,
      "public_tests": convert_tests(prob.public_tests),
      "generated_tests": convert_tests(prob.generated_tests),
      "private_tests": convert_tests(prob.private_tests),
  }
  if not JUST_PYTHON3:
    ans["solutions"] = convert_solutions(prob.solutions)
    ans["incorrect_solutions"] = convert_solutions(prob.incorrect_solutions)
  else:
    ans["solutions_py3"] = convert_solutions_py3(prob.solutions)
    ans["incorrect_solutions_py3"] = convert_solutions_py3(prob.incorrect_solutions)

  return ans


def convert_files(filenames, out_filename):
  """Convert a single file of contest problemsfrom .riegeli to .json.gz"""
  json_contents = []
  for filename in filenames:
    print("Converting", filename)
    assert filename.count(".riegeli") == 1
    reader = riegeli.RecordReader(io.FileIO(filename, mode='rb'),)
    json_contents.extend(convert_problem(prob) for prob in reader.read_messages(contest_problem_pb2.ContestProblem))

  save_json(json_contents, out_filename)


if __name__ == '__main__':
  print("ARGV", sys.argv)
  assert len(sys.argv) == 2, "Usage: export.py /path/to/dataset"
  path = sys.argv[1]
  import glob
  trains = glob.glob(os.path.join(path, "code_contests_train.riegeli*"))
  assert len(trains) == 128, f"Expected 128 train files, found {len(trains)}"
  convert_files(
    trains,
    os.path.join(path, "code_contests_train.json.gz")
  )
  convert_files(
    [os.path.join(path, "code_contests_valid.riegeli")], 
    os.path.join(path, "code_contests_valid.json.gz")
  )
  convert_files(
    [os.path.join(path, "code_contests_test.riegeli")], 
    os.path.join(path, "code_contests_test.json.gz")
  )

  print("Done!")

