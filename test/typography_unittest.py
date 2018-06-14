#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
  Quick-Typographie-Filter unit test: typography_unittest.py

  (C)opyleft in 2018 by Norman Markgraf (nmarkgraf@hotmail.com)

  Release:
  ========
  0.1   - 01.04.2018 (nm) - Erste Version
  0.2   - 14.06.2018 (nm) - Kleine Updates für $ und % im LaTeX.


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


class StyleTest(unittest.TestCase):

    def test_makeInline_InstanceHTML(self):
        input = ("xxx", "yyy")
        result = pf.RawInline
        self.assertIsInstance(makeInline(input, "html"), result)


    def test_makeInline_InstanceLaTeX(self):
        input = ("xxx", "yyy")
        result = pf.RawInline
        self.assertIsInstance(makeInline(input, "latex"), result)


    def test_makeInline_InstanceBeamer(self):
        input = ("xxx", "yyy")
        result = pf.RawInline
        self.assertIsInstance(makeInline(input, "beamer"), result)


    def test_makeInline_FormatHTML(self):
        input = ("xxx", "yyy")
        result = "html"
        self.assertEqual(makeInline(input, "html").format, result)


    def test_makeInline_FormatLaTeX(self):
        input = ("xxx", "yyy")
        result = "latex"
        self.assertEqual(makeInline(input, "latex").format, result)


    def test_makeInline_FormatBeamer(self):
        input = ("xxx", "yyy")
        result = "latex"
        self.assertEqual(makeInline(input, "beamer").format, result)


    def test_makeInline_OutputHTML2(self):
        input = ("xxx", "yyy")
        result = "xxx&thinsp;yyy"
        self.assertEqual(makeInline(input, "html").text, result)


    def test_makeInline_OutputHTML3(self):
        input = ("xxx", "yyy", "zzz")
        result = "xxx&thinsp;yyy&thinsp;zzz"
        self.assertEqual(makeInline(input, "html").text, result)


    def test_makeInline_OutputLaTeX2(self):
        input = ("xxx", "yyy")
        result = "\\mbox{xxx\\thinspace{}yyy}\\xspace{}"
        self.assertEqual(makeInline(input, "latex").text, result)


    def test_makeInline_OutputLaTeX3(self):
        input = ("xxx", "yyy", "zzz")
        result = "\\mbox{xxx\\thinspace{}yyy\\thinspace{}zzz}\\xspace{}"
        self.assertEqual(makeInline(input, "latex").text, result)

    def test_makeInline_OutputLaTeX4(self):
        """Teste Prozentzeichen.

        Zwischen 50% sollte ein kurzes Leerzeichen. Aber dafür muss das Prozentzeichen
        konvertiert werden in "\%", damit es nicht als LaTeX-Kommentarzeichen gewertet wird!
        """
        input = ("50", "%")
        result = "\\mbox{50\\thinspace{}\%}\\xspace{}"
        self.assertEqual(makeInline(input, "latex").text, result)

    def test_makeInline_OutputLaTeX5(self):
        """Teste Dollarzeichen.

        Zwischen 50$ sollte ein kurzes Leerzeichen. Aber dafür muss das Dollarzeichen
        konvertiert werden in "\$", damit es nicht als LaTeX-Zeichen gewertet wird!
        """
        input = ("50", "$")
        result = "\\mbox{50\\thinspace{}\$}\\xspace{}"
        self.assertEqual(makeInline(input, "latex").text, result)


    def test_makeInline_OutputBeamer2(self):
        input = ("xxx", "yyy")
        result = "\\mbox{xxx\\thinspace{}yyy}\\xspace{}"
        self.assertEqual(makeInline(input, "beamer").text, result)


    def test_makeInline_OutputBeamer3(self):
        input = ("xxx", "yyy", "zzz")
        result = "\\mbox{xxx\\thinspace{}yyy\\thinspace{}zzz}\\xspace{}"
        self.assertEqual(makeInline(input, "beamer").text, result)


    def test_makeLaTeXEscapes1(self):
        str = "$"
        result = "\\$"
        self.assertEqual(makeLaTeXEscapes(str), result)


    def test_makeLaTeXEscapes2(self):
        str = "%"
        result = "\\%"
        self.assertEqual(makeLaTeXEscapes(str), result)


    def test_makeLaTeXEscapes3(self):
        str = "US-$"
        result = "US-\\$"
        self.assertEqual(makeLaTeXEscapes(str), result)


    def test_isThisSpace1(self):
        self.assertTrue(isThisSpace(pf.Space()))


    def test_isThisSpace2(self):
        self.assertFalse(isThisSpace(pf.Str("")))


    def test_isThisString1(self):
        self.assertTrue(isThisString(pf.Str("")))


    def test_isThisString2(self):
        self.assertFalse(isThisString(pf.Space()))


if __name__ == "__main__":
    unittest.main()
