[![Build Status](
https://app.travis-ci.com/nickrusso42518/zhong.svg?branch=master)](
https://app.travis-ci.com/nickrusso42518/zhong)

# Chinese Language Trainer
A simple game to learn simplified Mandarin Chinese. It includes visual and
audio test questions and a customizable question database file. It includes
Chinese symbols, pinyin, and English definitions/descriptions. Output from
each question is colorized with green (correct) or red (incorrect) for
quick gameplay and scorekeeping.

> Contact information:\
> Email:    njrusmc@gmail.com\
> Twitter:  @nickrusso42518

  * [Installation](#installation)
  * [Quick Start](#quick-start)
  * [Advanced Usage](#advanced-usage)
  * [Forking](#forking)
  * [Testing](#testing)
  * [Disclaimer](#disclaimer)

## Installation
You must be running Python 3.6 or later.
Be sure to install the required packages before starting:
```
pip install -r requirements.txt
```

## Quick Start

Basic usage:
```
$ python play.py -h
usage: play.py [-h] [-c] [-p] [-s] [-r RATE] [-i INFILE]

options:
  -h, --help            show this help message and exit
  -a, --auto            enable auto-play (hands-free) mode, Ctrl+C to quit
  -c, --nochin          disable (mask) presentation of chinese symbols
  -p, --nopin           disable (mask) presentation of pinyin symbols
  -s, --nosound         disable sound; no audio narration of phrases
  -r RATE, --rate RATE  adjust rate of speech in words per minute (90 to 300)
  -i INFILE, --infile INFILE
                        input file in CSV format (chinese,pinyin,english)
```

Check the `inputs/` directory for sample CSV files. Be warned; these
are frequently updated.

## Advanced Usage
Detailed explanation:
  * `-i`: Pass in a CSV import file. The file must contain exactly 3 columns:
          chinese,pinyin,english. You can check the `default.csv` file for an
          example of proper formatting. The file may include comments beginning
          with the `#` symbolas in Python or YAML. Defaults to `default.csv`
          which is my current (and constantly growing) general-purpose list.

  * `-a`: Enable auto-scroll (hands-free) mode. This disables per-question
          input and automatically scrolls to the next question after a 5
          second pause. It's good for practing pronunciating and listening
          rather then translating into English.

  * `-s`: Enable nosound mode. This disables audio narration of the Chinese
          symbols. Learners must rely entirely on sight. The game will
          run faster as well. Note that audio narration is only available
          on MacOS, so Windows and Linux users are always in nosound mode.

  * `-c`: Enable nochin mode. This prints Chinese symbols with a black
          foreground and background color. This effectively masks the Chinese
          symbols; learner relies on sounds and/or pinyin. Using
          the mouse, you can highlight the Chinese symbols to reveal them if
          you need a hint; this technique should be used sparingly.

  * `-p`: Enable nopin mode. This prints pinyin symbols with a black
          foreground and background color. Same concept as nochin mode.

  * `-r`: The MacOS `say` command supports a range of narration rates,
          depending on the language spoken. The slowest (easiest) is 90
          words per minute, the fastest (hardest) is 300, and the default
          (most natural) is 180.

Example usages of minor options:
```
$ python play.py
$ python play.py -i inputs/tp.csv
$ python play.py -c
$ python play.py -c -i inputs/tp.csv
$ python play.py -p -r 120
$ python play.py -c -r 120 -i inputs/tp.csv
$ python play.py -r 120
$ python play.py -s
$ python play.py -s -i inputs/tp.csv
```

Invalid usages:
  * `python play.py -c -p -s`: Combination is never valid. Users have
    no visual or audible cues for learning, so this is useless. Program
    exits with return code 2 and an informative error message.
  * `$ python play.py -i inputs/nonexist.csv`: If a nonexistent file
    is supplied, the program exits with return code 3 and the corresponding
    `FileNotFoundError` message.
  * `$ python play.py -s`: Technically accepted on any platform,
    but `-s` has no effect on non-MacOS systems (Windows, Linux, etc.)
  * `$ python play.py -c -p`: Technically accepted on any platform,
    but `-c -p` has no effect on non-MacOS systems (Windows, Linux, etc.)

The `no_commit/` directory is ignored by `git` and can be used to
store temporary CSV files. I use these to create private, personalized
quizzes on my weak areas.

Non-colorized gameplay with comments in `{curly braces}`:
```
$ python play.py
HOW TO PLAY:
  Provide the english meaning for the chinese/pinyin phrase shown.
  Press ENTER by itself (no input) to reprint/restate the phrase.
  Enter a comma (,) character to skip/forfeit a question.
  Enter a question mark (?) character to consult the dictionary.
  Enter a period (.) character to quit gracefully.

1/796:    有点儿    (you3:2 dia3 r)
english meaning: a bit
correct english: a bit of intensity (before adj & northern)   {GREEN TEXT}
[success# = 1, success% = 100]

2/796:    瓶子    (ping2 zi)
english meaning: bottle
correct english: bottle (noun)   {GREEN TEXT}
[success# = 2, success% = 100]

3/796:    报    (bao4)
english meaning: wrong on purpose
correct english: announce/inform/report   {RED TEXT}
[success# = 2, success% = 66]

4/796:    员    (yuan2)
english meaning: ?

員   (yuan2)
  1. person
  2. employee
  3. member


correct english: employee/member   {RED TEXT}
[success# = 2   success% = 50]

5/796:    二    (er4)
english meaning: ,
correct english: 2/two   {RED TEXT}
[success# = 2   success% = 40]

6/796:    住    (zhu4)
english meaning: .

INCORRECTLY ANSWERED:
员,yuan2,employee/member
报,bao4,announce/inform/report
二,er4,2/two


$
```

## Forking
This code is somewhat generic and could apply to other foreign
languages, too. However, it isn't fully modularized and contains
many hardcoded features specific to Chinese languages. Feel free to
fork and modify, but I make no guarantees to functionality or
ease of use for other languages. I haven't tested/tried any of it.

You can customize the CI test runs in the `test_stdin/` directory
by modifying the sequential input files. Follow the general format
described in `Makefile` and `.travis.yml` for easier integration.

## Testing
A GNU Makefile with phony targets is used for testing this codebase.
There are currently three steps:
  * `lint`: Runs `black`, `pylint`, and `bandit`, in that order. This
    reveals any syntax, styling, or security errors with the source code.
  * `run`: Runs the program using various input options and files.
    The default input files should have no failures. Some true negative
    cases are evaluated as well.
  * `clean`: Finds and removes all `*.pyc` files.

You can run `make` or `make all` to run all the testing in series when doing
manual regression testing from the shell. As mentioned earlier in the README,
this is a good idea after first cloning/forking the repository.

## Disclaimer
I am actively learning Mandarin Chinese and consider myself a novice. This
program helps me study. I often discover errors in my CSV files (which I
promptly correct), so these files should not be viewed as authoritative
databases. You can check out the Python `chinese` package or perhaps a
professionally published Chinese dictionary to get the "right" information.
