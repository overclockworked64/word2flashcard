# word2flashcard

A tool to fetch words from Cambridge Dictionary and make flashcards out of it. Written with Obsidian's Spaced Repetition plugin in mind.

## Installing

Clone the repository, make a Python virtual environment, and install the code using pip. I also suggest symlinking the resulting console script to something like `~/.local/bin`, so that it lives somewhere in your PATH.

## Usage

It reads from stdin, so feed it a word using a Heredoc:

```sh
word2flashcard <<< word
```

or, feed it an entire list of words:

```sh
word2flashcard < words.txt
```

Be nice!