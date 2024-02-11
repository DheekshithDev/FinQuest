from openai import OpenAI
#prompt = ' generate it in a json format whre there should be a question,options,correct answer,explamnation,followup parameter is an array with two objects and each object has the question ,options,correct answsser ,explanation'
API_KEY = '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'
GPT_MODEL = "gpt-3.5-turbo-1106"

def generate_ai_questions(user_input, system_input):
    # Initialize OpenAI client
    client = OpenAI(api_key=API_KEY)

    example_prompt = """
        Example output:
        {
          "question": "What is the capital of France?",
          "options": ["Paris", "London", "Berlin", "Madrid"],
          "correct_answer": "Paris",
          "explanation": "Paris is the capital of France.",
          "follow_ups": [
            {
              "question": "Which river flows through Paris?",
              "options": ["Seine", "Thames"],
              "correct_answer": "Seine",
            },
            {
              "question": "In which country is Paris?",
              "options": ["France", "Spain"],
              "correct_answer": "France",
            }
          ]
        }
        """

    # Define the system message with the task
    system_message = {
        "role": "system",
        "content": system_input + example_prompt
    }

    # User message with user input
    user_message = {"role": "user", "content": user_input}

    # Request for generating 10 trivia questions
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[system_message, user_message],
        temperature=1
    )

    # Retrieve the generated questions as JSON
    generated_questions_json = response.choices[0].message.content

    return generated_questions_json


# Example usage:
user_input = 'Please create a real-life financial scenario question with four options.'
system_input = '''
        Generate output in a json format where there is a "question" field containing a real-life financial scenario question,
        an "options" field with an array of four options, a "correct_answer" field specifying the correct option,
        an "explanation" field explaining why the answer is correct, and a "follow_ups" field that is an array containing five follow-up questions relevant to the main question. 
        Each follow-up question should also have "question", 
        "options" field with two options, and "correct_answer" field.
        '''
# generated_questions = generate_ai_questions(user_input, system_input)
# print(generated_questions)
