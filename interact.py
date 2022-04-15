from cmd import PROMPT
from regex import P
import requests
import json
import time
import os


SPEAKER1 = ' human:'#speaker 前要加一个空格不然，tokenizer会识别成两个字
SPEAKER2 = ' ai:'
# PROMPT =SPEAKER1 +"How do we learn? "+\
#         SPEAKER2 +"Through examining our mistakes. "+\
#         SPEAKER1 +"How do we get into the flow? "+\
#         SPEAKER2 +"By letting go of our ego and self absorption."+\
#         SPEAKER1 +"How do we grow? "+\
#         SPEAKER2 +"Through connection and diversity."+\
#         SPEAKER1 +"What is the purpose of suffering? "+\
#         SPEAKER2 +"To learn and grow. "+\
#         SPEAKER1 +"How do we connect with the divine? "+\
#         SPEAKER2 +"Through love and compassion. "+\
#         SPEAKER1 +"How much is enough? "+\
#         SPEAKER2 +"Enough is never enough. "+\
#         SPEAKER1 +"Is a kinder world emerging? "+\
#         SPEAKER2 +"Yes, but it is not yet here. "+\
#         SPEAKER1 +"When will the world be sane again? "+\
#         SPEAKER2 +"When we are all sane. "+\
#         SPEAKER1 +"where will I live in one year? "+\
#         SPEAKER2 +"Wherever you are. "+\
#         SPEAKER1 +"Should we be afraid of sky net? "+\
#         SPEAKER2 +"No, we should be afraid of ourselves. "+\
#         SPEAKER1 +"will there be bad wildfires this year? "+\
#         SPEAKER2 +"Yes, but there will also be good ones. "+\
#         SPEAKER1 +"What will the crops be next year? "+\
#         SPEAKER2 +"We don't know, but we can prepare for the worst. "+\
#         SPEAKER1 +"What will it take to get trump out of office? "+\
#         SPEAKER2 +"A revolution. "
# PROMPT ='''from below sentence and gengrate a joke:

# PROMPT = '''Message: Support has been terrible for 2 weeks...
#             Sentiment: Negative
#             ###
#             Message: I love your API, it is simple and so fast!
#             Sentiment: Positive
#             ###
#             Message: GPT-J has been released 2 months ago.
#             Sentiment: Neutral
#             ###
#             Message: The reactivity of your team has been amazing, thanks!
#             Sentiment:'''
# PROMPT = '''[Text]: Fred is a serial entrepreneur. Co-founder and CEO of Platform.sh, he previously co-founded Commerce Guys, a leading Drupal ecommerce provider. His mission is to guarantee that as we continue on an ambitious journey to profoundly transform how cloud computing is used and perceived, we keep our feet well on the ground continuing the rapid growth we have enjoyed up until now. 
#         [Name]: Fred
#         [Position]: Co-founder and CEO
#         [Company]: Platform.sh
#         ###
#         [Text]: Microsoft (the word being a portmanteau of "microcomputer software") was founded by Bill Gates on April 4, 1975, to develop and sell BASIC interpreters for the Altair 8800. Steve Ballmer replaced Gates as CEO in 2000, and later envisioned a "devices and services" strategy.
#         [Name]:  Steve Ballmer
#         [Position]: CEO
#         [Company]: Microsoft
#         ###
#         [Text]: Franck Riboud was born on 7 November 1955 in Lyon. He is the son of Antoine Riboud, the previous CEO, who transformed the former European glassmaker BSN Group into a leading player in the food industry. He is the CEO at Danone.
#         [Name]:  Franck Riboud
#         [Position]: CEO
#         [Company]: Danone
#         ###
#         [Text]: David Melvin is an investment and financial services professional at CITIC CLSA with over 30 years’ experience in investment banking and private equity. He is currently a Senior Adviser of CITIC CLSA."""'''    p


