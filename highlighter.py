import sublime
import sublime_plugin

import re
from collections import OrderedDict

COLORS_BY_SCOPE = OrderedDict() # TODO: Make color configurable
COLORS_BY_SCOPE['markup.changed.git_gutter'] = None # vivid purple
COLORS_BY_SCOPE['support.class'] = None # yellow
COLORS_BY_SCOPE['markup.deleted.git_gutter'] = None # vivid pink
COLORS_BY_SCOPE['markup.inserted.git_gutter'] = None # vivid green
COLORS_BY_SCOPE['constant.numeric'] = None # orange
COLORS_BY_SCOPE['constant.character.escape'] = None # light blue
COLORS_BY_SCOPE['variable'] = None # red
COLORS_BY_SCOPE['string'] = None # light green
COLORS_BY_SCOPE['comment'] = None # glay

class TextHighlighterToggleCommand(sublime_plugin.WindowCommand):
  # TODO: run this command when new tab is opened
  def run(self):
    active_view = self.window.active_view()
    selected_region = active_view.sel()
    sel_string = active_view.substr(selected_region[0])

    # Get word on cursor if any region isn't selected.
    if not sel_string:
      word_region = active_view.word(selected_region[0])
      sel_string = active_view.substr(word_region)

    views = self.window.views()
    if is_highlighted(sel_string):
      color = find_used_color(sel_string)
      for view in views:
        eraser(view, sel_string, color)
    else:
      color = find_usable_color(sel_string)
      for view in views:
        highlighter(view, sel_string, color)
    print(COLORS_BY_SCOPE)

class TextHighlighterClearAllCommand(sublime_plugin.WindowCommand):
  def run(self):
    views = self.window.views()
    for sel_string in COLORS_BY_SCOPE.values():
      color = find_used_color(sel_string)
      for view in views:
        if sel_string:
          eraser(view, sel_string, color)
    print(COLORS_BY_SCOPE)


def highlighter(view, sel_string, color):
  regions = find_all(view, sel_string)
  if color:
    if not COLORS_BY_SCOPE[color]:
      COLORS_BY_SCOPE[color] = sel_string
    view.add_regions(
      sel_string,
      regions,
      color,
      'dot',
      sublime.DRAW_NO_OUTLINE
      )

def eraser(view, sel_string, color):
  regions = find_all(view, sel_string)
  COLORS_BY_SCOPE[color] = None
  view.erase_regions(sel_string)

def find_all(view, sel_string):
  return view.find_all(re.escape(sel_string))

def is_highlighted(sel_string):
  highlighted = False
  for key, value in COLORS_BY_SCOPE.items():
    if value == sel_string:
      highlighted = True
      break
  return highlighted

def find_used_color(sel_string):
  color = None
  for key, value in COLORS_BY_SCOPE.items():
    if value == sel_string:
      color = key
  return color

def find_usable_color(sel_string):
  color = None
  for key, value in COLORS_BY_SCOPE.items():
    if not value:
      color = key
      break
  return color

