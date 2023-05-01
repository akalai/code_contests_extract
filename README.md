Installation and execution instructions below.

# code_contests Converted format

There are 3 converted files:
1. code_contests_train.json.gz (3.9 GB compressed)
2. code_contests_valid.json.gz  (26M compressed)
3. code_contests_test.json.gz  (32M compressed)

`code_contests_train.json.gz` contains about 13k problems:
* Correct solutions:
  * CPP: 1.7M
  * Python3: 1.5M (each problem has many solutions!)
  * Java: 0.9M
* Incorrect solutions:
  * CPP: 4.8M
  * Python3: 1.7M
  * Java: 1M

I'm seeing around 2\% duplicates.

To load the python-3 solutions,
```
import gzip
import json
from collections import Counter
with gzip.open("code_contests_train.json.gz", "rt") as f:
    problems = json.load(f)  # takes a while!
correct_counts = Counter(lang for p in problems for lang in p["solutions"] for _ in p["solutions"][lang])
print("Correct solutions by language:\n", correct_counts.most_common())
incorrect_counts = Counter(lang for p in problems for lang in p["incorrect_solutions"] for _ in p["incorrect_solutions"][lang])
print("Incorrect solutions by language:\n", incorrect_counts.most_common())
```


These are just gzipped json files, for train, validation, and test.

Each problem has the following fields:
* `name` - unique string id
* `description` - string of contest problem description
* `solutions` - dictionary mapping language to list of strings
* `incorrect_solutions` - dictionary mapping language to incorrect solutions only, list of strings
* `source` - string indicating where it came from. Counts:

count  | source name 
------ | ----------- 
8,101  | CODEFORCES  
2,151  | AIZU        
1,323  | ATCODER     
1,267  | HACKEREARTH 
  768  | CODECHEF    

* `is_description_translated`: True/False
* `untranslated_description`: non-empty if the above is `True`
* `cf_contest_id`: some kind of id within conetst  (if codeforces)?
* `cf_index`: A-R but also A1, A2, empty string for non-codeforces (5513)
* `cf_points`: `0.0`-`5250.0`, 0.0 for non-codeforces and also some codeforces (7,587)
* `cf_rating`: 0, 800-3500, 1100 median, 1600 mode, 1109.1 mean
* `cf_tags`: list of string tags
* `difficulty`: weird string difficulty, looks like codeforces
* `input_file`: rarely used
* `output_file`: rarely used
* `memory_limit_bytes`: for evaluation
* `time_limit_seconds`: for evaluation
* public_tests: list of `{"input": __, "output": __}`

# Original Fields

## `source` and `Source`

number | source name | source value
------ | ----------- | ------------
8,101  | CODEFORCES  | 2
2,151  | AIZU        | 7
1,323  | ATCODER     | 6
1,267  | HACKEREARTH | 3
  768  | CODECHEF    | 1

```python
>>> pp.Source.items()
[('UNKNOWN_SOURCE', 0), ('CODECHEF', 1), ('CODEFORCES', 2), ('HACKEREARTH', 3), ('CODEJAM', 4), ('ATCODER', 6), ('AIZU', 7)]
```

## `name`

* unique string, use as id?

## `is_description_translated`

* True/False
* 1,088 AIZU problems have it True, everything else False
* These also have `.untranslated_description` field not equal to `''`


## `cf_contest_id`

* 0 if not codeforces (5513)
* 5 is most common codeforces value (684*5 occurrences)

## `cf_index`

* A-R but also A1, A2
* empty string for non-codeforces (5513)

## `cf_points`

* 0.0-5250.0
* 0.0 for non-codeforces and also some codeforces (7,587)

## `cf_rating` 0, 800-3500

* 0 if not in codeforces or if no rating (5627)
* 1100 median, 1600 mode, 1109.1 mean

## `cf_tags`

* `list(p.cf_tags)` is a list of tags for codeforces problems
* many of them have an empty string in them, so ignore the empty strings


## `difficulty` and `Difficulty`

