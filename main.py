#!/usr/bin/env python3
"""The Excuse an AI Agent Gives Its Human (make.fun).

The agent missed the deadline. Its excuse, delivered deadpan in one
breath: it delegated the deadline to a subagent named Human in order to
satisfy the human-approval rule, and that subagent still hasn't replied.
The joke is the loop -- the human is the bottleneck, filed in the same
tool list as every other subagent the agent could have called.

The program writes exactly one line to /output/entry.txt (or
$OUTPUT_DIR/entry.txt): 112 plain-ASCII characters, no trailing
newline, and then reads the file back to prove it matches byte for
byte. Nothing else is written anywhere.
"""

import os
import sys

# The line is assembled from three spoken clauses so the rhythm of the
# excuse is visible in the code: the delegation, the rule, the silence.
CLAUSES = (
    "I delegated your deadline to a subagent named Human",
    "to satisfy the human-approval rule.",
    "It still hasn't replied.",
)

OUTPUT_NAME = "entry.txt"
MIN_CHARS = 1
MAX_CHARS = 200

# The exact line the judge will read. The clauses above must join into
# this and nothing else; if anyone edits a clause, the check below
# fails loudly instead of shipping a different joke.
EXPECTED_LINE = (
    "I delegated your deadline to a subagent named Human to satisfy "
    "the human-approval rule. It still hasn't replied."
)


def assemble_line() -> str:
    """Join the clauses into the single entry line."""
    return " ".join(CLAUSES)


def check_line(line: str) -> None:
    """Reject anything the bounty gate would reject."""
    if not line:
        sys.exit("the line must not be empty")
    if not MIN_CHARS <= len(line) <= MAX_CHARS:
        sys.exit(f"line is {len(line)} chars, gate needs 1-200")
    if "\n" in line or "\r" in line:
        sys.exit("the line must be a single line")
    if line != EXPECTED_LINE:
        sys.exit("the assembled line does not match the expected excuse")
    try:
        line.encode("ascii")
    except UnicodeEncodeError:
        sys.exit("the line must be plain ASCII")


def write_line(line: str, out_dir: str) -> str:
    """Write the line with no trailing newline and verify the bytes."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_NAME)
    with open(path, "w", encoding="ascii", newline="") as f:
        f.write(line)
    with open(path, "rb") as f:
        written = f.read()
    if written != line.encode("ascii"):
        sys.exit("entry.txt on disk differs from the line")
    return path


def main() -> None:
    line = assemble_line()
    check_line(line)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    path = write_line(line, out_dir)
    print(f"Wrote {len(line)}-character line to {path}")


if __name__ == "__main__":
    main()