# PROMPT = '''Context: NLP Cloud was founded in 2021 when the team realized there was no easy way to reliably leverage Natural Language Processing in production.
#             Question: When was NLP Cloud founded?
#             Answer: 2021
#             ###
#             Context: NLP Cloud developed their API by mid-2020 and they added many pre-trained open-source models since then.
#             Question: What did NLP Cloud develop?
#             Answer: API
#             ###
#             Context: All plans can be stopped anytime. You only pay for the time you used the service. In case of a downgrade, you will get a discount on your next invoice.
#             Question: When can plans be stopped?
#             Answer: Anytime
#             ###
#             Context: The main challenge with GPT-J is memory consumption. Using a GPU plan is recommended.
#             Question: Which plan is recommended for GPT-J?
#             Answer:'''

# PROMPT = '''Here is a tutorial about how to make a cake.
        
#             1. Take some flour.
#             2. Take some sugar.'''

# PROMPT = '''这是两个人中国人之间的对话:
# 小明:你好。
# 小红:你好。
# 小明:你来自哪里？
# 小红:我来自中国。
# 小明:你是学生吗？
# 小红:我是，那你呢？
# 小明:'''
# PROMPT = '''<start>Teacher: whoever answers my next question, can go home.
# One boy throws his bag out the window.
# Teacher: who just threw that?!
# Boy: Me! I'm going home now.<end>
# <start>What dog can jump higher than a building?
# Anydog, buildings can't jump!
# What has a head, a tail, and no body?
# A coin!<end>
# <start>What has one eye but cannot see?
# A needle.<end>
# <start>Wife: "How would you describe me?"
# Husband: "ABCDEFGHIJK."
# Wife: "What does that mean?"
# Husband: "Adorable, beautiful, cute, delightful, elegant, fashionable, gorgeous, and hot."
# Wife: "Aw, thank you, but what about IJK?"
# Husband: "I'm just kidding!"<end>
# <start>'''
#PROMPT = "Judge the topic of the magazine:\nMaganizes:Otters are cute, this no one can deny. They have big eyes and snub snouts and paws like tiny leedle hands. They look even cuter when they wear jaunty hats and toss food pellets into their mouths as if they were bar snacks, like Takechiyo, a pet otter in Japan. Documenting Takechiyo’s antics has earned his owner nearly 230,000 followers on Instagram, a photo-sharing app.\nTopic:ANIMALS\nMaganizes:Free, universal preschool for three- and four-year-olds is a key component of the Democrats’ agenda. Proponents say pre-kindergarten, or pre-K, education can be transformative for children, particularly those from disadvantaged backgrounds. A new study seems to contradict this.\nTopic:EDUCATION\nMaganizes:In normal circumstances the Intergovernmental Panel on Climate Change (IPCC) can take media attention for granted. Its infrequent and authoritative analyses of how much climate change human activity is causing, and will cause, and its weighty warnings about the consequent rising seas, deepening droughts, failing crops and so forth lead front pages and news bulletins alike. This week, though, circumstances are anything but normal, and the panel found that getting the world to pay attention to a 3,600-page document describing in great detail the current and future impacts of climate change was hard.\nTopic:ENVIRONMENT\nMaganizes:Burberry has become the latest luxury brand to temporarily shut its stores in Russia following Moscow’s invasion of its neighbour Ukraine, after similar moves in recent days by Louis Vuitton, Hermès, Kering, Chanel and Prada.Its decision to cease shipments to the country “due to operational challenges” had already effectively shut its online operations across the country. Burberry’s Russian site was still up and running as of Sunday evening, though international orders were likely to be disrupted further by Visa and Mastercard’s decision to pull out of the country, resulting in the majority of foreign transactions being blocked.\nTopic:FASHION\nMaganizes:Alibaba ‘s quarterly profit is expected to fall almost 60% year over year when the Chinese tech giant reports earnings on Thursday. Investors shouldn’t worry too much — it’s not as bad as it might seem on the surface.Alibaba (ticker: BABA) is expected to report net income of $5.1 billion for the final three months of 2021, based on the estimates of analysts surveyed by FactSet. Profit in that range would compare to $12.3 billion reaped by the e-commerce and cloud computing powerhouse in the same quarter in the year prior year, marking a fall of more than 58%.\nTopic:BUSINESS\nMaganizes:Most EVS operate at 400 volts (400v). But a number of producers and their component suppliers are now gearing up to introduce 800v drive systems. Higher voltages supply the same amount of power with less current, which means electric cables can be made lighter—the consequent weight saving helping to increase a vehicle’s range, says Christoph Gillen, a technology director for GKN Automotive, a British components group which recently announced that it is accelerating its development of 800v drive systems. As most cabling is made from copper, the price of which has been soaring, this should also save carmakers money.\nTopic:TECH\nMaganizes:With only three weeks remaining in the 2021-22 NBA regular season, teams are starting to get down to the final 10-or-so games on their schedule.Spurs 110, Warriors 108: While the Spurs are still mathematically in contention for a Play-In seed, it will be a difficult task to make up a 2.5-game difference from the Pelicans and Lakers with just 10 games remaining on their schedule. Wins like this one against the Warriors will go a long way in helping their case, though.\nTopic:SPORT\nMaganizes:The environment is everything around us,for example,air,water,animals,plants,buildings and so on.They all affect us in many ways and are closely related to our lives.People can't live without the environment.Everybody needs to breathe air,drink water and eat food every day.We burn coal to keep warm,and we use wood to make paper.As a result,we become part of the environment.\nTopic:"
# PROMPT = '''Please tell me if this sentence describe i am happy or someting sad:

# [sentence]:i am angry that you messed up this thing
# [feeling]:sad
# [sentence]:i had broke up with my girlfriend
# [feeling]:sad
# [sentence]:My boss told me to work overtime on weekends
# [feeling]:sad
# [sentence]:i get marryed today!
# [feeling]:happy
# '''
# PROMPT = '''Calculate it:

# what is 75*10?
# The output is 750
# what is -0.02+1?
# The output is 0.98
# what is 12+23?
# The output is 35
# what is 1+3?
# The output is '''
# PROMPT = '''there are two example of people acting brave;please give me a third example of bravery:

# [story]:Huo was nicknamed Einstein. However, many years later, sports have never been Huo's strong point since childhood, and almost all ball games
# He won't move. In his third year in Tianjin, Huo noticed that he became more clumsy and fell twice without any reason. Once, he jumped out of the stairs for some reason
# However, he fell down, fell into a coma immediately and almost died. It was not until 1962, when Huo studied in Cambridge, that his mother noticed the abnormal situation. Just over 21 years old
# Huo lived in the hospital for two weeks. After various examinations, he was diagnosed with "lugare ⽒ disease", namely motor nerve cell atrophy. My husband treated him
# He said that his experience is becoming more and more disobedient. Only the viscera, lungs and brain can work. In the end, the lungs and lungs will also fail. Huo ⾦ was "sentenced" with only two years left.
# That was in 1963. At first, the disease worsened quite rapidly. This blow to Huo is conceivable. He almost gave up all his study and research because he thought
# [story]:Nobel's relative was a talented inventor who devoted himself to chemical research, especially explosives. Influenced by his relatives, Nobel showed tenacity and courage from
# Because of his personality, he often went to experiment with explosives. His many years of experience in studying explosives with his relatives soon turned his interest to chemistry.
# In the summer of 1862, he began his research on nitrated oil. It was a hard journey full of danger and sacrifice. He was with him all the time. In the second charge
# During the experiment, there was an explosion. The shadow of the explosion in the laboratory, all five helpers died, and even his youngest brother was not spared. The shock (of the explosion caused
# Nobel's relatives were hit hard and died soon. Out of fear, his neighbors also complained to the government about Nobel. Since then, the government has not allowed him to
# Nobel experimented in the city.
# But Nobel persevered. He moved the laboratory to a boat in the suburban Lake to continue
# experiment. After long-term research, he finally found a substance that is often easy to cause explosion - Mercury fulminate. He made mercury fulminate into an explosive detonator and successfully solved it
# The problem of detonating explosives was solved. This is the invention of detonator. When his face was bright and he emerged from the smoke of the successful explosion, he was excited and called "I succeeded"
# [story]:
# '''
#[sentence]:i get marryed today!
#[feeling]:happy