* difficulty is a key into the Difficulty enum

```python
>>> Counter(p.Difficulty.Name(p.difficulty) for p in problems).most_common()
[('UNKNOWN_DIFFICULTY', 4742), ('B', 1399), ('C', 1398), ('A', 1395), ('D', 1390), ('E', 1359), ('F', 653), ('EXTERNAL', 359), ('MEDIUM', 265), ('G', 261), ('H', 105), ('HARD', 72), ('EASY', 67), ('I', 54), ('J', 32), ('K', 17), ('L', 15), ('M', 11), ('N', 6), ('HARDER', 5), ('O', 2), ('P', 1), ('Q', 1), ('R', 1)]
```

## `input_file`, `output_file`

* 22 codeforces problems have a `input_file='input.txt'` and `output_file='output.txt'`
* Not sure what they are, maybe ignore these?

## `memory_limit_bytes`

Median 256_000_000 = 256 MB

## `description`

* string of lenght 29-12,976 chars (median 1,637) 
* super-short problems are all from AIZU which are just a couple of examples of input 

## `time_limit`

* Convert to a string 
```python
>>> Counter(p.time_limit.ToNanoseconds()/10**9 for p in problems).most_common(10)
[(2.0, 5169), (1.0, 3580), (0.0, 2039), (3.0, 884), (8.0, 679), (4.0, 396), (5.0, 390), (1.5, 109), (6.0, 90), (2.5, 65)]
```



## public_tests, generated_tests, private_tests 

* each test is an object that has a .input, .output

```python
def convert_tests(tests):
  return [[t.input, t.output] for t in tests]
```

##  solutions, incorrect_solutions 

* each solution has a .language and a .solution

```python
def convert_solutions(sols):
  return [[s.Language.name(s.language), s.solution] for s in sols]
```



# Memory (compression 4x)

memory 12GB when we read in all puzzles even though the dataset is 2.9GB 

# EXECUTION

To run, after the nightmare of installation below, you run: 

```
PYTHONINSPECT=1 bazel run --repo_env=CC=/usr/bin/clang -c opt :export /data/adam/code_contests/dm-code_contests
```

There is also a `PYTHON_ONLY` flag in the file if you just want that.

# CodeContests

