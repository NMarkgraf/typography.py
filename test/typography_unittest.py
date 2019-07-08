#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
  Quick-Typographie-Filter unit test: typography_unittest.py

  (C)opyleft in 2018 by Norman Markgraf (nmarkgraf@hotmail.com)

  Release:
  ========
  0.1   - 01.04.2018 (nm) - Erste Version
  0.2   - 14.06.2018 (nm) - Kleine Updates für $ und % im LaTeX.
  0.3   - 08.07.2019 (nm) - Code Refactor


  WICHTIG:
  ========
    Benoetigt python3 !
    -> https://www.howtogeek.com/197947/how-to-install-python-on-windows/
    oder
    -> https://www.youtube.com/watch?v=dX2-V2BocqQ

  RUN THE TESTS:
  ==============
  Um die unit tests auszuführen kann man im Terminal den Befehl

    > python3 -m unittest test/style_unittest.py

  im Hauptverzeichnis des Projektes eingeben!

  Lizenz:
  =======
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.


  "Errare (Errasse) humanum est, sed in errare (errore) perseverare diabolicum."

    -- Cicero

'''

# import sys
import unittest

# sys.path.append('..')
import panflute as pf  # panflute fuer den pandoc AST
from typography import *

import io as io


class StyleTest(unittest.TestCase):

    def test_makeInline_InstanceHTML(self):
        input = ("xxx", "yyy")
        result = pf.RawInline
        self.assertIsInstance(make_inline(input, "html"), result)


    def test_makeInline_InstanceLaTeX(self):
        input = ("xxx", "yyy")
        result = pf.RawInline
        self.assertIsInstance(make_inline(input, "latex"), result)


    def test_makeInline_InstanceBeamer(self):
        input = ("xxx", "yyy")
        result = pf.RawInline
        self.assertIsInstance(make_inline(input, "beamer"), result)


    def test_makeInline_FormatHTML(self):
        input = ("xxx", "yyy")
        result = "html"
        self.assertEqual(make_inline(input, "html").format, result)


    def test_makeInline_FormatLaTeX(self):
        input = ("xxx", "yyy")
        result = "latex"
        self.assertEqual(make_inline(input, "latex").format, result)


    def test_makeInline_FormatBeamer(self):
        input = ("xxx", "yyy")
        result = "latex"
        self.assertEqual(make_inline(input, "beamer").format, result)


    def test_makeInline_OutputHTML2(self):
        input = ("xxx", "yyy")
        result = "xxx&thinsp;yyy"
        self.assertEqual(make_inline(input, "html").text, result)


    def test_makeInline_OutputHTML3(self):
        input = ("xxx", "yyy", "zzz")
        result = "xxx&thinsp;yyy&thinsp;zzz"
        self.assertEqual(make_inline(input, "html").text, result)


    def test_makeInline_OutputLaTeX2(self):
        input = ("xxx", "yyy")
        result = "\\mbox{xxx\\thinspace{}yyy}\\xspace{}"
        self.assertEqual(make_inline(input, "latex").text, result)


    def test_makeInline_OutputLaTeX3(self):
        input = ("xxx", "yyy", "zzz")
        result = "\\mbox{xxx\\thinspace{}yyy\\thinspace{}zzz}\\xspace{}"
        self.assertEqual(make_inline(input, "latex").text, result)

    def test_makeInline_OutputLaTeX4(self):
        """Teste Prozentzeichen.

        Zwischen 50% sollte ein kurzes Leerzeichen. Aber dafür muss das Prozentzeichen
        konvertiert werden in "\%", damit es nicht als LaTeX-Kommentarzeichen gewertet wird!
        """
        input = ("50", "%")
        result = "\\mbox{50\\thinspace{}\%}\\xspace{}"
        self.assertEqual(make_inline(input, "latex").text, result)

    def test_makeInline_OutputLaTeX5(self):
        """Teste Dollarzeichen.

        Zwischen 50$ sollte ein kurzes Leerzeichen. Aber dafür muss das Dollarzeichen
        konvertiert werden in "\$", damit es nicht als LaTeX-Zeichen gewertet wird!
        """
        input = ("50", "$")
        result = "\\mbox{50\\thinspace{}\$}\\xspace{}"
        self.assertEqual(make_inline(input, "latex").text, result)


    def test_makeInline_OutputBeamer2(self):
        input = ("xxx", "yyy")
        result = "\\mbox{xxx\\thinspace{}yyy}\\xspace{}"
        self.assertEqual(make_inline(input, "beamer").text, result)


    def test_makeInline_OutputBeamer3(self):
        input = ("xxx", "yyy", "zzz")
        result = "\\mbox{xxx\\thinspace{}yyy\\thinspace{}zzz}\\xspace{}"
        self.assertEqual(make_inline(input, "beamer").text, result)


    def test_makeLaTeXEscapes1(self):
        str = "$"
        result = "\\$"
        self.assertEqual(make_latex_escapes(str), result)


    def test_makeLaTeXEscapes2(self):
        str = "%"
        result = "\\%"
        self.assertEqual(make_latex_escapes(str), result)


    def test_makeLaTeXEscapes3(self):
        str = "US-$"
        result = "US-\\$"
        self.assertEqual(make_latex_escapes(str), result)


    def test_isThisSpace1(self):
        self.assertTrue(is_this_a_space(pf.Space()))


    def test_isThisSpace2(self):
        self.assertFalse(is_this_a_space(pf.Str("")))


    def test_isThisString1(self):
        self.assertTrue(is_this_a_string(pf.Str("")))


    def test_isThisString2(self):
        self.assertFalse(is_this_a_string(pf.Space()))


    def test_KurzerText(self):
        txt = """
Test/Test, 40$ oder 50%, d.h. nichts oder m.a.W. alles!
        """
        txt_json_result = """{"pandoc-api-version":[1,17,4,2],"meta":{},"blocks":[{"t":"Para","c":[{"t":"Str","c":"Test/Test,"},{"t":"Space"},{"t":"Str","c":"40$"},{"t":"Space"},{"t":"Str","c":"oder"},{"t":"Space"},{"t":"Str","c":"50%,"},{"t":"Space"},{"t":"Str","c":"d.h."},{"t":"Space"},{"t":"Str","c":"nichts"},{"t":"Space"},{"t":"Str","c":"oder"},{"t":"Space"},{"t":"Str","c":"m.a.W."},{"t":"Space"},{"t":"Str","c":"alles!"}]}]}"""
        doc_in = pf.convert_text(txt, standalone=True)
        with io.StringIO() as f:
            pf.dump(doc_in, f)
            doc_as_json = f.getvalue()

        doc_as_inputstream = io.StringIO(doc_as_json)
        doc_as_outputstream = io.StringIO()
        pf.toJSONFilter(action, input_stream=doc_as_inputstream, output_stream=doc_as_outputstream)
        self.assertEqual(doc_as_outputstream.getvalue(), txt_json_result)


if __name__ == "__main__":
    unittest.main()
