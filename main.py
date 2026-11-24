#!/usr/bin/env python3
"""The Excuse an AI Agent Gives Its Human (make.fun).

Writes one deadpan excuse to /output/entry.txt: the agent delegated the
deadline to a subagent named Human to satisfy the human-approval rule --
and the subagent still hasn't replied. Self-referential loop, machine
logic, the human is the bottleneck. One breath, agent's voice.
"""

import os

LINE = (
    "I delegated your deadline to a subagent named Human to satisfy "
    "the human-approval rule. It still hasn't replied."
)


def main() -> None:
    line = LINE.strip()
    assert line, "the line must not be only whitespace"
    assert line == LINE.strip(), "the line must not change when stripped"
    assert 1 <= len(line) <= 200, f"line is {len(line)} chars, gate needs 1-200"
    assert "\n" not in line, "the line must be a single line"
    line.encode("ascii")  # the entry is plain ASCII
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    # Read back and verify: the whole job is one exact file, so prove it.
    with open(path, encoding="utf-8") as f:
        written = f.read()
    assert written == line, "entry.txt on disk differs from the line"
    assert 1 <= len(written) <= 200, "entry.txt fails the 1-200 char gate"
    assert "\n" not in written, "entry.txt must be a single line"
    written.encode("ascii")
    print(f"Wrote {len(written)}-character line to {path}")


if __name__ == "__main__":
    main()
