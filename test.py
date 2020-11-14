import requests
import numpy as np


BASE = "http://127.0.0.1:3000/"

# response = requests.patch(BASE + "2", {"txt": "whatthefuck"})
# print(response.json())


body = '''President Donald Trump’s health and the state of a fiscal stimulus package will be the main focus for markets in the coming week.

In the early morning hours Friday, President Donald Trump tweeted that he and the first lady tested positive for Covid. Stocks sold off hard, but the S&P 500 came off its lows in Friday trading and closed down just under 1%. It was up 1.5% for the week.

The market was helped by signs that a stimulus package is still a possibility, after House Speaker Nancy Pelosi asked airlines not to furlough workers. She promised either a stand alone aid bill, or a bigger negotiated relief legislation that would help the industry.'''

data = [{"text_in": body},
        {'text_in': body, 'len_out': 2}]
data = [{'text_in': body, 'len_out': 2}]

print("Test 1: put response")

for i in range(len(data)):
    response = requests.put(BASE + str(np.random.randint(10000)), data[i])
    print(response.json())

# print("Test 2: get response")

# response = requests.get(BASE + "1")
# print(response.json())

# print("Test 3: not existed")

# response = requests.get(BASE + "9")
# print(response.json())

# print("Test 4: delete")

# response = requests.delete(BASE + "0")
# print(response)