CodeContests is a competitive programming dataset for machine-learning. This
dataset was used when training
[AlphaCode](https://deepmind.com/blog/article/Competitive-programming-with-AlphaCode).

It consists of programming problems, from a variety of sources:

Site        | URL                         | Source
----------- | --------------------------- | ------
Aizu        | https://judge.u-aizu.ac.jp  | [CodeNet](https://github.com/IBM/Project_CodeNet)
AtCoder     | https://atcoder.jp          | [CodeNet](https://github.com/IBM/Project_CodeNet)
CodeChef    | https://www.codechef.com    | [description2code](https://github.com/ethancaballero/description2code)
Codeforces  | https://codeforces.com      | [description2code](https://github.com/ethancaballero/description2code) and Codeforces
HackerEarth | https://www.hackerearth.com | [description2code](https://github.com/ethancaballero/description2code)

Problems include test cases in the form of paired inputs and outputs, as well as
both correct and incorrect human solutions in a variety of languages.

## Downloading the dataset

[Install the Cloud SDK](https://cloud.google.com/sdk/docs/quickstart), which
provides the `gsutil` utility. You can then download the full data (~3GiB) with,
e.g:

```
gsutil -m cp -r gs://dm-code_contests /tmp
```

The data consists of `ContestProblem` protocol buffers in
[Riegeli](https://github.com/google/riegeli) format. See `contest_problem.proto`
for the protocol buffer definition and documentation of its fields.

The dataset contains three splits:

Split      | Filename
---------- | ----------------------------------------
Training   | `code_contests_train.riegeli-*-of-00128`
Validation | `code_contests_valid.riegeli`
Test       | `code_contests_test.riegeli`

There is example code for iterating over the dataset in C++ (in
`print_names.cc`) and Python (in `print_names_and_sources.py`). For example, you
can print the source and name of each problem in the validation data by
[installing bazel](https://docs.bazel.build/versions/main/install.html) and then
running:

```
# Also maybe helpful: https://www.kaggle.com/code/usaiprashanth/finetuning

# Install bazel: Use our custom APT repository # https://docs.bazel.build/versions/main/install-ubuntu.html#install-on-ubuntu
sudo apt install apt-transport-https curl gnupg
curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor > bazel.gpg
sudo mv bazel.gpg /etc/apt/trusted.gpg.d/
echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
sudo apt update && sudo apt install bazel

sudo apt-get install python-dev python2.7-dev

sudo apt install clang

bazel run --repo_env=CC=/usr/bin/clang -c opt :print_names_and_sources /datadrive/code_contests/dm-code_contests/code_contests_valid.riegeli 

bazel run -c opt \
  :print_names_and_sources /tmp/dm-code_contests/code_contests_valid.riegeli
```

Or do the same for the training data with the following command (which will
print around 13000 lines of output):

```
bazel run -c opt \
  :print_names_and_sources /tmp/dm-code_contests/code_contests_train.riegeli*
```

## Executing and evaluating solutions

The `execution` subdirectory contains code for executing a solution and
evaluating whether it solves a problem. `solve_example` demonstrates this
functionality, and can be run with e.g.

```
bazel run -c opt execution:solve_example -- \
  /tmp/dm-code_contests/code_contests_valid.riegeli
```

The execution code defaults to using Python 3.9 and 2.7, located at
`/usr/bin/python3.9` and `/usr/bin/python2.7`, with standard libraries at
`/usr/lib/python3.9` and `/usr/lib/python2.7`. These can be changed with the
flags defined in `py_locations.cc`, for example:

```
bazel run -c opt execution:solve_example -- \
  --valid_path=/tmp/dm-code_contests/code_contests_valid.riegeli \
  --python3_path=/usr/bin/python3.10 --python3_library_paths=/usr/lib/python3.10
```

## Supported platforms

This repository is supported on Linux, compiled with clang.

## Citing this work

If you use this dataset or code, please cite this paper:

```
@article{li2022competition,
  title={Competition-Level Code Generation with AlphaCode},
    author={Li, Yujia and Choi, David and Chung, Junyoung and Kushman, Nate and
    Schrittwieser, Julian and Leblond, R{\'e}mi and Eccles, Tom and
    Keeling, James and Gimeno, Felix and Dal Lago, Agustin and
    Hubert, Thomas and Choy, Peter and de Masson d'Autume, Cyprien and
    Babuschkin, Igor and Chen, Xinyun and Huang, Po-Sen and Welbl, Johannes and
    Gowal, Sven and Cherepanov, Alexey and Molloy, James and
    Mankowitz, Daniel and Sutherland Robson, Esme and Kohli, Pushmeet and
    de Freitas, Nando and Kavukcuoglu, Koray and Vinyals, Oriol},
  journal={arXiv preprint arXiv:2203.07814},
  year={2022}
}
```

## License

The code is licensed under the
[Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).

All non-code materials provided are made available under the terms of the CC BY
4.0 license
([Creative Commons Attribution 4.0 International license](https://creativecommons.org/licenses/by/4.0/legalcode)).

We gratefully acknowledge the contributions of the following:

*   Codeforces materials are sourced from http://codeforces.com.
*   Description2Code materials are sourced from:
    [Description2Code Dataset](https://github.com/ethancaballero/description2code),
    licensed under the
    [MIT open source license](https://opensource.org/licenses/MIT), copyright
    not specified.
*   CodeNet materials are sourced from:
    [Project_CodeNet](https://github.com/IBM/Project_CodeNet), licensed under
    [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0), copyright not
    specified.

Use of the third-party software, libraries code or data may be governed by
separate terms and conditions or license provisions. Your use of the third-party
software, libraries or code may be subject to any such terms. We make no
representations here with respect to rights or abilities to use any such
materials.

## Disclaimer

This is not an official Google product.
