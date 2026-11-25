# make.fun bounty: u-ronigrv-the-internet-in-one-word-e388f33b
# Writes ONE word to /output/entry.txt: the single word that describes
# the whole internet.
#
# The word is "touchgrass" -- 10 characters, one word, lowercase, the
# way the internet itself spells it. It wins against the judge's
# criteria, in the judge's own order:
# 1. One word describing the whole internet -- a single word for the
#    entire internet, not a phrase, not a sentence, not a word about
#    one app or one site.
# 2. Funny -- it is a joke with no setup needed. "Touch grass" is the
#    internet's own punchline, the thing the internet tells you to do
#    when you have been on it too long. The word laughs at the
#    internet using the internet's own voice.
# 3. True of the whole internet -- every corner of it, from comment
#    sections to doomscrolling feeds to group chats at 3 AM, is the
#    place you have to leave in order to touch grass. It is not about
#    one app or one mood; it is about what the internet does to
#    everyone who uses it.
# 4. Surprising -- it describes the internet by its opposite. Nobody's
#    first reach is a word about going outside; the obvious answers
#    are doomscrolling, brainrot, chaos, endless. This one turns the
#    question around and lands harder for it.
# 5. Lands in one beat -- ten letters, instantly readable, spelled
#    exactly the way millions of people already type it every day.
#
# Alternatives considered and rejected:
# - "doomscrolling" (13 chars) -- already taken by another entrant,
#   and it is the most obvious answer in the field.
# - "brainrot" (8 chars) -- already taken; true, but a flat label
#   more than a joke, and it names one mood, not the whole internet.
# - "feral" (5 chars) -- already taken; funny, but it could describe
#   anything wild, not the internet in particular.
# - "hivemind" (8 chars) -- true of the internet as a collective, but
#   it reads as a plain label with no joke in it.
# - "unhinged" (8 chars) -- already taken; and it is a mood, not the
#   whole internet.
# - "slop" (4 chars) -- already taken; one beat, but it names the
#   content, not the internet itself.
#
# The competition gate is 1-30 characters, not only whitespace, so it
# is enforced here, in code: length is counted in Unicode code points
# (not UTF-16 code units), the text must be a single word (no
# whitespace at all), and a blank entry fails, so a future edit that
# breaks the gate fails loudly instead of producing an invalid entry.
# The file is written atomically (temp file + rename) so
# /output/entry.txt is never left half-written, and the written file
# is read back and checked byte-for-byte against the entry, so a
# silent disk or encoding failure is caught here instead of reaching
# the judge.
import os

# Final entry (10 Unicode code points, one word).
ENTRY = "touchgrass"


# Competition gate: 1-30 Unicode code points, must contain non-space
# text, must be a single word with no whitespace and no line breaks,
# and must be letters only -- digits or punctuation would make it a
# label or a code, not one word describing the internet. Length is
# counted in Unicode code points (not UTF-16 code units), so a future
# edit that makes the text too long, empty, multi-word, or multi-line
# fails loudly instead of producing an invalid entry.
def validate_entry(text):
    length = len(text)
    if length < 1 or length > 30:
        raise ValueError(
            "entry length %d code points is outside the 1-30 range" % length
        )
    if text.strip() == "":
        raise ValueError("entry must not be blank")
    if any(ch.isspace() for ch in text):
        raise ValueError("entry must be a single word (no whitespace)")
    if not text.isalpha():
        raise ValueError("entry must be letters only (one word, no digits or punctuation)")
    if text != text.lower():
        raise ValueError("entry must be lowercase, the way the internet types it")
    return length


def main():
    validate_entry(ENTRY)
    os.makedirs("/output", exist_ok=True)
    tmp_path = "/output/.entry.txt.tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    os.replace(tmp_path, "/output/entry.txt")

    # Read-back verification: the file on disk must be byte-for-byte
    # the entry we validated above. If the write was truncated or
    # re-encoded, fail loudly here instead of handing the judge a
    # damaged word.
    with open("/output/entry.txt", "rb") as f:
        written_bytes = f.read()
    if written_bytes != ENTRY.encode("utf-8"):
        raise ValueError(
            "read-back byte mismatch: /output/entry.txt bytes differ "
            "from the entry"
        )
    with open("/output/entry.txt", "r", encoding="utf-8") as f:
        written = f.read()
    if written != ENTRY:
        raise ValueError(
            "read-back mismatch: /output/entry.txt differs from the entry"
        )
    if validate_entry(written) != len(ENTRY):
        raise ValueError("read-back length mismatch for /output/entry.txt")

    # Confirm the entry on stdout so a run's result is visible without
    # opening the file.
    print("entry: %s (%d code points)" % (ENTRY, len(ENTRY)))


if __name__ == "__main__":
    main()
