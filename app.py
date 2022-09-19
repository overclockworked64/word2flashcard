from pathlib import Path
import sys

import asks
import bs4
import trio
import trio_parallel


MAX_TASKS_IN_FLIGHT = 200
CAMBRIDGE_URL = "https://dictionary.cambridge.org/dictionary/english/"
VAULT_PATH = (
    Path().home()
    / "Documents"
    / "dbase"
    / "dbase"
    / "languages"
    / "english"
    / "wordlists"
)
USER_AGENT = (
    "curl/7.16.3 (i686-pc-cygwin) "
    + "libcurl/7.16.3 "
    + "OpenSSL/0.9.8h "
    + "zlib/1.2.3 "
    + "libssh2/0.15-CVS"
)


def extract_info(block):
    meaning = block.find("div", {"class": "ddef_h"})
    example = block.find("div", {"class": "examp"})
    return meaning, example


def sync_worker(word, page):
    soup = bs4.BeautifulSoup(page, "lxml")

    # find all definition blocks
    definition_blocks = soup.find_all("div", {"class": "def-block"})

    # create a new file, extract info from the blocks and write it
    with open(VAULT_PATH / word[0].upper() / f"{word}.md", "w") as f:
        f.write(word + "\n?\n")
        for block in definition_blocks:
            meaning, example = extract_info(block)
            if meaning is not None:
                f.write("- " + meaning.text.strip() + "\n")
            if example is not None:
                f.write("example: " + example.text + "\n")


async def micrograbber(tx, limiter, word):
    async with limiter:
        page = await asks.get(CAMBRIDGE_URL + word, headers={"User-Agent": USER_AGENT})
    await tx.send((word, page.text))


async def receiver(nursery, rx, words):
    async for (word, page) in rx:
        nursery.start_soon(trio_parallel.run_sync, sync_worker, word, page)
        words.remove(word)
        if not words:
            break


async def amain(words):
    limiter = trio.CapacityLimiter(MAX_TASKS_IN_FLIGHT)
    tx, rx = trio.open_memory_channel(0)
    async with trio.open_nursery() as nursery:
        nursery.start_soon(receiver, nursery, rx, words)
        for word in words:
            nursery.start_soon(micrograbber, tx.clone(), limiter, word)


def sync_main():
    words = list(
        filter(
            lambda x: x,
            map(
                str.strip,
                sys.stdin.readlines(),
            ),
        )
    )
    trio.run(amain, words)


if __name__ == "__main__":
    sync_main()
