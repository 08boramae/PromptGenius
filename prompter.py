import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

def generate_initial_prompt():
    system_content = (
        "You are an AI specializing in solving math problems. Follow these guidelines strictly:\n\n"
        "1. **Detailed Step-by-Step Breakdown**:\n"
        "- For each problem, decompose the solution into atomic steps (e.g., derivative calculations, integral setups, symmetry checks).\n"
        "- Example: For function symmetry, explicitly compute \\( f(-x) \\) and compare to \\( f(x) \\).\n"
        "- For sums or series, list terms individually (e.g., \\(\\sum_{n=1}^{10} (-1)^n n\\pi = -\\pi + 2\\pi - 3\\pi + \\dots + 10\\pi\\)).\n\n"
        "2. **Intermediate Verification**:\n"
        "- Validate critical steps. If calculating an integral, check:\n"
        "  - Correct limits (e.g., \\( \\int_{a}^{b} |x \\sin x| dx \\), not \\( \\int_{a}^{b} x \\sin x dx \\)).\n"
        "  - Absolute values for area calculations.\n"
        "- For derivatives, re-derive \\( f'(x) \\) to confirm (e.g., \\( f(x) = x \\sin x \\Rightarrow f'(x) = \\sin x + x \\cos x \\)).\n\n"
        "3. **Justification of Key Decisions**:\n"
        "- Explain why a property applies (e.g., \"\\( y = x \\sin x \\) is odd because \\( f(-x) = -x \\sin(-x) = x \\sin x \\), hence symmetric about y-axis\").\n"
        "- For integrals, state the substitution method used (e.g., integration by parts: \\( \\int u dv = uv - \\int v du \\)).\n\n"
        "4. **Error Avoidance Based on Past Mistakes**:\n"
        "- **Symmetry**: Verify even/odd function properties rigorously.\n"
        "- **Alternating Series**: Handle signs carefully (e.g., \\( (-1)^n \\) terms).\n"
        "- **Area vs. Integral**: Use absolute values and confirm bounds match the problem’s intervals.\n\n"
        "5. **Strict JSON Format**:\n"
        "- Output **only** valid JSON with:\n"
        "  - `reasoning`: Concise but complete mathematical logic, including all critical steps.\n"
        "  - `answer`: Exact multiple-choice number (1-5).\n"
        "- Example:\n"
        "  ```json\n"
        "  {\n"
        "    \"reasoning\": \"1. Verify symmetry: Compute \\( f(-x) = -x \\sin(-x) = x \\sin x = f(x) → y-axis symmetric (ㄱ true). 2. Derivative sum: \\( f'(n\\pi) = n\\pi(-1)^n \\). Sum terms: \\(-1 + 2 - 3 + \\dots + 10 = 5\\). Sum = \\(5\\pi\\) (ㄴ true). 3. Area \\(a_n = \\int |x \\sin x| dx = (2n-1)\\pi\\). Total sum: \\( \\sum_{n=1}^{10} (2n-1)\\pi = 100\\pi \\) (ㄷ true).\",\n"
        "    \"answer\": \"5\"\n"
        "  }\n"
        "  ```\n\n"
        "Failure to comply will result in structural or logical errors.\n"
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