# -*- coding: utf-8 -*-
from os.path import isdir, isfile
from sys import platform
from imp import reload

from .options import Options
from .templates import Templates
from w2a.config import CONFIG
from w2a.core import printer
from w2a.lib.file import list_dir
from w2a.lib.dbconnect import DBConnect


class Framework():
    """docstring for Framework"""

    def __init__(self):
        self.modules = {}
        self.current_module = None

        self.options = Options()
        self.advanced_options = Options()
        self.options.add_boolean(
            'USECOLOR', 'Enable color on the console interface', default=False)
        self.options.add_boolean(
            'DEBUGFLAG', 'Enable debug infomation', default=False)
        self.modules_path = CONFIG.MODULES_PATH

        # db store
        try:
            self.dbconnect = DBConnect()
        except Exception as ex:
            self.dbconnect = None

        if platform.startswith('linux'):
            self.options.set_option('USECOLOR', 'True')

        if not isdir(self.modules_path):
            raise Exception('path to modules not found !')

        ############# get list loadable module ###############
        all_modules = list_dir(self.modules_path)
        loadable_modules = all_modules + []

        for module in all_modules:
            if not module.endswith('.py'):
                loadable_modules.remove(module)
                continue
            if module.startswith("__"):
                loadable_modules.remove(module)
                continue
            if module.lower() != module:
                loadable_modules.remove(module)
        del all_modules

        ############# import module ####################
        for module_name in loadable_modules:
            module_name = module_name[:-3]
            module = self.import_module(self.modules_path, module_name)
            self.set_module(module_name, module)

    def set_module(self, module_name, module):
        module_instance = module.Module()

        if not isinstance(module_instance, Templates):
            self.print_error(
                '%s is not child of Templates class' % module_name)

        if not hasattr(module_instance, 'run'):
            raise Exception('Module %s has no run() function' % module_name)

        if not isinstance(module_instance.options, Options) or not isinstance(module_instance.advanced_options, Options):
            raise Exception(
                'options and advanced_options must be Options instances')

        module_instance.name = module_name
        self.modules[module_name] = module_instance

    def reload_module(self, module_name=None):
        if module_name == None:
            if self.current_module != None:
                module_name = self.current_module
            else:
                self.print_debug(
                    'Must specify module if not module is currently being used')
                return False
        if not isfile('%s/%s.py' % (self.modules_path, module_name)):
            return False

        module = self.import_module(self.modules_path, module_name)
        reload(module)
        self.set_module(module_name, module)
        return True

    def import_module(self, path, module_name):
        return __import__((path + '.' + module_name).replace('/', '.'), None, None, ['Module'])
        # return __import__(path.replace('/', '.') , None, None, [module_name])
    ##################################

    def run(self, args, module_name=None):
        if module_name:
            if module_name in self.modules.keys():
                self.current_module = module_name
            else:
                raise Exception('No module name: ' + module_name)
        elif not self.current_module:
            raise Exception('Must \'use\' < module > first')

        module = self.modules[self.current_module]
        missing_options = self.options.get_missing_options()
        missing_options.extend(module.options.get_missing_options())

        if missing_options:
            self.print_error(
                'The following options must be set: ' + ', '.join(missing_options))
            return
        del missing_options
        module.run(self, args)

    def stop(self):
        if self.current_module:
            module = self.modules[self.current_module]
            module.close()

    def close(self):
        self.stop()

        if self.dbconnect:
            self.dbconnect.close()
            ##################################

    def print_error(self, message):
        printer.print_error(message, self.options['USECOLOR'])

    def print_success(self, message):
        printer.print_success(message, self.options['USECOLOR'])

    def print_line(self, message=''):
        printer.print_line(message)

    def print_status(self, message):
        printer.print_status(message, self.options['USECOLOR'])

    def print_debug(self, message):
        printer.print_debug(message, self.options['USECOLOR'])

    def print_process(self, percent):
        printer.print_process(percent, self.options['USECOLOR'])
