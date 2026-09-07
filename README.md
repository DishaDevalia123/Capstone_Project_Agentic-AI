# A Tutor Agent That Finds Out Why a Student Is Struggling

Disha Devalia — Agentic AI capstone, baseline.

A score tells you a student got 4/10. It does not tell you what they got wrong in their head.
This baseline takes a question, the correct answer, and the student's wrong answer, and asks a
model to name the exact misunderstanding behind it.

This is the weak baseline on purpose. One question, one diagnosis. No memory, no follow-up
questions, no score history.

## Quick start

Python 3.9 or newer. Run these in order from the project folder:

```bash
pip install -r requirements.txt
# now make the .env file, see below
python test_key.py
python run_baseline.py --input examples/test1.txt --answer 11
```

## The .env file

Get a free API key from aistudio.google.com. Make a file called `.env` in the project folder and
put this in it:

```
GEMINI_API_KEY=your_key_here
```

That is the only thing you need. You can also add `MODEL=` to the same file to use a different
model. If you leave it out, it uses `gemini-3-flash-preview`.

`test_key.py` just checks the key works before you run anything else.

## What the run does

The last command is the exact test case from the proposal.

The input is `examples/test1.txt`. It holds the question and the correct answer, split by `---`.
The question is a recursive function `calc(n)` and the right answer is 10. Passing `--answer 11`
pretends to be a student who made an off-by-one mistake.

There is no output file. Everything prints straight to the terminal.

You should get a diagnosis saying the student thinks the recursion goes one step too far and adds an extra 1, giving 11 instead of 10. The wording is written fresh each run and may vary. Either way it comes back as prose with no fixed label, which is one of the problems the project is about.

To get a new question instead of the fixed one:

```bash
python run_baseline.py --concept recursion
```

This makes up a question and asks you to type an answer. The question is different every time, so
use `--input` if you want the same result twice.

## Files

- `run_baseline.py` — the baseline
- `examples/test1.txt` — the fixed question and its answer, split by `---`
- `test_key.py` — checks your API key works
- `requirements.txt` — `openai`, `python-dotenv`

## Things that can go wrong

- The free tier sometimes returns a 503 when it is busy. Run it again, or add `MODEL=` to `.env`
  with a lighter model.
- There is a daily limit on free requests. Fine for a few runs.
- With `--concept`, no two runs give the same question.
