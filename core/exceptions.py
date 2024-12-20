""" Собственные исключения """
class AssistantError(Exception):
  """Base class for assistant errors."""
  pass

class InternetConnectionError(AssistantError):
   """Raised when there is no internet connection."""
   pass

class DispatcherError(AssistantError):
  """Base class for dispatcher errors"""
  pass