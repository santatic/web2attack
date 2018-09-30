# -*- coding: utf-8 -*-
import os
import sys
from traceback import print_exc
from random import choice
from subprocess import Popen

from cmd import Cmd
from w2a.config import CONFIG
from w2a.lib.file import full_path
from .core import Framework
from .options import Options
from .printer import color_status, color_success, print_error


# check readline module, available for tab
try:
    import readline
except ImportError:
    print_error(
        "No readline module found, no tab completion available.")


class OverrideCmd(Cmd, object):
    '''OverrideCmd class is meant to override methods from Cmd so they can\nbe imported into the base interpreter class.'''

    def __init__(self, debugging=False):
        super().__init__(completekey='tab')
        self.__hidden_commands__ = ['EOF']

    def cmdloop(self):
        while True:
            try:
                super().cmdloop()
                return
            except KeyboardInterrupt:
                self.print_line()
                self.print_error('Please use the \'exit\' command to quit')
                self.do_stop()

    def get_names(self):
        commands = super().get_names()
        for name in self.__hidden_commands__:
            if 'do_' + name in commands:
                commands.remove('do_' + name)
        return commands

    def emptyline(self):
        pass

    def help_help(self):
        self.do_help('')

    def precmd(self, line):
        tmpLine = line.split()
        if len(tmpLine) <= 1:
            return line
        if tmpLine[0] == '?':
            self.do_help(tmpLine[1])
            return ''
        else:
            return line

    def completenames(self, text, *ignored):
        dotext = 'do_'+text
        return [a[3:]+' ' for a in self.get_names() if a.startswith(dotext)]

    def do_EOF(self, args):
        self.print_line()
        return self.do_exit('')


