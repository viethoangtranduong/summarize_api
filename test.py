import requests
import numpy as np


BASE = "http://127.0.0.1:3001/"
# BASE = 'http://viethoangtranduong.pythonanywhere.com/'
BASE = 'http://ec2-54-221-124-167.compute-1.amazonaws.com:3001/'

# response = requests.patch(BASE + "2", {"txt": "whatthefuck"})
# print(response.json())


body1 = '''President Donald Trump’s health and the state of a fiscal stimulus package will be the main focus for markets in the coming week.

In the early morning hours Friday, President Donald Trump tweeted that he and the first lady tested positive for Covid. Stocks sold off hard, but the S&P 500 came off its lows in Friday trading and closed down just under 1%. It was up 1.5% for the week.

The market was helped by signs that a stimulus package is still a possibility, after House Speaker Nancy Pelosi asked airlines not to furlough workers. She promised either a stand alone aid bill, or a bigger negotiated relief legislation that would help the industry.'''

body2 = '''Another volatile week may be in store for traders as coronavirus cases rise in the U.S. and Europe while Democrats and Republicans remain at an impasse over new fiscal aid. The Dow Jones Industrial Average and S&P 500 fell for three straight days this week. That slide was the longest losing streak for the averages since mid-September. The two market benchmarks eked out slight gains on Friday to snap their losing streak. Investors and traders expect this choppy trading action to continue, especially as the worsening coronavirus data and a lack of U.S. coronavirus stimulus draw attention away from a strong earnings season thus far. "The combination of no stimulus, fading economic momentum, and the threat of rising coronavirus cases, creates a rather negative dynamic for risk assets right now," said Tom Essaye, founder of The Sevens Report, in a note to clients.\n\nThe seven-day average of new daily coronavirus infections has risen in 39 states, including New York, New Jersey and Wisconsin, according to a CNBC analysis of data from Johns Hopkins University and the U.S. Census Bureau. At the nationwide level, the rate of new daily cases is at its highest level since August. In Europe, the seven-day average of new Covid-19 cases has surpassed that of the U.S., leading several countries in the region to reinstate tougher social distancing rules and roll back previous reopening measures. "What this means is economic activity may slow down a bit, and we\'ve already started to see some of that in the data," said Art Hogan, chief market strategist at National Securities, noting the weekly jobless claims numbers released Thursday show they\'ve reached a point where "they\'re not going to get better; they\'re going to get worse." The Labor Department said initial U.S. jobless claims hit their highest level since August, reaching 898,000 in the week ending Oct. 10. Investors will also keep their eyes on Washington during the week ahead as lawmakers continue to struggle over new U.S. fiscal stimulus.\n\nPolitical posturing on stimulus \'hurting\' those in need\n\nThis week, President Donald Trump said he would raise his offer for a coronavirus aid above the current level of $1.8 trillion. The White House\'s current offer is smaller than a $2.2 trillion package passed by the House. House Speaker Nancy Pelosi, D-Calif., has said the administration\'s proposal "falls significantly short" of what is needed. This back and forth between the two parties has dwindled expectations among market participants of a compromise being reached before the Nov. 3 election. It has also added to the concerns surrounding the U.S. economic recovery. "This political posturing is hurting that cohort of the economy that needs help the most," said Quincy Krosby, chief market strategist at Prudential Financial. "To the small and mid-size business owner, the airlines, this is not just about politics; this is every day life. There going to be an impact in the real economy if we don\'t see something now."\n\nEarnings season ignored?\n\nThose talks over further stimulus are also expected to divert attention away from the corporate earnings season, which began this week but had next to no impact on the broader market. Procter & Gamble, Netflix, Travelers, American Airlines and American Express are among the companies slated to report next week. JPMorgan Chase, Goldman Sachs and VF Corp. are among the 49 S&P 500 companies that posted their latest quarterly results this week. Of those 49 companies, 86% reported better-than-expected earnings, according to data from The Earnings Scout. "I wish I could say that next week we\'re going to put aside the politics and the Covid concerns behind us, but we won\'t trade this earnings season," said Hogan of National Securities. "While it will likely be a record-breaking season for companies beating estimates, it\'s also going to be one that is largely ignored because there\'re so many other macro factors that are more important." There is also some important housing data in the week ahead, including home builders\' sentiment Monday, housing starts Tuesday, and existing home sales Thursday. "The housing market is still off to the races," said Mark Zandi, chief economist at Moody\'s Analytics. "The mortgage applications were strong, suggesting very strong activity in the month of September." Zandi said the market will eventually cool when interest rates begin to rise. But for now, "certainly the economy could use the juice." —CNBC\'s Patti Domm contributed to this report.\n\nWeek ahead calendar

'''

data = [{"text_in": body1},
        {'text_in': body1, 'len_out': 2},
        {'text_in': body2}]

print("Test 1: put response")

for i in range(len(data)):              
    response = requests.put(BASE + 'running', data[i])
    print(response.json())
    print("")

# print("Test 2: get response")

# response = requests.get(BASE + "1")
# print(response.json())

# print("Test 3: not existed")

# response = requests.get(BASE + "9")
# print(response.json())

# print("Test 4: delete")

# response = requests.delete(BASE + "0")
# print(response)

