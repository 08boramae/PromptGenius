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
    # 1) Generate initial prompt
    initial_prompt = generate_initial_prompt()
    print(f"{bcolors.OKCYAN}=== [1] Initial Prompt ==={bcolors.ENDC}")
    print(initial_prompt)
    print()

    # 2) Solve math problems with the initial prompt
    solutions = solve_math_problems(prompt=initial_prompt, problems_json_path="math_problems.json")
    print(f"{bcolors.OKCYAN}=== [2] Math Problem Solutions ==={bcolors.ENDC}")
    for sol in solutions:
        print(f"{bcolors.WARNING}Question: {sol['question']}{bcolors.ENDC}")
        print(f"GPT Answer (Raw): {sol['gpt_answer_raw']}")
        print(f"Parsed Answer: {sol['parsed_answer']} | Correct Answer: {sol['correct_answer']} | Correct: {sol['is_correct']}")
        print(f"{bcolors.OKGREEN}---------------------------------------------------------{bcolors.ENDC}")

    # 3) Refine the prompt based on the solutions
    refined_prompt = refine_prompt_with_solution(initial_prompt, solutions)
    print(f"{bcolors.OKCYAN}\n=== [3] Refined Prompt ==={bcolors.ENDC}")
    print(refined_prompt)
    print()

    # 4) Repeat 10 times: solve problems with the refined prompt and refine the prompt again
    for i in range(1, 11):
        print(f"{bcolors.OKCYAN}=== Iteration {i} ==={bcolors.ENDC}")
        solutions_iter = solve_math_problems(prompt=refined_prompt, problems_json_path="math_problems.json")

        print(f"{bcolors.OKCYAN}=== [Iteration {i} Solutions] ==={bcolors.ENDC}")
        for sol in solutions_iter:
            print(f"{bcolors.WARNING}Question: {sol['question']}{bcolors.ENDC}")
            print(f"GPT Answer (Raw): {sol['gpt_answer_raw']}")
            print(f"Parsed Answer: {sol['parsed_answer']} | Correct Answer: {sol['correct_answer']} | Correct: {sol['is_correct']}")
            print(f"{bcolors.OKGREEN}---------------------------------------------------------{bcolors.ENDC}")

        refined_prompt = refine_prompt_with_solution(refined_prompt, solutions_iter)
        print(f"{bcolors.OKCYAN}\n=== [Iteration {i} Refined Prompt] ==={bcolors.ENDC}")
        print(refined_prompt)
        print()

if __name__ == "__main__":
    main()