import requests

response = requests.put('http://127.0.0.1:5000/key_sample', data='Ehi, come va?')
print(response)
response = requests.get('http://127.0.0.1:5000/key_sample')
print(response)
response = requests.get('http://127.0.0.1:5000')
print(response)
response = requests.delete('http://127.0.0.1:5000/key_sample')
print(response)
response = requests.get('http://127.0.0.1:5000')
print(response)
