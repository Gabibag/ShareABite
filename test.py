import easyocr
import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv('key')

name = 'multican.jpg'

reader = easyocr.Reader(['en']) 
result = reader.readtext(name)

food = ""

for x in result: 
    food = food + x[1] + " "

list_foods = []

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "In this sentence pick out the name of the every main food item: " + food + ". Only return the name of the food items and nothing else. for example 'beef stew', 'carrots', 'spinach'"}
  ]
)
list_foods = completion.choices[0].message.content.split(",")

print(list_foods)
