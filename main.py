from itertools import islice
from os.path import getsize
from pathlib import Path
from typing import Iterator, Optional

import typer
from chess.pgn import skip_game
from more_itertools import consume, ichunked, pairwise
from tqdm import tqdm


def find_byte_boundaries(filename: Path) -> Iterator[int]:
    """Generator of byte offsets for the start and end of each PGN."""
    yield 0
    with open(filename, "r") as pgn:
        while skip_game(pgn):
            yield pgn.tell()
        yield pgn.tell()


def _tqdm_boundaries(filename: Path, it: Iterator[int]) -> Iterator[int]:
    """Apply tqdm to the provided iterator."""
    byte_length: int = getsize(filename)
    pbar = tqdm(total=byte_length, unit="bytes", unit_scale=True)

    for new_position in it:
        # pbar.update expects a relative update, not an absolute
        difference: int = new_position - pbar.n
        pbar.update(difference)

        yield new_position


def split_file(filename: Path, seperators: Iterator[int]) -> Iterator[bytes]:
    """Generator of bytes, blocks correspond to PGN."""
    with open(filename, "rb") as pgn:
        for start, end in pairwise(seperators):
            difference: int = end - start
            pgn.seek(start)
            yield pgn.read(difference)


def split(
    skip: Optional[int] = typer.Option(
        default=None,
        min=0,
        help="Number of games to skip from FILENAME before producing output.",
    ),
    games: Optional[int] = typer.Option(
        default=None, min=0, help="Number of games to extract from FILENAME."
    ),
    chunked: int = typer.Option(
        default=1, min=1, help="Number of games exported to each file."
    ),
    filename: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="Input file to be split into seperate PGN files.",
    ),
    output_folder: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        help="Output folder for PGN files.",
    ),
    dry_run: bool = typer.Option(
        default=False, help="Dry run the operation, thereby not producing any files."
    ),
):
    """Streaming PGN splitter.

    Reads FILENAME and splits it into seperate PGN files output to OUTPUT_FOLDER.
    Output files are named 0.pgn, 1.pgn, ..., n.pgn.

    By default all games are exported, but the number of games being exported can
    be limited using --games, and the scanning can be offset using --start.
    """
    # Find byte offsets for splits between PGNs
    seperators: Iterator[int] = find_byte_boundaries(filename)
    # Offset by skipping 'skip' PGNs
    if skip:
        consume(seperators, skip)

    if games is None:
        seperators = _tqdm_boundaries(filename, seperators)
    else:
        seperators = islice(seperators, games + 1)

    blocks = split_file(filename, seperators)
    if games:
        blocks = tqdm(blocks, total=games, unit="games")

    chunks = ichunked(blocks, chunked)

    for i, chunk in enumerate(chunks):
        if dry_run:
            continue
        with open(f"{output_folder}/{str(i)}.pgn", "wb") as pgn:
            for block in chunk:
                pgn.write(block)


if __name__ == "__main__":
    typer.run(split)
