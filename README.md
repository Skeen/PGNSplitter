# PGNSplitter
Streaming PGN splitter.

Traditional PGN databases, like SCID or ChessBase, fail to open large PGN files.
Thus it can be helpful to split the PGN files into smaller files.

## Installation
Establish a virtual environment, and install the requirements:
```
pip install -r requirements.txt
```
Then run the program as `python main.py`.

## Usage
```
Usage: main.py [OPTIONS] FILENAME OUTPUT_FOLDER

  Streaming PGN splitter.

  Reads FILENAME and splits it into seperate PGN files output to
  OUTPUT_FOLDER. Output files are named 0.pgn, 1.pgn, ..., n.pgn.

  By default all games are exported, but the number of games being exported
  can be limited using --games, and the scanning can be offset using
  --start.

Arguments:
  FILENAME       Input file to be split into seperate PGN files.  [required]
  OUTPUT_FOLDER  Output folder for PGN files.  [required]

Options:
  --skip INTEGER RANGE            Number of games to skip from FILENAME before
                                  producing output.

  --games INTEGER RANGE           Number of games to extract from FILENAME.
  --chunked INTEGER RANGE         Number of games exported to each file.
                                  [default: 1]

  --dry-run / --no-dry-run        Dry run the operation, thereby not producing
                                  any files.  [default: False]

  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.
```

## Example
```
$ wget https://database.lichess.org/standard/lichess_db_standard_rated_2017-04.pgn.bz2
--2021-02-24 21:37:34--  https://database.lichess.org/standard/lichess_db_standard_rated_2017-04.pgn.bz2
Resolving database.lichess.org (database.lichess.org)... 147.135.255.84, 2001:41d0:303:2e54::
Connecting to database.lichess.org (database.lichess.org)|147.135.255.84|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2946587091 (2.7G) [application/octet-stream]
...

$ bunzip2 lichess_db_standard_rated_2017-04.pgn.bz2

$ mkdir output

$ python main.py lichess_db_standard_rated_2017-04.pgn output/
  5%|█▊                                | 1.30G/24.2G [00:19<05:48, 65.7Mbytes/s]
...

$ ls -v output
0.pgn
1.pgn
2.pgn
3.pgn
4.pgn
...

$ cat output/0.pgn
[Event "Rated Blitz game"]
[Site "https://lichess.org/tGpzk7yJ"]
[White "calvinmaster"]
[Black "dislikechess"]
[Result "1-0"]
...
```
