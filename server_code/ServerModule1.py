import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.server
import random
from datetime import datetime

file = (app_files.words).get_bytes()
wf = file.decode('UTF-8')
wf = wf.split("\n")
words = {line.replace("'s", "").lower() for line in wf} 
words = [line for line in words if len(line)>3]
words = sorted(words)[1:]
error_list=[]


@anvil.server.callable
def get_keyword():
  return list(random.choice([i for i in words if len(i)>7]))

def get_possible_keywords(keywords):
  """internal method to get all possible anwers"""
  keyword = list(keywords)
  currList=[]
  for w in words:
      check = True
      for i in w:
          if i not in keyword or w.count(i)>keyword.count(i) or w == "".join(keyword):
              check=False
              break
      if check==True:
          currList.append(w)
  return currList

def check_if_winner(guess,keyword):
  """internal method to to check if it is a winner"""
  currList = get_possible_keywords(keyword)
  guess = set(guess.split(" "))
  if len(guess) >= 7:
    guess.difference_update(set(currList))
    if len(guess)==0:
      return True
  return False
    
@anvil.server.callable
def insert_attempt(guess,time,keyword,user_agent):
  """insert any attempts"""
  winer = check_if_winner(guess,keyword)
  
  app_tables.scores.add_row(
  Time=float(time),Who=" ",Sourceword=keyword,
  Matches=guess.replace(" ",","),Winner=winer,
  IPaddress=anvil.server.context.client.ip,
  TimeStamp=datetime.now(),
  UAG=user_agent
  )
  return winer

@anvil.server.callable
def get_errors():
  """looks finds inserted row and looks through it geting errors"""
  looser = []
  for r in app_tables.scores.search(Who=" ",Winner=False):
    looser = r
  
  
  guess = looser['Matches']
  keyword = looser['Sourceword']  
  
  spell_c = small_c = letters_c =  False
  guesses = guess.split(",")
  n_of_guesses = len(guesses)
  
  num_err="• You have an incorrect number of words: "+str(n_of_guesses)+",not 7"
  letters_err="• You used these invalid letters: "
  spell_err="• You misspelt these words: "
  small_err="• These words are too small: "
  source_err="• You cannot use the source word: "+keyword

  
  currList = get_possible_keywords(keyword)
  """checks and create's error messages"""
  worderr=False
  for word in guesses:
    if len(word) < 4:
      small_err+=word+" "
      small_c=True
      if(word not in keyword):
        letters_err+=word+" "
        letters_c=True
    elif word == "".join(keyword) and worderr==False:
      error_list.append({'error':source_err})
      worderr=True
    elif word not in currList:#if its not in the list
      if len(word)==1:
         letters_err+=word+" "
         letters_c=True
      else:
        spell_err+=word+" "
        spell_c=True
      for letter in word:
        if letter not in keyword:
          letters_err+=letter+" "
          letters_c=True
    
  if n_of_guesses < 7:
    error_list.append({'error':num_err})
  if letters_c:
    error_list.append({'error':letters_err})
  if spell_c:
    error_list.append({'error':spell_err})
  if small_c:
    error_list.append({'error':small_err})
    
  looser['Who']="unknown"
  looser['errors']= error_list
  return error_list


@anvil.server.callable
def get_time():
  """get elapsed time of current player"""
  return str([r['Time'] for r in app_tables.scores.search(Who=" ")])[1:-1]  

@anvil.server.callable
def update_name(name):
  """Update user name method"""
  rows=len(app_tables.scores.search(Who=name))
  if rows == 0:
    for r in app_tables.scores.search(Who=" "):
      r['Who']=name
      r['errors']=[]
    return True
  else:
    return False

@anvil.server.callable
def get_top10():
  """fileter table to get Position column"""
  table = app_tables.scores.search(tables.order_by('Time'),Winner=True)
  display_table=[]
  index=1
  for row in table:
    display_table.append({ "Position": index, "Time": row['Time'],"Who":row['Who'], "Sourceword": row['Sourceword'],"Matches": row['Matches']})
    index+=1
  return display_table


@anvil.server.callable
def get_current_user():
  """get Current player"""
  return app_tables.scores.search(tables.order_by('TimeStamp', ascending=False))[0]

@anvil.server.http_endpoint('/top10')
def printTop10(**p):
  """create's a string for top 10"""
  table=get_top10()
  text ="Position Time \t\t Who \t\t Sourceword \t\t Matches\n"
  for i, row in enumerate(table[:10],start=1):
    curRow = list(row.values())[1:]
    curItem = str(curRow.pop(0))
    curRow.insert(0,curItem)
    curRow = "\t       ".join(curRow)
    text+=f"{i}: \t{curRow}\n"
  return text

@anvil.server.http_endpoint('/log')
def printLog(**p):
  """create log string for web"""
  text ="Winner \t IPadress \t\t TimeStamp \t\t User-agent-identifier \t\t Sourceword \t\t Guesses \n"
  table = app_tables.scores.search(tables.order_by('TimeStamp',ascending=False))
  for row in table:
    text+=str(row['Winner'])+"\t"+row['IPaddress']+"\t"+str(row['TimeStamp'])+"\t"+row['UAG']+"\t\t\t"+row['Sourceword']+"\t"+row['Matches']+"\n"
    if(row['errors']!=[]):
      text+="ERRORS : "
      for err in row['errors']:
        value="\t".join(list(err.values()))
        text+=value
      text+="\n\n"
    else:
      text+='\n'
  return text

@anvil.server.http_endpoint('/get-user-agent')
def get_user_agent():
  """method to get use browser"""
  return {'UAG': anvil.server.request.headers['user-agent']}
