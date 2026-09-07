"""
Baseline: one-shot misconception diagnosis.

Loads or generates a question, takes the student's answer, asks the
model what misconception produced it. No loop, no memory, no score
history. That's the point.

Two modes:
  --concept recursion            generate a fresh question (normal use)
  --input examples/test1.txt     use a fixed question (reproduces the
                                 test case in the proposal)
"""

import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = os.getenv("MODEL", "gemini-3-flash-preview")

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


def ask_model(prompt: str, system: str = "You are a helpful assistant.") -> str:
    """One call. Returns the text of the reply."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


def load_question(path: str):
    """Read a fixed question from a file: question, then ---, then answer."""
    with open(path, encoding="utf-8") as f:
        question, answer = f.read().split("---")
    return question.strip(), answer.strip()


def generate_question(concept: str):
    reply = ask_model(
        f"Write one short-answer question about {concept} in Python. "
        f"The question must include a short code snippet (5 lines or fewer) "
        f"and ask what it returns or prints for a specific input. "
        f"It must have a single short answer, like a number or a word. "
        f"Do not ask for a definition or the name of an exception. "
        f"Reply with the question, then ---, then the correct answer. Nothing else."
    )
    question, answer = reply.split("---")
    return question.strip(), answer.strip()


def diagnose(concept, question, correct_answer, student_answer):
    reply = ask_model(
        f"A student is learning {concept} in Python.\n\n"
        f"Question asked: {question}\n"
        f"Correct answer: {correct_answer}\n"
        f"Student answered: {student_answer}\n\n"
        f"Name the one specific misunderstanding that would most likely "
        f"produce this exact wrong answer. Be specific - do not say the "
        f"student is confused about {concept} in general. Then explain in "
        f"two or three sentences why that misunderstanding leads to this answer."
    )
    return reply


def main():
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--concept", help="generate a fresh question, e.g. recursion")
    source.add_argument("--input", help="use a fixed question file, e.g. examples/test1.txt")
    parser.add_argument("--answer", help="student answer; if omitted, you are prompted")
    args = parser.parse_args()

    if args.input:
        question, correct_answer = load_question(args.input)
        concept = "recursion"
    else:
        question, correct_answer = generate_question(args.concept)
        concept = args.concept

    print(f"\nQuestion: {question}\n")

    if args.answer:
        student_answer = args.answer
        print(f"Your answer: {student_answer}")
    else:
        student_answer = input("Your answer: ").strip()

    print("\nThinking...\n")
    print(diagnose(concept, question, correct_answer, student_answer))


if __name__ == "__main__":
    main()