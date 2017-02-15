# -*- coding: utf-8 -*-
"""
Command used to generate the violations reports
"""

import os
import subprocess
import sys

from django.core.management.base import BaseCommand, CommandError
from pylint import lint
from pylint.reporters.text import ParseableTextReporter as Reporter
from django.conf import settings


class Command(BaseCommand):
    """
    Checks for violation in code.
    """
    help = 'Checks for violation in code'

    def add_arguments(self, parser):
        """
        Add arguments to violations command.
        :param parser: Argument parser.
        """
        parser.add_argument('--no-pylint', action='store_false',
                            help='Disable pylint violations check')
        parser.add_argument('--no-flake8', action='store_false',
                            help='Disable flake8 violations check')
        parser.add_argument('--max', type=int,
                            help='Maximum number of acceptable pylint violations')

    def handle(self, *args, **options):
        """
        Command execution.
        """
        count = 0
        if options['no_pylint']:
            count += self.handle_pylint()

        if options['no_flake8']:
            count += self.handle_flake8()

        msg = None
        if options['max'] and count > options['max']:
            msg = 'Maximum number of violation exceeded. Expecting %i got %i.' % (
                options['max'], count)
        if msg:
            raise CommandError(msg)

    def handle_pylint(self):
        """
        Handle pylint violations.
        :return: The number of violations.
        """
        config_file = os.path.join(settings.BASE_DIR, 'pylint.ini')
        out_file_name = os.path.join(settings.BASE_DIR, 'reports', 'pylint.report')
        if not os.path.exists(os.path.dirname(out_file_name)):
            os.makedirs(os.path.dirname(out_file_name))
        output = open(out_file_name, 'w')
        args = ["--rcfile=%s" % config_file, settings.BASE_DIR]
        run = lint.Run(args, reporter=Reporter(output=output), exit=False)
        output.close()

        lint_count = 0
        for key in run.linter.stats['by_msg']:
            lint_count += run.linter.stats['by_msg'][key]
        self.stdout.write('pylint found %i violations' % lint_count)
        return lint_count

    def handle_flake8(self):
        """
        Handle pep8, pyflakes and complexity violations
        :return: The number of violations.
        """
        config_file = os.path.join(settings.BASE_DIR, 'flake8.ini')
        output_file = os.path.join(settings.BASE_DIR, 'reports', 'flake8.report')

        subprocess.Popen([sys.executable, '-m', 'flake8',
                          '--config=%s' % config_file,
                          '--output-file=%s' % output_file,
                          settings.BASE_DIR]).communicate()

        flake8_count = sum(1 for _ in open(output_file))
        self.stdout.write('flake8 found %i violations' % flake8_count)
        return flake8_count
