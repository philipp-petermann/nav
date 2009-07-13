#
# Copyright (C) 2009 UNINETT AS
#
# This file is part of Network Administration Visualized (NAV).
#
# NAV is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License version 2 as published by the Free
# Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.  You should have received a copy of the GNU General Public
# License along with NAV. If not, see <http://www.gnu.org/licenses/>.
#

"""Configuration parser for Geomap.

Parses Geomap's peculiar configuration file format.

The format is inspired by Python, with indentation indicating block
structure and colon used to begin a block.  The parse_conf and
parse_conf_file functions only parse this block structure, leaving the
contents of each line unparsed.  The functions are thus quite generic
and may be used in any case where one is interested in parsing
Python-ish block structure.

The rest of the functions read and parse the Geomap configuration
using the functions mentioned above for parsing the basic syntax.

The configuration is read when this module is loaded and is accessible
by the function get_configuration.

"""

import os
import re
import logging

import nav
from nav.errors import ConfigurationError

from nav.web.geomap.utils import *


logger = logging.getLogger('nav.web.geomap.conf')

_config = None


class ConfigurationSyntaxError(ConfigurationError):
    def __init__(self, msg, filename, linenr):
        self.msg = msg
        self.filename = filename
        self.linenr = linenr
    def __str__(self):
        return 'Syntax error in configuration file %s on line %d: %s' % \
            (self.filename, self.linenr, self.msg)


class ConfigurationEvaluationError(ConfigurationError):
    def __init__(self, expression, original_exception, filename, linenr):
        self.expression = expression
        self.original_exception = original_exception
        self.filename = filename
        self.linenr = linenr
    def __str__(self):
        return ('Exception when evaluating expression "%s" in configuration '
                'file %s on line %d: %s') % \
                (self.expression, self.filename, self.linenr,
                 self.original_exception)


def parse_conf(lines, filename):
    stack = [{'objects': [],
              'indent': 0}]
    def line_empty_p(line):
        return re.match(r'^\s*(#.*)?$', line) is not None
    def normalize_line(line):
        line = line.replace('\t', ' '*8)
        line = line.rstrip()
        return line
    def line_indent(line):
        return len(re.match(r'^ *', line).group(0))
    def current_frame():
        return stack[-1]
    def current_indent():
        return current_frame()['indent']
    def current_objlist():
        return current_frame()['objects']
    def make_block(line, linenr):
        return {'type': 'block',
                'text': line,
                'objects': [],
                'linenr': linenr}
    def make_line(line, linenr):
        return {'type': 'line',
                'text': line,
                'linenr': linenr}
    def add_line(line, linenr):
        line = line.lstrip()
        if line[-1] == ':':
            obj = make_block(line[:-1], linenr)
        else:
            obj = make_line(line, linenr)
        current_objlist().append(obj)
    def last_object():
        if len(current_objlist()) > 0:
            return current_objlist()[-1]
        return None
    def expect_more_indent_p():
        last = last_object()
        return (last is not None and last['type'] == 'block' and
                len(last['objects']) == 0)
    def current_level():
        if expect_more_indent_p():
            return len(stack)
        return len(stack)-1
    def push(new_indent):
        objlist = last_object()['objects']
        stack.append({'objects': objlist,
                      'indent': new_indent})
    def pop(new_indent):
        while current_indent() > new_indent:
            stack.pop()

    linenr = 0
    def error(msg):
        raise ConfigurationSyntaxError(msg, filename, linenr)

    for linenr in xrange(1, len(lines)+1):
        line = normalize_line(lines[linenr-1])
        if line_empty_p(line):
            continue
        new_indent = line_indent(line)
        if expect_more_indent_p() and new_indent > current_indent():
            push(new_indent)
        elif expect_more_indent_p():
            error('Expected more indentation')
        elif new_indent > current_indent():
            error('Unexpected increase in indentation')
        elif new_indent < current_indent():
            pop(new_indent)
            if new_indent != current_indent():
                error('New indentation of %d spaces does not match any ' +
                      'previous indentation' % new_indent)
        add_line(line, linenr)
    if expect_more_indent_p():
        error('Unexpected end of file (at start of a block)')
    pop(0)
    return current_objlist()


def parse_conf_file(filename):
    f = file(filename)
    lines = f.readlines()
    f.close()
    return parse_conf(lines, filename)


