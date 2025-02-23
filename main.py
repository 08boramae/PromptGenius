import os
import json
from prompter import generate_initial_prompt, refine_prompt_with_solution
from math_solver import solve_math_problems

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

def main():
    # 1. 초기 Prompt 생성
    prompt = generate_initial_prompt()
    print(f"{bcolors.OKCYAN}=== [1] Initial Prompt ==={bcolors.ENDC}")
    print(prompt)
    print()

    # 2. 10번 반복: 문제 풀이 -> refine
    for i in range(1, 11):
        print(f"{bcolors.OKCYAN}=== Iteration {i} ==={bcolors.ENDC}")

        # (a) 문제 풀기 (이때 'prompt'만 사용; 이전 대화 없음)
        solutions = solve_math_problems(
            prompt=prompt,  # <-- 이전 맥락 없이, prompt만 넘김
            problems_json_path="math_problems.json"
        )

        # 결과 출력
        print(f"{bcolors.OKCYAN}=== [Iteration {i} Solutions] ==={bcolors.ENDC}")
        for sol in solutions:
            print(f"{bcolors.WARNING}Question: {sol['question']}{bcolors.ENDC}")
            print(f"GPT Answer (Raw): {sol['gpt_answer_raw']}")
            print(f"Parsed Answer: {sol['parsed_answer']} | Correct Answer: {sol['correct_answer']} | Correct: {sol['is_correct']}")
            print(f"{bcolors.OKGREEN}---------------------------------------------------------{bcolors.ENDC}")

        # (b) prompt refine
        prompt = refine_prompt_with_solution(
            previous_prompt=prompt,
            solutions=solutions
        )
        print(f"{bcolors.OKCYAN}=== [Iteration {i} Refined Prompt] ==={bcolors.ENDC}")
        print(prompt)
        print()

if __name__ == "__main__":
    main()