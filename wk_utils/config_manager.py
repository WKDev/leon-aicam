import os
import configparser
import traceback
from datetime import datetime

config_dir = "."
config_path = os.path.join(config_dir, f'config.ini')


def load_config():
    cf = SafeConfigParser()

    if not os.path.exists(config_path):
        # Create a default config object with default values
        config = configparser.ConfigParser()
        config['common'] = {
            'cap_width':'640',
            'cap_height':'480',
        }

        # Write the default config to the file
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        with open(config_path, 'w') as configfile:
            config.write(configfile)
        with open(os.path.join(os.path.dirname(config_path), f'{datetime.now().strftime("%y%m%dT%H%M")}_config.ini'), 'w') as configfile:
            config.write(configfile)
        with open(os.path.join(os.path.dirname(config_path), f'config_bak.ini'), 'w') as configfile:
            config.write(configfile)

        print(f"Default config file created at {config_dir}")

        cf.read(config_path)
    else:
        # Load the config file if it exists
        cf.read(config_path)
        # print(f"Config file loaded successfully from {config_pa®th}")
    return cf


class SafeConfigParser():
    def __init__(self):
        self.base = configparser.ConfigParser()
        self.backup = configparser.ConfigParser()
        # self.lg = init_logging('safe_config_parser')

    def read(self, path):
        try:
            return self.base.read(path)
        except configparser.NoSectionError:
            print(
                f'no {path} found in current config, finding the section from backup config')
            try:
                return self.backup.read(path)
            except:
                print(
                    f'no {path} found in backup config, returning empty string')

                return ''

    def get(self, section, option, *, raw=False, vars=None):
        try:
            return self.base.get(section, option)
        except configparser.NoSectionError:
            print(
                f'no {section=} {option=}found in current config, finding the section from backup config')
            try:
                return self.backup.get(section, option)
            except:
                print(
                    f'no {section=} {option=}found in backup config, returning empty string')

                return ''

    def getboolean(self, section, option, *, raw=False, vars=None):
        try:
            return self.base.getboolean(section, option)
        except configparser.NoSectionError:
            print(
                f'no {section=} {option=}found in current config, finding the section from backup config')
            try:
                return self.backup.getboolean(section, option)
            except:
                print(
                    f'no {section=} {option=}found in backup config, returning empty string')

                return ''

    def getint(self, section, option, *, raw=False, vars=None):
        try:
            return self.base.getint(section, option)
        except configparser.NoSectionError:
            print(
                f'no {section=} {option=}found in current config, finding the section from backup config')
            try:
                return self.backup.getint(section, option)
            except:
                print(
                    f'no {section=} {option=}found in backup config, returning empty string')

                return ''

    def getfloat(self, section, option, *, raw=False, vars=None):
        try:
            return self.base.getfloat(section, option)
        except configparser.NoSectionError:
            print(
                f'no {section=} {option=}found in current config, finding the section from backup config')
            try:
                return self.backup.getfloat(section, option)
            except:
                print(
                    f'no {section=} {option=}found in backup config, returning empty string')

                return ''
