class Judge_Prompt(object):
    judge_prompt = '''### System A:
{system_A}

### System B:
{system_B}

### Evaluation Factors:
1. User-friendliness: Evaluate which system's response is easier to understand and more relatable.
2. Clarity: Determine which system's response is more straightforward and easy to understand, using simple language, concise explanations.
3. Usefulness of Information: Assess which system's response provides more practical and relevant information that aids in decision-making and is actionable.
4. Uniqueness of Explanation: Evaluate the uniqueness of each system's recommendation explanations, giving higher ratings to those that provide particularly distinctive and non-universal explanations.
5. Innovativeness: Judge which system introduces more creative ideas or perspectives that enhance the user experience.

### Instruction:
You are an impartial judge with a professional level of knowledge about movies. System A and System B have each provided explanations for why user YM_289 received a movie recommendation for Nightmare on Elm Street 4, A - The Dream Master.
For each system, your goal is to determine which one performs better for each of the five evaluation factors listed above. Conclude which system is superior overall.
Provide your responses in the following format, where 'A' indicates System A is better, 'B' indicates System B is better, 'T' indicates that both systems A and B are similar, resulting in a draw. (Example 1: ['T', 'B', 'A', 'T', 'B'], Example 2: ['B', 'A', 'B', 'A', 'B'], Example 3: ['B', 'T', 'B', 'B', A], Example 4: ['A', 'B', 'T', 'B', 'T'])

Your response must be formatted as JSON:
{{
    "Reasons": "Brief reasons for the judgment",
    "Answer": [results]
}}

Let's think step by step!

### Response:
'''