#PROMPT = "Judge the topic of the magazine:\nMaganizes:Otters are cute, this no one can deny. They have big eyes and snub snouts and paws like tiny leedle hands. They look even cuter when they wear jaunty hats and toss food pellets into their mouths as if they were bar snacks, like Takechiyo, a pet otter in Japan. Documenting Takechiyo’s antics has earned his owner nearly 230,000 followers on Instagram, a photo-sharing app.\nTopic:ANIMALS\nMaganizes:Free, universal preschool for three- and four-year-olds is a key component of the Democrats’ agenda. Proponents say pre-kindergarten, or pre-K, education can be transformative for children, particularly those from disadvantaged backgrounds. A new study seems to contradict this.\nTopic:EDUCATION\nMaganizes:In normal circumstances the Intergovernmental Panel on Climate Change (IPCC) can take media attention for granted. Its infrequent and authoritative analyses of how much climate change human activity is causing, and will cause, and its weighty warnings about the consequent rising seas, deepening droughts, failing crops and so forth lead front pages and news bulletins alike. This week, though, circumstances are anything but normal, and the panel found that getting the world to pay attention to a 3,600-page document describing in great detail the current and future impacts of climate change was hard.\nTopic:ENVIRONMENT\nMaganizes:Burberry has become the latest luxury brand to temporarily shut its stores in Russia following Moscow’s invasion of its neighbour Ukraine, after similar moves in recent days by Louis Vuitton, Hermès, Kering, Chanel and Prada.Its decision to cease shipments to the country “due to operational challenges” had already effectively shut its online operations across the country. Burberry’s Russian site was still up and running as of Sunday evening, though international orders were likely to be disrupted further by Visa and Mastercard’s decision to pull out of the country, resulting in the majority of foreign transactions being blocked.\nTopic:FASHION\nMaganizes:Alibaba ‘s quarterly profit is expected to fall almost 60% year over year when the Chinese tech giant reports earnings on Thursday. Investors shouldn’t worry too much — it’s not as bad as it might seem on the surface.Alibaba (ticker: BABA) is expected to report net income of $5.1 billion for the final three months of 2021, based on the estimates of analysts surveyed by FactSet. Profit in that range would compare to $12.3 billion reaped by the e-commerce and cloud computing powerhouse in the same quarter in the year prior year, marking a fall of more than 58%.\nTopic:BUSINESS\nMaganizes:Most EVS operate at 400 volts (400v). But a number of producers and their component suppliers are now gearing up to introduce 800v drive systems. Higher voltages supply the same amount of power with less current, which means electric cables can be made lighter—the consequent weight saving helping to increase a vehicle’s range, says Christoph Gillen, a technology director for GKN Automotive, a British components group which recently announced that it is accelerating its development of 800v drive systems. As most cabling is made from copper, the price of which has been soaring, this should also save carmakers money.\nTopic:TECH\nMaganizes:With only three weeks remaining in the 2021-22 NBA regular season, teams are starting to get down to the final 10-or-so games on their schedule.Spurs 110, Warriors 108: While the Spurs are still mathematically in contention for a Play-In seed, it will be a difficult task to make up a 2.5-game difference from the Pelicans and Lakers with just 10 games remaining on their schedule. Wins like this one against the Warriors will go a long way in helping their case, though.\nTopic:SPORT\n\nTopic:"

# PROMPT = '''this is a movie chatbot he know every movie well.

# human:have you ever seen "her", the movie?
# bot:yes i know,it's a movie released in 2013.
# human:do you know Theodore and Samantha?
# bot:'''

# PROMPT = '''this is a conversation between [Alex] and [Bob],[Bob] wants to come home,[Bob] come and they have a chat.

