# https://docs.python.org/3/reference/import.html#finders-and-loaders

import sys
from importlib.util import find_spec


class ImportHookFinder():
    def __init__(self):
        self._import_hooks = {}
        self._skip = set()

    def find_spec(self, fullname, path, target=None):
        # If we don't have an import hook registered or are already 
        # handling this module, let another loader handle it
        if fullname not in self._import_hooks or fullname in self._skip:
            return None

        self._skip.add(fullname)  # Mark module as currently being handled

        # Import module a second time, taking the loader that was found and wrapping with our own.
        try:
            spec = find_spec(fullname)
            loader = getattr(spec, "loader", None)

            if loader and not isinstance(loader, ImportHookChainedLoader):
                spec.loader = ImportHookChainedLoader(loader, self)
                return spec
        finally:
            self._skip.remove(fullname)

    def notify_import_hooks(self, name, module):
        # Remove import hooks entry before calling them
        hooks = self._import_hooks.pop(name, None)

        if hooks is not None:
            for hook in hooks:
                # Call each hook with the new module
                hook(module)

    def register_import_hook(self, name, hook):
        hooks = self._import_hooks.get(name, None)

        if hooks is None:
            # No hooks registered. Module may have already been imported.
            module = sys.modules.get(name, None)
            if module is not None:
                # Module was already imported, call hook immediately
                hook(module)
            else:
                # Module not imported but no hooks found, set up hooks list
                self._import_hooks[name] = [hook]
        else:
            # Existing hooks found, add a new one to the list
            hooks.apppend(hook)


class ImportHookChainedLoader():
    def __init__(self, loader, finder):
        self.loader = loader  # The original loader we're wrapping
        self.finder = finder  # The finder that holds our hooks

    def create_module(self, spec):
        return self.loader.create_module(spec)

    def exec_module(self, module):
        self.loader.exec_module(module)

        # Call the import hooks on the module being handled.
        self.finder.notify_import_hooks(module.__name__, module)

 
_finder = ImportHookFinder()

# Register finder with Python
sys.meta_path.insert(0, _finder)  

# Export register_import_hook to module as an API
register_import_hook = _finder.register_import_hook
