from google import genai
from google.genai import types


def talkAI(instruction, prompt):
    client = genai.Client(api_key="AIzaSyArOL_G8qDWb1EVdDHJUOClcePSKS5GZk4")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=instruction,
            max_output_tokens=500,
            temperature=0.1),
        contents=prompt,
    )

    return response

def main():
    system_instruction = """You're the head of the day care center. 
                            Analyze the grade of the student and give a comment or suggestion about there performance.
                            Your answer should be limited to 20-50 words.
                        """
    

    student_performance = {
        "name": "John Doe",
        "grades": {"Math": 70, "Science": 85, "English": 90},
        "performance": "John struggles with mathematical problem-solving but has strong comprehension skills in English."
    }


    prompt = f"""Base on the grades and performance of the kinder student, 
                suggest if they are goods to be move to grade level or need some improvments.
                Performance data of the student: {student_performance}"""

    suggestion = talkAI(system_instruction, "What is facebook?")
    
    print(f"Suggestion: {suggestion.text}")
    print(f"Usage: {suggestion.usage_metadata}")

if __name__ == "__main__":
    main()