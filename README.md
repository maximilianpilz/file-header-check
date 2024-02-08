# file-header-check

GitHub action to check whether specified files contain a header matching a given regular expression.

## Usage

An example usage is as follows:

```
- uses: maximilianpilz/file-header-check@v1
  with:
    config: 'config/config_file'
    config-encoding: 'utf-8'
```

The parameter "config" specifies the config file that contains information
of which pathnames to check against which regular expression of a file header.
The "config-encoding" parameter specifies the encoding of the aforementioned
"config" file to let the action read in the config file properly.

An optional "log-level" parameter can be given as follows:

```
- uses: maximilianpilz/file-header-check@v1
  with:
    config: 'config/config_file'
    config-encoding: 'utf-8'
    log-level: 'DEBUG'
```

whereas the allowed values are "CRITICAL", "FATAL", "ERROR", "WARN", "WARNING", "INFO", "DEBUG", "NOTSET".

### Content of the config file

The config file has to be in a format compatible with https://docs.python.org/3/library/configparser.html .

An example for the same header pattern
being checked in all ".java" files is as follows:

```
[whatever]
file_name_pattern: **/*.java
file_header_encoding: utf-8
header_regex_file: config/header
header_regex_file_encoding: utf-8
```

An example for different header patterns
being checked in ".py" and ".java" files is as follows:

```
[whatever]
file_name_pattern: **/*.java
file_header_encoding: utf-8
header_regex_file: config/header
header_regex_file_encoding: utf-8

[next]
file_name_pattern: **/*.py
file_header_encoding: utf-8
header_regex_file: config/header
header_regex_file_encoding: utf-8
```

Whereas "file_name_pattern" is a Unix shell pattern to get all the pathnames
and from those all the files to check
against the "header_regex_file" regular expression.
"header_regex_file" shall contain a Python style regular expression
for the header expected at the beginning of each of the files matching
file_name_pattern.
The encodings are necessary to correctly read in all the files and are
required, they do not have a default.
There can be an arbitrary amount of config sections in the config file
and "file_name_pattern"s are allowed to overlap.

### Content of the header regex file

The file specified via "header_regex_file" in the config file shall contain
a Python regular expression (see https://docs.python.org/3/library/re.html) that is supposed to match with the header
that is supposed to be in each file matching "file_name_pattern".

For example, it could look like this:

```
"""
This file is part of my project.
Copyright \(C\) [0-9]{4}(, [0-9]{4})? my name

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
```


## Disclaimer

This GitHub action is currently not security hardened, and 
it is advised to only use it when you are fully aware of all
the potential consequences of missing security hardening.
Security hardening might be done in a future version without any 
guarantee.

## Licensing

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