def interpret_configuration(c, filename):
    def is_variant(c_obj):
        if c_obj['type'] != 'block':
            return False
        m = re.match(r'^def variant\((.+),(.+)\)$', c_obj['text'])
        return m is not None

    def read_variant(c_obj):
        m = re.match(r'^def variant\((.+),(.+)\)$', c_obj['text'])
        identifier = m.group(1).strip()
        name = eval_or_warning(m.group(2), c_obj['linenr'])
        indicators = {}
        styles = {}
        template_files = {}
        styles['node'], styles['edge'] = {}, {}
        indicators['node'], indicators['edge'] = [], []
        for sub in c_obj['objects']:
            if is_indicator(sub):
                indicator_type,indicator = read_indicator(sub)
                if indicator_type not in indicators:
                    indicators[indicator_type] = []
                indicators[indicator_type].append(indicator)
            elif is_style(sub):
                style_type,style = read_style(sub)
                if style_type not in styles:
                    styles[style_type] = {}
                styles[style_type].update(style)
            elif is_template_file(sub):
                template_for,template_file = read_template_file(sub)
                template_files[template_for] = template_file
            else:
                warn_unknown_object(sub)
        return (identifier,
                {'identifier': identifier,
                 'name': name,
                 'indicators': indicators,
                 'styles': styles,
                 'template_files': template_files})

    def is_indicator(c_obj):
        if c_obj['type'] != 'block':
            return False
        m = re.match(r'^def indicator\((.+),(.+),(.+)\)$', c_obj['text'])
        return m is not None

    def read_indicator(c_obj):
        m = re.match(r'^def indicator\((.+),(.+),(.+)\)$', c_obj['text'])
        type = m.group(1).strip()
        property = m.group(2).strip()
        name = eval_or_warning(m.group(3), c_obj['linenr'])
        options = []
        for sub in c_obj['objects']:
            if sub['type'] != 'block':
                raise ConfigurationSyntaxError(
                    'Illegal indicator syntax (expected a block)',
                    filename, sub['linenr'])
            m = re.match(r'^if (.+)$', sub['text'])
            if m is None:
                raise ConfigurationSyntaxError(
                    'Illegal indicator syntax (expected \'if ...\')',
                    filename, sub['linenr'])
            test = m.group(1)
            result = concat_str([o['text'] for o in sub['objects']])
            value_and_label = \
                eval_or_warning(result, sub['linenr'],
                                ('','(configuration error, see log)'))
            if len(value_and_label) != 2:
                logger.warning(('Error in configuration file %s on line ' +
                                '%d: expected expression "%s" to evaluate ' +
                                'to 2-tuple, it evaluated to %s') %
                               (filename, sub['linenr'], result,
                                value_and_label))
                value_and_label = '','(configuration error, see log)'
            value,label = value_and_label
            options.append({'test': test,
                            'value': value,
                            'label': label})
        return (type,
                {'type': type,
                 'property': property,
                 'name': name,
                 'options': options})
    
    def is_template_file(c_obj):
        if c_obj['type'] == 'block':
            return False
        m = re.match(r'^template_file\((.+),(.+)\)$', c_obj['text'])
        return m is not None
        
    def read_template_file(c_obj):
        m = re.match(r'^template_file\((.+),(.+)\)$', c_obj['text'])
        template_for = m.group(1).strip()
        template_file = eval_or_warning(m.group(2), c_obj['linenr'], None)
        return (template_for,template_file)

    def is_style(c_obj):
        if c_obj['type'] == 'block':
            return False
        m = re.match(r'^style\((.+),(.+),(.+)\)$', c_obj['text'])
        return m is not None
        
    def read_style(c_obj):
        m = re.match(r'^style\((.+),(.+),(.+)\)$', c_obj['text'])
        type = m.group(1).strip()
        property = m.group(2).strip()
        value = eval_or_warning(m.group(3), c_obj['linenr'], None)
        return (type,
                {property: value})

    def warn_unknown_object(c_obj):
        logger.warning(('Error in configuration file %s: Unknown object ' +
                        '"%s" starting on line %d') %
                       filename, c_obj['text'], c_obj['linenr'])

    def eval_or_warning(expr, linenr,
                        default_value='(configuration error, see log)'):
        try:
            return conf_eval(expr, filename, linenr)
        except ConfigurationEvaluationError, e:
            logger.warning(e)
            return default_value

    variants = {}
    variant_order = []
    for c_obj in c:
        if is_variant(c_obj):
            variant_id, variant = read_variant(c_obj)
            variants[variant_id] = variant
            variant_order.append(variant_id)
        else:
            warn_unknown_object(sub)

    return {'variants': variants,
            'variant_order': variant_order}


def conf_eval(expr, filename, linenr):
    try:
        return eval(expr, {})
    except Exception, e:
        raise ConfigurationEvaluationError(expr, e, filename, linenr)


def read_configuration(filename):
    return interpret_configuration(parse_conf_file(filename),
                                   filename)


def get_configuration():
    global _config
    if _config is None:
        _config = read_configuration(os.path.join(nav.path.sysconfdir,
                                                  'geomap/config.py'))
    return _config
