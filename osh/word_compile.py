#!/usr/bin/env python2
"""
word_compile.py

This is called the "compile" stage because it happens after parsing, but it
doesn't depend on any values at runtime.
"""
from _devbuild.gen.id_kind_asdl import Id, Id_str
from _devbuild.gen.syntax_asdl import (
    Token, class_literal_term, class_literal_term_t,
)
from core.pyutil import stderr_line
from frontend import consts
from osh import string_ops

from typing import Optional


def EvalCharLiteralForRegex(tok):
  # type: (Token) -> Optional[class_literal_term_t]
  """For regex char classes.

  Similar logic as below.
  """
  id_ = tok.id
  value = tok.val

  if id_ == Id.Char_OneChar:
    c = value[1]
    s = consts.LookupCharC(c)
    return class_literal_term.ByteSet(s, tok.span_id)

  elif id_ == Id.Char_Hex:
    s = value[2:]
    i = int(s, 16)
    return class_literal_term.ByteSet(chr(i), tok.span_id)

  elif id_ in (Id.Char_Unicode4, Id.Char_Unicode8):
    s = value[2:]
    i = int(s, 16)
    return class_literal_term.CodePoint(i, tok.span_id)

  elif id_ == Id.Expr_Name:  # [b B] is NOT mutated
    return None

  else:
    raise AssertionError(Id_str(id_))


# TODO: Strict mode syntax errors:
#
# \x is a syntax error -- needs two digits (It's like this in C)
# \0777 is a syntax error -- we shouldn't do modulus
# \d could be a syntax error -- it is better written as \\d

def EvalCStringToken(tok):
  # type: (Token) -> Optional[str]
  """
  This function is shared between echo -e and $''.

  $'' could use it at compile time, much like brace expansion in braces.py.
  """
  id_ = tok.id
  value = tok.val

  if id_ == Id.Char_Literals:
    return value

  elif id_ == Id.Char_BadBackslash:
    if 1:
      # Either \A or trailing \ (A is not a valid backslash escape)
      # TODO: add location info with tok.span_id (errfmt), and make it an rror
      # when strict_backslash is on.  I USED this to fix a refactored regex!
      # Extract from [[ ]] and fix backslashes.
      stderr_line(
          'warning: Invalid backslash escape in C-style string: %r' % value)
      #from core.pyerror import e_die
      #e_die('Invalid backslash escape %r', value, span_id=tok.span_id)
    return value

  elif id_ == Id.Char_OneChar:
    c = value[1]
    return consts.LookupCharC(c)

  elif id_ == Id.Char_Stop:  # \c returns a special sentinel
    return None

  elif id_ in (Id.Char_Octal3, Id.Char_Octal4):
    if id_ == Id.Char_Octal3:  # $'\377'
      s = value[1:]
    else:                      # echo -e '\0377'
      s = value[2:]

    i = int(s, 8)
    if i >= 256:
      i = i % 256
      # NOTE: This is for strict mode
      #raise AssertionError('Out of range')
    return chr(i)

  elif id_ == Id.Char_Hex:
    s = value[2:]
    i = int(s, 16)
    return chr(i)

  elif id_ in (Id.Char_Unicode4, Id.Char_Unicode8):
    s = value[2:]
    i = int(s, 16)
    #util.log('i = %d', i)
    return string_ops.Utf8Encode(i)

  else:
    raise AssertionError()
