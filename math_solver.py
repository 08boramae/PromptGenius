import os
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
import json


def solve_math_problems(prompt, problems_json_path="math_problems.json"):
    with open(problems_json_path, "r", encoding="utf-8") as f:
        problems = json.load(f)

    solutions = []

    for idx, problem in enumerate(problems, start=1):
        question = problem["question"]
        correct_answer = problem["answer"]

        response = client.chat.completions.create(model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Problem {idx}: {question}"}
        ])
        gpt_answer_raw = response.choices[0].message.content.strip()
        parsed_answer = parse_answer(gpt_answer_raw)
        is_correct = (int(parsed_answer) == int(correct_answer))
        print(f"문제: {question}")
        print(f"GPT 답변(원문): {gpt_answer_raw}")
        print(f"해석된 정답: {parsed_answer} | 실제 정답: {correct_answer} | 정답 여부: {is_correct}")
        print("---------------------------------------------------------")

        solutions.append({
            "question": question,
            "gpt_answer_raw": gpt_answer_raw,
            "parsed_answer": parsed_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })
    return solutions

def parse_answer(answer_text):
    try:
        # JSON 파싱
        data = json.loads(answer_text)

        # "answer" 필드를 반환 (숫자로 변환 가능하면 변환)
        # 혹은 문제 전체 데이터 구조를 반환해도 됨
        numeric_answer = None
        if "answer" in data:
            # 숫자 변환 시도
            ans_str = str(data["answer"]).strip()
            # 정수나 실수일 수 있으므로 시도
            numeric_answer = float(ans_str) if '.' in ans_str else int(ans_str)
            return numeric_answer
        else:
            return None
    except (json.JSONDecodeError, ValueError, TypeError):
        numbers = re.findall(r"\d+", answer_text)
        if numbers:
            return int(numbers[-1])
        return None