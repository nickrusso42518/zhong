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
usage: play.py [-h] [-m] [-q] [-r RATE] [-i INFILE]

optional arguments:
  -h, --help            show this help message and exit
  -m, --mask            disable easy reading of chinese symbols (MacOS only)
  -q, --quiet           disable audio narration of chinese symbols (MacOS only)
  -r RATE, --rate RATE  adjust rate of speech in words per minute (90 to 300)
  -i INFILE, --infile INFILE
                        input file in CSV format (chinese,pinyin,english)
```

Check the `inputs/` directory for sample CSV files. Be warned; these
are frequently updated.

## Advanced Usage
Detailed explanation:
  * `-i`: Pass in a CSV import file. The file must contain exactly 3 columns:
          chinese,pinyin,english. You can check the `all.csv` file for an
          example of proper formatting. The file may include comments beginning
          with the `#` symbol, just like Python or YAML.  Defaults to `all.csv`
          which is my current (and constantly growing) general-purpose list.

  * `-q`: Enable quiet mode. This disables audio narration of the Chinese
          symbols. Learners must rely entirely on sight. The game will
          run faster as well. Note that audio narration is only available
          on MacOS, so Windows and Linux users are always in quiet mode.

  * `-m`: Enable mask mode. This prints Chinese symbols with a black foreground
          and background color. This effectively masks the Chinese
          symbols, forcing a learner to rely only on the audio narration. For
          that reason, this option is only available to MacOS users. Using
          the mouse, you can highlight the Chinese symbols to reveal them if
          you need a hint; this technique should be used sparingly.

  * `-r`: The MacOS `say` command supports a range of narration rates,
          depending on the language spoken. The slowest (easiest) is 90
          words per minute, the fastest (hardest) is 300, and the default
          (most natural) is 180.

Example usages of minor options:
```
$ python play.py
$ python play.py -i inputs/tp.csv
$ python play.py -m
$ python play.py -m -i inputs/tp.csv
$ python play.py -m -r 120
$ python play.py -m -r 120 -i inputs/tp.csv
$ python play.py -r 120
$ python play.py -q
$ python play.py -q -i inputs/tp.csv
```

Invalid usages:
  * `python play.py -q -m`: Combination is never valid. Program
    exits with return code 2 and an informative error message
  * `$ python play.py -i inputs/nonexist.csv`: If a nonexistent file
    is supplied, the program exits with return code 3 and the corresponding
    `FileNotFoundError` message.
  * `$ python play.py -q`: Technically accepted on any platform,
    but `-q` has no effect on non-MacOS systems (Windows, Linux, etc.)
  * `$ python play.py -m`: Technically accepted on any platform,
    but `-m` has no effect on non-MacOS systems (Windows, Linux, etc.)

The `no_commit/` directory is ignored by `git` and can be used to
store temporary CSV files. I use these to create private, personalized
quizzes on my weak areas.

Gameplay (not colorized) with comments in brackets:
```
$ python play.py 
HOW TO PLAY:
  Provide the english meaning for the chinese/pinyin phrase shown.
  Press ENTER by itself (no input) to reprint/restate the phrase.
  Enter a comma (,) character to skip/forfeit a question.
  Enter a period (.) character to quit gracefully.

1/451:    末    (mo4)
english meaning: end
correct english: end  [green]

2/451:    中文    (zhong1 wen2)
english meaning: chinese language
correct english: chinese language  [green]

3/451:    星期    (xing1 qi1)
english meaning: wrong on purpose
correct english: week day specifier  [red]

4/451:    一共    (yi1 gong4)
english meaning: 

4/451:    一共    (yi1 gong4)
english meaning: ,
correct english: altogether/in total  [red]

5/451:    电    (dian4)
english meaning: .


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
