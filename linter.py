#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Bartosz Kruszczynski
# Copyright (c) 2015 Bartosz Kruszczynski
#
# License: MIT
#

"""This module exports the Reek plugin class."""

from SublimeLinter.lint import RubyLinter
import re


class Reek(RubyLinter):
    """Provides an interface to reek."""

    defaults = {
        'selector': 'source.ruby - text.html - text.haml'
    }

    cmd = ('ruby', '-S', 'reek', '-s', '--no-color',
           '--no-progress', '--no-documentation', '${file}')
    regex = r'^.+?:(?P<line>\d+): (?P<error>\w+): (?P<message>.+)$'
    tempfile_suffix = 'rb'

    def split_match(self, match):
        """Add near detail to error dict."""

        error = super().split_match(match)
        error['near'] = self.search_token(error['message'])

        return error

    def search_token(self, message):
        """Search text token to be highlighted."""

        # First search for variable name enclosed in single quotes
        m = re.search("'.*'", message)

        # If there's no variable name search for nil-check message
        if m is None:
            m = re.search(r'nil(?=-check)', message)

        # If there's no nil-check search for method name that comes after a `#`
        if m is None:
            m = re.search(r'(?<=#)\S+', message)

        return m.group(0) if m else None
