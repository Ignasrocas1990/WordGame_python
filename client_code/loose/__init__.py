from ._anvil_designer import looseTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
from ..game import game

class loose(looseTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    errors=anvil.server.call('get_errors')
    self.repeating_panel_loose.items = errors

  def play_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('game')

  def main_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('main')


