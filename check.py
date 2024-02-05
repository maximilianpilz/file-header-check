"""
This file is part of file-header-check, a command-line tool and GitHub action for checking file headers.
Copyright (C) 2024 Maximilian Pilz

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; version 2.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import argparse
import configparser
import glob
import logging
import pathlib
import re
import sys

LOGGER_NAME = 'file-header-check'
LOGGER = logging.getLogger(LOGGER_NAME)


def scan(file_name_pattern: str,
         file_header_encoding: str,
         header_regex_file_name: str,
         header_regex_file_encoding: str) -> bool:
    """
    Read in each file matching the given pattern, search for a character sequence that
    matches the given regular expression, check that such sequence could be found and
    that it starts at the beginning of the file.

    :param file_name_pattern: the glob pattern for getting all the pathnames/files to check
    :param file_header_encoding: the encoding of the files to check
    :param header_regex_file_name: the file name of the file containing the regular expression
    :param header_regex_file_encoding: the encoding of the file containing the regular expression
    :return: True when the check was passed successfully by each file, False otherwise
    """

    try:
        with open(header_regex_file_name, 'rt', encoding=header_regex_file_encoding) as header_regex_file_obj:
            regex = re.compile(header_regex_file_obj.read())
    except UnicodeDecodeError:
        LOGGER.error(f'Unable to decode the file "{header_regex_file_name}" as "{header_regex_file_encoding}".')
        return False

    local_results = list()

    for file_to_scan in glob.glob(pathname=file_name_pattern,
                                  include_hidden=True,
                                  recursive=True):

        if pathlib.Path(file_to_scan).is_file():

            try:
                with open(file_to_scan, 'rt', encoding=file_header_encoding) as file_to_scan_obj:
                    match = regex.search(string=file_to_scan_obj.read())

                    if match is None:
                        # fail
                        LOGGER.error(
                            msg=f'The file {file_to_scan} '
                                f'does not contain a character sequence that matches the regex given in '
                                f'{header_regex_file_name}.')
                        local_results.append(False)
                    elif match.start() != 0:
                        # fail
                        LOGGER.error(
                            msg=f'The file {file_to_scan} '
                                f'contains a character sequence that matches the regex given in '
                                f'{header_regex_file_name}, '
                                f'but the matching character sequence is not at the beginning of the file.')
                        local_results.append(False)
                    else:
                        assert match is not None
                        assert match.start() == 0
                        # success
                        local_results.append(True)
            except UnicodeDecodeError:
                LOGGER.error(f'Unable to decode the file "{file_to_scan}" as "{file_header_encoding}".')
                return False

        else:

            LOGGER.debug(f'Ignoring the pathname "{file_to_scan}" since it is not a file.')

    return bool(local_results) and all(local_results)


def configure_logger(log_level: int) -> None:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    LOGGER.addHandler(stream_handler)
    LOGGER.setLevel(log_level)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='file-header-check',
        description='checks that files have a header matching a given regular expression',
        epilog='file-header-check in v1')

    parser.add_argument('config',
                        help='config file for determining pathnames and which regex file to use')
    parser.add_argument('-e', '--encoding',
                        help='encoding of the config file')
    parser.add_argument('-ll', '--log_level',
                        default='WARNING',
                        help='log level to use, defaults to WARNING')

    args = parser.parse_args()

    level_names_mapping = logging.getLevelNamesMapping()
    log_level_arg = args.log_level
    if log_level_arg in level_names_mapping:
        configure_logger(log_level=level_names_mapping[log_level_arg])
    else:
        # the log level was provided wrong
        configure_logger(log_level=logging.WARNING)
        LOGGER.warning(msg=f'The provided log level value "{log_level_arg}" is not allowed/invalid, '
                           f'will use the default value i.e. "WARNING" instead. '
                           f'Consider that the log level value is case sensitive.')

    config = configparser.ConfigParser()
    files = config.read(filenames=[args.config], encoding=args.encoding)

    results = list()

    for section in config.sections():
        file_name_pattern_var = config.get(section=section, option='file_name_pattern')
        file_header_encoding_var = config.get(section=section, option='file_header_encoding')
        header_regex_file_name_var = config.get(section=section, option='header_regex_file')
        header_regex_file_encoding_var = config.get(section=section, option='header_regex_file_encoding')

        results.append(scan(file_name_pattern=file_name_pattern_var,
                            file_header_encoding=file_header_encoding_var,
                            header_regex_file_name=header_regex_file_name_var,
                            header_regex_file_encoding=header_regex_file_encoding_var))

    overall_result = (bool(results) and all(results))

    if overall_result:
        sys.exit(0)
    else:
        sys.exit(1)
