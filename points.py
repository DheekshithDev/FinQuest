import ai_integration
import json
response = ai_integration.generate_ai_questions('write 3 questions about the Indian prime ministers', ' generate it in a json format whre there should be a question,options,correct answer,explamnation,followup and followup is   an array with two objects and each object has the question ,options,correct answsser ,explanation and the same for all the questions')
value1 = json.loads(response)
print(value1)
print(type(value1))
#print(value1[0]['options'])
