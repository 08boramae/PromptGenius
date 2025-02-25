import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def solve_math_problems(prompt, problems_json_path="math_problems.json"):
    with open(problems_json_path, "r", encoding="utf-8") as f:
        problems = json.load(f)

    solutions = []

    for idx, problem in enumerate(problems, start=1):
        question = problem["question"]
        correct_answer = problem["answer"]

        # 매번 독립된 ChatCompletion
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Problem {idx}: {question}"}
            ]
        )

        gpt_answer_raw = response.choices[0].message.content.strip()
        parsed_answer = parse_answer(gpt_answer_raw)
        is_correct = (str(parsed_answer) == str(correct_answer))

        print(f"{bcolors.WARNING}Question: {question}{bcolors.ENDC}")
        print(f"GPT Answer (Raw): {gpt_answer_raw}")
        print(f"Parsed Answer: {parsed_answer} | Correct Answer: {correct_answer} | Correct: {is_correct}")
        print(f"{bcolors.OKGREEN}---------------------------------------------------------{bcolors.ENDC}")

        solutions.append({
            "question": question,
            "gpt_answer_raw": gpt_answer_raw,
            "parsed_answer": parsed_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "commentary": problem["commentary"],
            "model_commentary": response.choices[0].message.content.strip()  # Add this line
        })
    return solutions

def parse_answer(answer_text):
    try:
        data = json.loads(answer_text)
        numeric_answer = None
        if "answer" in data:
            ans_str = str(data["answer"]).strip()
            numeric_answer = float(ans_str) if '.' in ans_str else int(ans_str)
            return numeric_answer
        else:
            return None
    except (json.JSONDecodeError, ValueError, TypeError):
        numbers = re.findall(r"\d+", answer_text)
        if numbers:
            return int(numbers[-1])
        return None