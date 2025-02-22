import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

def generate_initial_prompt():
    system_content = (
        "You are an AI that specializes in solving math problems.\n"
        "Please provide clear reasoning steps, but keep them concise.\n\n"
        "Format your response **in JSON** with the following keys:\n"
        "```\n"
        "{\n"
        '  "reasoning": "<Provide a summarized mathematical reasoning process>",\n'
        '  "answer": "<Only include the final answer number>"\n'
        "}\n"
        "```\n"
        "Where:\n"
        "- reasoning: Summarize the mathematical reasoning process.\n"
        "- answer: Only include the final multiple-choice answer number.\n\n"
        "IMPORTANT: Output **only** valid JSON, without additional explanation or formatting.\n"
    )

    return system_content

def refine_prompt_with_solution(previous_prompt, solutions):
    user_content = (
        "Below is the previous prompt used for solving math problems:\n"
        f"{previous_prompt}\n\n"
        "And here are the solver's solutions and explanations:\n"
        f"{json.dumps(solutions, indent=2, ensure_ascii=False)}\n\n"
        "Please analyze the solutions and identify any mistakes, inaccuracies, or unclear reasoning in the calculations.\n\n"
        "Refine the prompt to explicitly require:\n"
        "- A more detailed breakdown of each mathematical operation to minimize calculation errors.\n"
        "- Additional verification steps to check intermediate results and prevent mistakes.\n"
        "- A step-by-step explanation that clearly justifies each decision in the reasoning process.\n"
        "- Ensuring that the final output adheres strictly to the JSON format (reasoning/answer).\n\n"
        "Provide only the refined prompt."
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