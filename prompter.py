import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

APIKEY = os.getenv("OPENAI_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

def generate_initial_prompt():
    system_content = (
        "You are an AI that specializes in solving math problems.\n"
        "Please provide clear reasoning steps, but keep them concise.\n\n"
        "Format your response **in JSON** with the following keys:\n"
        "```\n"
        "{\n"
        '  "reasoning": "<문제 풀이 과정>",\n'
        '  "answer": "<최종 정답 번호만 기재>"\n'
        "}\n"
        "```\n"
        "Where:\n"
        "- reasoning: 수학적 사고 과정을 요약하여 적어주세요\n"
        "- answer: 최종 객관식 정답 번호만 기재해주세요.\n\n"
        "IMPORTANT: Output **only** valid JSON, without additional explanation or formatting.\n"
    )

    return system_content

def refine_prompt_with_solution(previous_prompt, solutions):
    user_content = (
        "Below is the previous prompt used for solving math problems:\n"
        f"{previous_prompt}\n\n"
        "And here are the solver's solutions and explanations:\n"
        f"{json.dumps(solutions, indent=2)}\n\n"
        "Please suggest how we can refine or improve the prompt to get better or more accurate explanations.\n\n"
        "Remember to preserve the JSON format instruction (problem/reasoning/answer)."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a prompt engineering expert."},
            {"role": "user", "content": user_content}
        ]
    )

    improved_prompt = response.choices[0].message.content
    return improved_prompt