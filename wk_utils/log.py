# 220906 chanhyeokson
# simple & colorful logger

import os
import time
from natsort import natsorted
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

from wk_utils.config_manager import load_config


def init_logging(log_title=None):
    assert log_title is not None, 'log should not be empty'
    cf = load_config()
    dev_type = 'aicam'

    log_base_path = os.path.join('.', 'logs')

    if not os.path.exists(log_base_path):
        os.makedirs(log_base_path)
    log_path = os.path.join(
        log_base_path, f'{dev_type}_{log_title}_{datetime.now().strftime("%y%m%d")}.log')

    lg = logging.getLogger(log_title)
    if len(lg.handlers) > 0:
        return lg  # Logger already exists
    formatter = logging.Formatter(u'%(asctime)s [%(levelname)s] %(message)s')
    # RotatingFileHandler
    log_max_size = 10 * 1024 * 1024  # 10MB
    log_file_count = 20

    rotatingFileHandler = RotatingFileHandler(
        filename=log_path,
        maxBytes=log_max_size,
        backupCount=log_file_count
    )
    rotatingFileHandler.setFormatter(formatter)
    lg.addHandler(rotatingFileHandler)

    lg.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    lg.addHandler(ch)
    return lg


class CustomFormatter(logging.Formatter):
    # enable windows color scheme https://www.howtogeek.com/322432/how-to-customize-your-command-prompts-color-scheme-with-microsofts-colortool/
    # https: // github.com / herzog0 / best_python_logger
    color = {'black': '\033[0m', 'red': '\033[31m', 'yellow': '\033[33m', 'white': '\033[37m', 'green': '\033[32m',
             'none': '\033[0m', 'blue': '\033[34m', 'cyan': '\033[46m'}
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: color['green'] + format + reset,
        logging.INFO: color['blue'] + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class WKLogger:
    def __init__(self, title=os.path.basename(__file__), log_path=None, log_level='verbose', max_log_count=100):
        level = ['verbose', 'debug', 'info', 'warn', 'err', 'fatal']
        self.title = str(title.split(sep='.')[0])
        self.log_path = log_path
        self.COLOR = {'black': '\033[0m', 'red': '\033[31m', 'yellow': '\033[33m', 'white': '\033[37m',
                      'green': '\033[32m', 'none': '\033[0m', 'blue': '\033[34m', 'cyan': '\033[46m'}
        self.log_level = level.index(log_level)
        self.max_log_count = max_log_count

        # print(self.log_level)

    def get_filename(self):
        # 현재 날짜를 받아옵니다.
        curr_time = time.localtime()
        yr = str(curr_time.tm_year)

        # 날짜가 10보다 작은 경우, 앞에 0을 붙여줍니다.
        month = (lambda x: '0' + str(x) if x <
                 10 else str(x))(curr_time.tm_mon)
        d = (lambda x: '0' + str(x) if x < 10 else str(x))(curr_time.tm_mday)
        h = (lambda x: '0' + str(x) if x < 10 else str(x))(curr_time.tm_hour)
        _min = (lambda x: '0' + str(x) if x < 10 else str(x))(curr_time.tm_min)
        _sec = (lambda x: '0' + str(x) if x < 10 else str(x))(curr_time.tm_sec)

        ret = yr + month + d

        return ret

    def get_date_and_time(self):
        # 현재 날짜를 받아옵니다.
        curr_time = time.localtime()
        yr = str(curr_time.tm_year)[2:]

        # 날짜가 10보다 작은 경우, 앞에 0을 붙여줍니다.
        month = (lambda x: '0' + str(x) if x <
                 10 else str(x))(curr_time.tm_mon)
        d = (lambda x: '0' + str(x) if x < 10 else str(x))(curr_time.tm_mday)
        h = (lambda x: '0' + str(x) if x < 10 else str(x))(curr_time.tm_hour)
        _min = (lambda x: '0' + str(x) if x < 10 else str(x))(curr_time.tm_min)
        _sec = (lambda x: '0' + str(x) if x < 10 else str(x))(curr_time.tm_sec)

        ret = yr + month + d + '-' + h + ':' + _min + ':' + _sec

        return ret

    def auto_flush(self):
        import glob
        saved_imgs = natsorted(glob.glob(self.log_path + '*.jpg'))
        if len(saved_imgs) > self.max_log_count:
            for p in saved_imgs[:-self.max_log_count]:
                os.remove(p)
            self.info('maximum log amount reached. oldest one would be removed.')

    def add_data(self, data):
        self.auto_flush()
        with open(os.path.join(self.log_path, self.get_filename()+'.txt'), 'a') as f:
            f.write(data + '\n')

    def verbose(self, contents='', c='green', write=True):
        raw_log = '[' + self.get_date_and_time() + ']' + \
            '[' + self.title + '][VERBOSE] ' + str(contents)
        # colored_log = self.COLOR[c] +raw_log+'\033[0m'
        if write:
            self.add_data(data=raw_log)
        if self.log_level >= 0:
            print(raw_log)
    #
    # def debug(self, contents='', c='none', write=True):
    #     raw_log = '[' + self.get_date_and_time() + ']' + '[' + os.path.basename(__file__) + '][DEBUG] ' + contents
    #     colored_log = self.COLOR[c] +raw_log+'\033[0m'
    #     if write:
    #         self.add_data(data=raw_log)
    #
    #     if self.log_level >= 1:
    #         print(raw_log)

    def debug(self, contents='', c='blue', write=True):
        raw_log = '[' + self.get_date_and_time() + ']' + \
            '[' + self.title + '][DEBUG] ' + str(contents)
        colored_log = self.COLOR[c] + raw_log + '\033[0m'
        if write:
            self.add_data(data=raw_log)
        if self.log_level <= 2:
            print(colored_log)

    def info(self, contents='', c='green', write=True):
        raw_log = '[' + self.get_date_and_time() + ']' + \
            '[' + self.title + '][INFO] ' + str(contents)
        colored_log = self.COLOR[c] + raw_log + '\033[0m'
        if write:
            self.add_data(data=raw_log)
        if self.log_level <= 3:
            print(colored_log)

    def warn(self, contents='', c='yellow', write=True):
        raw_log = '['+self.get_date_and_time()+']'+'['+self.title + \
            '][WARN] ' + str(contents)
        colored_log = self.COLOR[c] + raw_log+'\033[0m'
        if write:
            self.add_data(data=raw_log)
        if self.log_level <= 4:
            print(colored_log)

    def err(self, contents='', c='red', write=True):
        raw_log = '['+self.get_date_and_time()+']'+'['+self.title + \
            '][ERROR] ' + str(contents)
        colored_log = self.COLOR[c] + raw_log + '\033[0m'
        if write:
            self.add_data(data=raw_log)
        if self.log_level <= 5:
            print(colored_log)


if __name__ == '__main__':
    lg = WKLogger(log_path='/')

    lg.verbose('verbose')
    lg.debug('debug')
    lg.info('info')
    lg.warn('warn')
    lg.err('err')