class Interface(OverrideCmd):
    def __init__(self):
        super().__init__(self)
        self.__doc__ = 'The core interpreter for the program'
        self.doc_header = 'Type help <command> For Information\nList Of Available Commands:'

        self.frmwk = Framework()
        self.print_error = self.frmwk.print_error
        self.print_success = self.frmwk.print_success
        self.print_line = self.frmwk.print_line
        self.print_status = self.frmwk.print_status

    @property
    def intro(self):
        intro = os.linesep
        intro += '''	 -``--``--``-
	( Có gì Hot  )
	 `--'`--'`--'
	       \  ,__,
	        \ (oo)____
	          (__)    )\\
	             ||--|| *'''

        intro += os.linesep
        fmt_string = "\t<[ {0:<15} {1:>15} ]>"
        intro += fmt_string.format(CONFIG._NAME_,
                                   'v' + CONFIG._VERSION_ + '') + os.linesep
        intro += fmt_string.format('Loaded modules:',
                                   len(self.frmwk.modules)) + os.linesep
        return intro

    @property
    def prompt(self):
        if self.frmwk.current_module:
            if self.frmwk.options['USECOLOR']:
                return '\033[4;37m' + CONFIG._NAME_ + '\033[4;m (\033[' + CONFIG.COLOR_CMD + self.frmwk.current_module + '\033[1;m) > '
            else:
                return CONFIG._NAME_ + ' (' + self.frmwk.current_module + ') > '
        else:
            return '\033[4;37m' + CONFIG._NAME_ + '\033[4;m > '

    def default(self, args):
        argv = args.split(' ')
        if argv[0] in ['ifconfig', 'ls', 'dir', 'netstat', 'ps', 'clear', 'cat']:
            Popen(args, shell=True).wait()
        else:
            self.print_error('Unknown command !')

    def do_exit(self, args):
        self.frmwk.close()
        self.print_success(choice(CONFIG.QUOTES))
        return True

    def do_exploit(self, args):
        self.do_run(args)

    def do_help(self, args):
        super().do_help(args)

    def do_stop(self):
        self.frmwk.stop()

    #####################################################################
    def show_options(self, options):
        longest_name = 10
        longest_value = 16
        for option_name, option_def in options.items():
            longest_name = max(longest_name, len(option_name))
            longest_value = max(longest_value, len(str(options[option_name])))

        fmt_string = "  {0:<" + str(longest_name) + \
            "} {1:<" + str(longest_value) + "} {2:<10} {3}"
        self.print_line(color_status(fmt_string.format(
            'Name', 'Current Setting', 'Required', 'Description')))
        self.print_line(fmt_string.format(
            '----', '---------------', '--------', '-----------'))

        list_options = {}
        for option_name in options.keys():
            option_val = options[option_name]

            if option_val == None:
                option_val = ''
            option_id = options.get_option_id(option_name)
            option_req = 'no'

            if options.get_option_require(option_name):
                option_req = 'yes'
            option_desc = options.get_option_help(option_name)
            list_options[option_id] = fmt_string.format(
                option_name, str(option_val), str(option_req), option_desc)

        for v in list_options.values():
            self.print_line(v)

    def do_info(self, args):
        """Show module information"""
        args = args.split(' ')
        if args[0]:
            if args[0] in self.frmwk.modules.keys():
                module = self.frmwk.modules[args[0]]
            else:
                self.print_error('Invalid module name')
                return
        elif self.frmwk.current_module == None:
            self.print_error('Must select module to show information')
            return
        else:
            module = self.frmwk.modules[self.frmwk.current_module]
        ##########################
        fmt_string = '\t{0:<10} : {1}'
        self.print_line('')
        self.print_line(fmt_string.format('Name', module.name))

        if len(module.author) == 1:
            self.print_line(fmt_string.format('Author', module.author[0]))
        elif len(module.author) > 1:
            self.print_line(fmt_string.format(
                'Authors', ', '.join(module.author)))

        self.print_line(fmt_string.format('Version', str(module.version)))
        self.print_line()
        self.print_line(color_success('Basic Options:'))
        self.print_line('--------------')
        self.show_options(module.options)
        self.print_line()
        self.print_line(color_success('Advanced Options:'))
        self.print_line('-----------------')
        self.show_options(module.advanced_options)
        self.print_line()
        self.print_line(color_success('Description:'))
        self.print_line('------------')
        for line in module.detailed_description.split('\n'):
            self.print_line('  ' + line)

    def complete_info(self, text, line, begidx, endidx):
        # [i for i in self.frmwk.modules.keys() if i.startswith(text)]
        return self.complete_use(text, line, begidx, endidx)
    ##########################################

    def do_reload(self, args):
        """Reload a module in to the framework"""
        args = args.strip()
        if args:
            if not args in self.frmwk.modules.keys():
                self.print_error('Invalid Module Selected.')
                return
            else:
                module_name = args
        elif self.frmwk.current_module:
            module_name = self.frmwk.current_module
        else:
            self.print_error('Must \'use\' module first')
            return
        self.frmwk.reload_module(module_name)
        self.print_status('Successfully reloaded module: ' + module_name)

    def complete_reload(self, text, line, begidx, endidx):
        return self.complete_use(text, line, begidx, endidx)
    ##########################################

    def do_run(self, args):
        """Run the currently selected module"""
        args = args.split(' ', 1)
        old_module = None

        if args[0] in self.frmwk.modules.keys():
            old_module = self.frmwk.current_module
            self.frmwk.current_module = args[0]

        self.frmwk.print_line()
        if self.frmwk.current_module:
            try:
                self.frmwk.run(args)
            except Exception as e:
                print_exc()
        else:
            self.print_error('Must \'use\' < module > first')

        if old_module:
            self.frmwk.current_module = old_module

    def complete_run(self, text, line, begidx, endidx):
        return [i for i in self.frmwk.modules.keys() if i.startswith(text)]
    ##########################################

    def do_set(self, args):
        """Set an option, usage: set [option] [value]"""
        args = args.split(' ', 1)
        if len(args) < 2:
            self.print_error('set: [option] [value]')
            return
        name = args[0].upper()
        value = args[1].strip()

        if self.frmwk.current_module:
            options = self.frmwk.modules[self.frmwk.current_module].options
            advanced_options = self.frmwk.modules[self.frmwk.current_module].advanced_options
        else:
            options = self.frmwk.options
            advanced_options = self.frmwk.advanced_options
        if name in options:
            try:
                options.set_option(name, value)
                self.print_line(name + ' => ' + value)
            except TypeError:
                self.print_error('Invalid data type')
            except ValueError as ex:
                self.print_error('\n'.join(ex.args))
            except Exception as ex:
                self.print_error('\n'.join(ex.args))
            pass
            return
        elif name in advanced_options:
            try:
                advanced_options.set_option(name, value)
                self.print_line(name + ' => ' + value)
            except TypeError:
                self.print_error('Invalid data type')
            return
        self.print_error('Unknown variable name')

    def complete_set(self, text, line, begidx, endidx):
        try:
            if self.frmwk.current_module:
                options = self.frmwk.modules[self.frmwk.current_module].options
                options = dict(list(options.items(
                )) + list(self.frmwk.modules[self.frmwk.current_module].advanced_options.items()))
            else:
                options = dict(list(self.frmwk.options.items()) +
                               list(self.frmwk.advanced_options.items()))
            ##################
            cmd = line.split(' ', 3)
            if len(cmd) < 3:
                return [i+' ' for i in options.keys() if i.startswith(text.upper())]
            else:
                completes = options[cmd[1].strip().upper()][5]
                if completes != None:
                    return [i for i in completes if i.startswith(cmd[2])]
                elif options[cmd[1].strip().upper()][1] in ['file', 'dir']:
                    path = cmd[2].strip().rsplit('/', 1)
                    if len(path) == 1:
                        dir = ''
                        com = path[0]
                    else:
                        dir = path[0] + '/'
                        com = path[1]
                    dirs = os.listdir(full_path(dir))
                    completes = []
                    for c in dirs:
                        if os.path.isdir(full_path(dir + c)):
                            c = c + '/'
                        completes.append(c)
                    return [i for i in completes if i.startswith(com)]
                else:
                    pass  # get history
        except Exception as ex:
            print('\n')
            print_exc()
            pass
    ##########################################

    def do_unset(self, name):
        if not name:
            self.print_error('unset: [option]')
            return

        if self.frmwk.current_module:
            options = self.frmwk.modules[self.frmwk.current_module].options
            advanced_options = self.frmwk.modules[self.frmwk.current_module].advanced_options
        else:
            options = self.frmwk.options
            advanced_options = self.frmwk.advanced_options

        if name in options:
            options.unset_option(name)
        elif name in advanced_options:
            advanced_options.unset_option(name)
        else:
            self.print_error('Unknown option name : ' + name)

    def complete_unset(self, text, line, begidx, endidx):
        if self.frmwk.current_module:
            options = self.frmwk.modules[self.frmwk.current_module].options
        else:
            options = self.frmwk.options
        return [i+' ' for i in options.keys() if i.startswith(text.upper())]
    ##########################################

    def do_show(self, args):
        """Valid parameters for the "show" command are: modules, options"""
        args = args.split(' ', 1)

        if args[0] == '':
            args[0] = 'all'
        elif not args[0] in ['advanced', 'modules', 'options', 'all', '-h']:
            self.print_error('Invalid parameter "' +
                             args[0] + '", use "show -h" for more information')
            return

        if args[0] == 'modules':
            self.print_line(os.linesep + color_success('Modules') +
                            os.linesep + '=======' + os.linesep)
            longest_name = 20

            for module_name in self.frmwk.modules.keys():
                longest_name = max(longest_name, len(module_name))

            fmt_string = "  {0:" + str(longest_name) + "} {1}"
            self.print_line(color_status(
                fmt_string.format('Name', 'Description')))
            self.print_line(fmt_string.format('----', '-----------'))

            module_names = sorted(self.frmwk.modules.keys())
            for module_name in module_names:
                module_obj = self.frmwk.modules[module_name]
                self.print_line(fmt_string.format(
                    module_name, module_obj.description))
            self.print_line('')
            return
        elif args[0] in ['options', 'advanced', 'all']:
            if self.frmwk.current_module:
                if args[0] in ['options', 'all']:
                    self.print_line(os.linesep + color_success('Module Options') +
                                    os.linesep + '==============' + os.linesep)
                    self.show_options(
                        self.frmwk.modules[self.frmwk.current_module].options)
                if args[0] in ['advanced', 'all']:
                    self.print_line(os.linesep + color_success('Advanced Module Options') +
                                    os.linesep + '=======================' + os.linesep)
                    self.show_options(
                        self.frmwk.modules[self.frmwk.current_module].advanced_options)
            elif self.frmwk.current_module == None:
                if args[0] in ['options', 'all']:
                    self.print_line(os.linesep + color_success('Framework Options') +
                                    os.linesep + '=================' + os.linesep)
                    self.show_options(self.frmwk.options)
                if args[0] in ['advanced', 'all']:
                    self.print_line(os.linesep + color_success('Advanced Framework Options') +
                                    os.linesep + '==========================' + os.linesep)
                    self.show_options(self.frmwk.advanced_options)
            self.print_line()
        else:
            self.print_status(
                'Valid parameters for the "show" command are: modules, options, advanced')

    def complete_show(self, text, line, begidx, endidx):
        return [i for i in ['modules', 'options', 'advanced', 'all'] if i.startswith(text)]
    ##########################################

    def do_use(self, args):
        """Select a module to use"""
        if self.frmwk.current_module != None:
            self.frmwk.reload_module(self.frmwk.current_module)

        args = args.split(' ', 1)
        if args[0] in self.frmwk.modules.keys():
            self.frmwk.current_module = args[0]
        else:
            self.print_error('Failed to load module: ' + args[0])

    def complete_use(self, text, line, begidx, endidx):
        if line.find('/') != -1:
            text = line.split(' ', 1)[1].strip()
            return [i[len(text.rsplit('/', 1)[0]) + 1:] for i in self.frmwk.modules.keys() if i.startswith(text)]
        return [i for i in self.frmwk.modules.keys() if i.startswith(text)]
    ##########################################

    def do_back(self, args):
        """Stop using a module"""
        self.frmwk.current_module = None
    ##########################################

    def do_banner(self, args):
        """Print the banner"""
        self.print_line(self.intro)
