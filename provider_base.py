"""
Base class for creating provider base classes
"""

# Python
from abc import ABCMeta
import logging

log = logging.getLogger(__name__)

class ProviderBase(metaclass=ABCMeta):
  # Registered providers get added to this dict
  providers = {}

  @classmethod
  def get(cls, provider, config):
    """
    Construct an instance of the given provider with the specified configuration
    """

    try:
      plugin = cls.providers[provider.lower()]
      return plugin(config)
    except KeyError:
      raise ValueError('{} provider "{}" is unknown. Ensure that the class has been imported and registered.'.format(
        cls.__name__,
        provider))

  @classmethod
  def register(cls, name=None):
    """
    Return a decorator that will register the given class as a provider
    with the given name. If name is None, use the class name. In either case,
    the name is case-insensitive.
    """

    def decorator(cls2register, name=name):
      """ Decorator to register the class as a provider """

      # Set name
      if name is None:
        name = cls2register.__name__
      name = name.lower()

      # Register the class
      if name in cls.providers:
        raise ValueError('{} provider "{}" is already registered.'.format(
          cls.__name__,
          name))

      cls.providers[name] = cls2register
      log.debug("{} provider registered: '{}'".format(
        cls.__name__,
        name))

      # Return the class unchanged
      return cls2register

    return decorator
