from ._anvil_designer import WinTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files

class Win(WinTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.seconds.text = anvil.server.call('get_time')
      
    # Any code you write here will run when the form opens.
    
  def button_1_click(self, **event_args):
    if self.name.text != "":
      updated=anvil.server.call('update_name',self.name.text)
      if updated == True:
        open_form('Display')
      else:
        alert("Name already exist in the database, Please provide with different name")
        self.name.text=""
    else:
      alert("Name field left empty. Please provide your name")
    

