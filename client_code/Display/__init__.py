from ._anvil_designer import DisplayTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files

class Display(DisplayTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    table = []
    table = anvil.server.call('get_top10')
    self.repeating_panel_winners.items=table[:10]

    currUser=anvil.server.call('get_current_user')
    
    self.label_total.text=len(table)
    
    for row in table:
      if row["Who"]==currUser['Who']:
        self.label_curr.text = row["Position"]
        break
        
  
  def button_play_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('game')
    pass

  def button_main_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('main')
    pass




