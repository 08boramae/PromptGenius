from prompter import generate_initial_prompt, refine_prompt_with_solution
from math_solver import solve_math_problems

def main():
    # 1) 초기 프롬프트 생성
    initial_prompt = generate_initial_prompt()
    print("=== [1] 초기 프롬프트 ===")
    print(initial_prompt)
    print()

    # 2) 해당 프롬프트로 수학 문제 풀이
    solutions = solve_math_problems(prompt=initial_prompt, problems_json_path="math_problems.json")
    print("=== [2] 수학 문제 풀이 결과 ===")
    for sol in solutions:
        print(f"문제: {sol['question']}")
        print(f"GPT 답변(원문): {sol['gpt_answer_raw']}")
        print(f"해석된 정답: {sol['parsed_answer']} | 실제 정답: {sol['correct_answer']} | 정답 여부: {sol['is_correct']}")
        print("---------------------------------------------------------")

    # 3) 풀이 결과/해설을 바탕으로 프롬프트 개선
    refined_prompt = refine_prompt_with_solution(initial_prompt, solutions)
    print("\n=== [3] 개선된 프롬프트 ===")
    print(refined_prompt)
    print()

    # 4) 아래부터 10번 반복: 새로운 프롬프트(refined_prompt)로 다시 문제를 풀고,
    #    그 결과를 바탕으로 프롬프트를 또 개선한다.
    for i in range(1, 11):
        print(f"=== 반복 {i}차 ===")
        # 개선된 프롬프트로 다시 수학문제 풀이
        solutions_iter = solve_math_problems(prompt=refined_prompt, problems_json_path="math_problems.json")

        print(f"=== [반복 {i}차 풀이 결과] ===")
        for sol in solutions_iter:
            print(f"문제: {sol['question']}")
            print(f"GPT 답변(원문): {sol['gpt_answer_raw']}")
            print(f"해석된 정답: {sol['parsed_answer']} | 실제 정답: {sol['correct_answer']} | 정답 여부: {sol['is_correct']}")
            print("---------------------------------------------------------")

        # 다시 프롬프트를 개선
        refined_prompt = refine_prompt_with_solution(refined_prompt, solutions_iter)
        print(f"\n=== [반복 {i}차 개선된 프롬프트] ===")
        print(refined_prompt)
        print()

if __name__ == "__main__":
    main()