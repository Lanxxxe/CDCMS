from google import genai
from google.genai import types
from decouple import config

def mask_email(email):
    """Mask the email to show only the first 3 letters and domain."""
    if "@" in email:
        name, domain = email.split("@")
        masked_name = name[:2] + "*" * (len(name) - 2)
        return f"{masked_name}@{domain}"
    return email


def get_genai_suggestion(instruction, prompt):
    client = genai.Client(api_key=config('GEMINI_API_KEY'))
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=instruction,
            max_output_tokens=500,
            temperature=0.1),
        contents=prompt,
    )

    return response

def get_suggestion(student_data):
    system_instruction = """You're the teacher of the day care center. 
                            Analyze the grade of the student and compare it with the standard raw score the a student must meet per domain subjects.
                            Give a comment or suggestion about there performance.

                            In your answer, include whether the children can skip one kinder level.
                            Your answer should be limited to 20-50 words.
                        """

    prompt = f"""Base on the grades and performance of the kinder student, 
                suggest if they are good to skip a kinder level and move to grade level or need some improvments.
                Performance data of the student: {student_data}"""

    suggestion = get_genai_suggestion(system_instruction, prompt)
    
    print(f"Suggestion: {suggestion.text}")
    print(f"Usage: {suggestion.usage_metadata}")


    return suggestion.text