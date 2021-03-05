from ._anvil_designer import gameTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import string
import time
start = time.time()
class game(gameTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.keyword.text = "".join(anvil.server.call('get_keyword'))
    
  def get_id(self):
    user_agent=""
    user_agent = anvil.http.request(anvil.server.get_api_origin() + '/get-user-agent', json=True)['UAG']
    user_agent= user_agent[-20:]
    poss = user_agent.find("/")
    user_agent = user_agent[-18:poss]
    user_agent.strip(" ")
    return user_agent
    
    #print(start)
  def button_1_click(self, **event_args):
    if self.guesses.text!="":
      errors=[]
      end = time.time()
      curr_time = str(round(end-start, 2))
      check=anvil.server.call('insert_attempt',self.guesses.text,curr_time,self.keyword.text,self.get_id())
      #errors = anvil.server.call('check_guesses',self.guesses.text,curr_time,self.keyword.text)
      if check:
        open_form('Win')
      else:
        open_form('loose')
    else:
      alert("Guess field is empty.Please try some keywords")