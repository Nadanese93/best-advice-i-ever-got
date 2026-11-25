"""Write the Best Advice entry to $MAKEFUN_OUTPUT_DIR/entry.txt.

Deterministic, stdlib only: no clock, no random, no network.
Reads only the MAKEFUN_OUTPUT_DIR environment variable.
"""

import os

ENTRY_TEXT = (
    "My father, a plumber, told me the leak you ignore is the one "
    "that rots the floor, so fix the small drip before it eats the house."
)


class BlankError(ValueError):
    """Raised when the entry text is empty or only whitespace."""


class MultiLineError(ValueError):
    """Raised when the entry text contains a line break."""


class LengthError(ValueError):
    """Raised when the entry text is outside 1-200 characters."""


class VerificationError(RuntimeError):
    """Raised when entry.txt on disk does not match ENTRY_TEXT bytes."""


def validate(text):
    if not text or not text.strip():
        raise BlankError("entry text is blank")
    if "\n" in text or "\r" in text:
        raise MultiLineError("entry text must be a single line")
    if len(text) < 1 or len(text) > 200:
        raise LengthError(
            "entry text must be 1-200 characters, got %d" % len(text)
        )
    # One sentence: exactly one sentence-ending mark, at the end.
    terminators = sum(text.count(mark) for mark in ".!?")
    if terminators != 1 or not text.rstrip().endswith((".", "!", "?")):
        raise ValueError("entry text must be exactly one sentence")


def verify_written(path, expected_text):
    """Re-read entry.txt and raise unless its bytes equal expected_text."""
    with open(path, "rb") as handle:
        actual = handle.read()
    expected = expected_text.encode("utf-8")
    if actual != expected:
        raise VerificationError(
            "entry.txt mismatch: wrote %d bytes, read back %d bytes"
            % (len(expected), len(actual))
        )


def main():
    validate(ENTRY_TEXT)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY_TEXT)
    verify_written(path, ENTRY_TEXT)


if __name__ == "__main__":
    main()
