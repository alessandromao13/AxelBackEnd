import ollama

res = ollama.chat(
	model="llava:7b",
	messages=[
		{
			'role': 'user',
			'content': 'Describe this image:',
			'images': ['./gay_cowboys.jpg']
		}
	]
)
print(res['message']['content'])
