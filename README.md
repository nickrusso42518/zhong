[![Build Status](
https://travis-ci.com/nickrusso42518/zhong.svg?branch=master)](
https://travis-ci.com/nickrusso42518/zhong)

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
```
$ python play.py -q -m
$ python play.py -q   (only works on MacOS)
$ python play.py -m   (only works on MacOS)
```

Gameplay (not colorized) with comments in brackets:
```
$ python play.py -q
HOW TO PLAY:
  Provide the pinyin and english for the chinese phrase shown.
  Unicode values for chinese characters are shown in parenthesis.
  MacOS users can enable narration of the chinese symbols.
  Press ENTER by itself (no input) to reprint/restate the phrase.
  Enter a comma (,) character to skip/forfeit a question.
  Enter a period (.) character to quit; it's invalid input.

1/168:   六十六
Type the pinyin,english: liu4 shi2 liu4,66
pinyin: liu4 shi2 liu4    english: 66/sixty six
[pinyin green, english green]

2/168:   他们
Type the pinyin,english: ta1 de,they
pinyin: ta1 men    english: they (male)
[pinyin red, english green]

3/168:   你的
Type the pinyin,english:
pinyin: ni3 de    english: your
[enter ENTER (black entry) to reprint/replay a question]

3/168:   你的
Type the pinyin,english: ,
pinyin: ni3 de    english: your
[enter comma (,) to skip a question, pinyin and english red]

4/168:   吃
Type the pinyin,english: .
[enter period (.) to gracefully exit]

$
```

## Forking
This code is somewhat generic and could apply to other foreign
languages, too. However, it isn't fully modularized and contains
many hardcoded features specific to Chinese languages. Feel free to
fork and modify, but I make no guarantees to functionality or
ease of use for other languages. I haven't tested/tried any of it.
