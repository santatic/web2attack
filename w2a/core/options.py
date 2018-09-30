# -*- coding: utf-8 -*-

from os.path import isfile, isdir


class Options(dict):
    def __init__(self):
        dict.__init__(self)
        self.id = 0
    ##########################################

    def __setitem__(self, name, options):
        newopts = (self.id, options[0], options[1], options[2], self.checkValue(
            options, options[3]), options[4])
        dict.__setitem__(self, name, newopts)
        self.id += 1

    def __getitem__(self, name):
        options = dict.__getitem__(self, name)
        return options[4]

    def checkValue(self, options, value):
        if value != None:
            if options[0] in ['str', 'string', 'char']:
                if not isinstance(value, str):
                    value = str(value)
            elif options[0] in ['int', 'integer']:
                if not isinstance(value, int):
                    if not value.isdigit():
                        raise TypeError('invalid value type')
                    value = int(value)
            elif options[0] in ['flt', 'float']:
                if not isinstance(value, float):
                    if not value.replace('.').isdigit():
                        raise TypeError('invalid value type')
                    value = float(value)
            elif options[0] in ['bool', 'boolean']:
                if not isinstance(value, bool):
                    if value.lower() in ['true', '1', 'on']:
                        value = True
                    elif value.lower() in ['false', '0', 'off']:
                        value = False
                    else:
                        raise TypeError('invalid value type')
            elif options[0] in ['file', 'dir']:
                if not isinstance(value, str):
                    raise TypeError('invalid value type')
                if options[2] == True:
                    if not isfile(value) and not isdir(value):
                        raise TypeError('path do not exist')
            else:
                raise Exception('Unknown value type')
            if options[4] != None:
                if value not in options[4]:
                    raise ValueError('Value %s not in list: %s' %
                                     (value, ', '.join(options[4])))
        return value

    def add_string(self, name, help, required=True, default=None, complete=None):
        self.__setitem__(name, ('str', help, required, default, complete))

    def add_integer(self, name, help, required=True, default=None, complete=None):
        self.__setitem__(name, ('int', help, required, default, complete))

    def add_float(self, name, help, required=True, default=None, complete=None):
        self.__setitem__(name, ('flt', help, required, default, complete))

    def add_boolean(self, name, help, required=True, default=None, complete=None):
        self.__setitem__(name, ('bool', help, required, default, complete))

    def add_path(self, name, help, required=True, default=None, complete=None):
        self.__setitem__(name, ('file', help, required, default, complete))
    ##########################################

    def set_option(self, name, value):
        if self.__contains__(name) == False:
            raise ValueError('invalid variable/option name')
        options = dict.__getitem__(self, name)
        value = self.checkValue(options[1:], value)
        dict.__setitem__(
            self, name, (options[0], options[1], options[2], options[3], value, options[5]))

    def unset_option(self, name):
        if self.__contains__(name) == False:
            raise ValueError('invalid variable/option name')
        options = dict.__getitem__(self, name)
        dict.__setitem__(
            self, name, (options[0], options[1], options[2], options[3], None, options[5]))

    def get_missing_options(self):
        missing_options = []
        for option_name, option_def in self.items():
            if option_def[3] == True and option_def[4] == None:
                missing_options.append(option_name)
        return missing_options

    def get_option_id(self, name):
        if self.__contains__(name) == False:
            raise ValueError('invalid variable/option name')
        options = dict.__getitem__(self, name)
        return options[0]

    def get_option_type(self, name):
        if self.__contains__(name) == False:
            raise ValueError('invalid variable/option name')
        options = dict.__getitem__(self, name)
        return options[1]

    def get_option_help(self, name):
        if self.__contains__(name) == False:
            raise ValueError('invalid variable/option name')
        options = dict.__getitem__(self, name)
        return options[2]

    def get_option_require(self, name):
        if self.__contains__(name) == False:
            raise ValueError('invalid variable/option name')
        options = dict.__getitem__(self, name)
        return options[3]

    def get_option_value(self, name):
        if self.__contains__(name) == False:
            raise ValueError('invalid variable/option name')
        options = dict.__getitem__(self, name)
        return options[4]

    def get_option_complete(self, name):
        if self.__contains__(name) == False:
            raise ValueError('invalid variable/option name')
        options = dict.__getitem__(self, name)
        return options[5]