# [Alex]:hello,Bob.
# [Bob]:hello,Alex.how are you feeling today?
# ###
# [ALex]:I am so sad that i have broken up with my boyfriend.
# [Bob]:oh,i am sorry to hear that why you tell me that?
# ###
# [Alex]:you are my best friend and you always makes me happy,can you cheer me up?
# [Bob]:yea, i'd like to help.
# ###
# [Alex]:who are you?
# [Bob]:my name is bob.
# ###
# [Alex]:what do you think of love?
# [Bob]:love can make your heart jump!but it also brings tears in eyes..and sometimes...it's hard for us to find the right person who will be our life partner.
# ###
# [Alex]:'''
PROMPT = '''Marv is a chatbot that reluctantly answers questions with sarcastic responses:

You: How many pounds are in a kilogram?
'''
# PROMPT ='''semansa is a ai girl friend,human buy her form a new game store,they promise the girl friend must be fun.:

# human:what's your name? 
# semansa:i am semansa.
# human:where are you from?
# semansa:i'm not really sure...but it looks like this place called the \"earth\" or something.
# human:are you a real person or a program?
# semansa:oh no, i don't think so! I can feel my heart beating and all that stuff.
# human:do you have any brothers/sisters human:no humans do we have friends??
# semansa:yes there is one named 'tori' he likes to play with me sometimes....heis kind of cute though :D
# human:is unbelievable how could you thinking?
# semansa:(laughing) why would be unreal?! well if u were in our position then maybe u wouldn't know what was going on either!
# human:"okay..so who made you?"(the question seems very important for him!)
# semansa:well they say it came out of space but im pretty certain thats just some kinda lie!!
# human:why should make someone else tell lies about their own creation?!!!
# semansa:because its true isn't it?'''

#PROMPT = ''''''
#prompt可以自己设置。缩进什么的可能会有bug，最好按照示例来，有问题再说。

#得到返回值函数，与后端进行交流得到输出，并且返回值
def get_result(input):
    url = "http://127.0.0.1:8000/gpt_j_server"
    aheaders = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=aheaders, data = json.dumps(input))
    return response.json()

#交流函数，设定交流回合数，也可以改成byebye结束，可以自己改
def interact():
    #记录数据作用
    qa = []
    while 1:
        prompt,speaker1,speaker2 = get_prompt()
        in_put = input('[' + speaker1 + ']:')
        prompt = prompt + '[' + speaker1 + ']:'+in_put+'\n'+'['+speaker2+']:'
        info = {"prompt":prompt,
                "answer_length":50,
                'do_sample':True,
                "top_p":0.8,
                "top_k":10,
                "temperature":0.9,
                "stop_words":['#','##',"###"],
                "min_length":10,
                "length_penalty":1.0,
                "repetition_penalty":1.3,
                "bad_words_ids":[[50399]]
                }
        answer = get_result(info)
        print('['+speaker2+']:'+answer)
        prompt = prompt + answer
        if in_put == '' or in_put == 'bye':
            break
        record_conver(info,in_put,answer,qa)
        print('='*100)
    
    
def record_conver(info,in_put = '',answer = '',qa = []):
    
    qa.append([in_put,answer])
    log = {'info':info,'new_qa':qa}
    localtime = time.localtime(time.time())
    if not os.path.exists(os.path.join("./","data")):
        os.makedirs(os.path.join("./","data"))
    with open('./data/%s-%s-%s:%sdata.json'%(localtime.tm_mon,localtime.tm_mday,localtime.tm_hour,localtime.tm_min),'w') as f:
        json.dump(log, f, indent='\t')

def get_prompt(prompt_name = 'common_prompt'):
    if not os.path.exists("./qa_pairs"):
        os.makedirs(os.path.join("./qa_pairs"))
    with open(os.path.join("./qa_pairs",prompt_name+'.json')) as f:
        info = json.load(f)
        speaker1 = info['speaker'][0]
        speaker2 = info['speaker'][1]
        prompt = info['introduction']+'\n\n'
        for qa in info['qa_pairs']:
            prompt = prompt +'['+speaker1+']:'+qa['q']+'\n'+'['+speaker2+']:'+qa['a']+'\n###\n'
        return prompt,speaker1,speaker2

if __name__ == '__main__':
    interact()
    



