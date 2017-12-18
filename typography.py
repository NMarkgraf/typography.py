#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
  Quick-Typographie-Filter: typography.py

  (C)opyleft in 2017 by Norman Markgraf (nmarkgraf@hotmail.com)

  Release:
  ========
  0.1 - 25.10.2017 (nm) - Erste Version
  0.2 - 25.10.2017 (rm) - Verbesserte Version
  0.3 - 10.11.2017 (nm) - Erweiterte Version
  0.4 - 28.11.2017 (nm) - Erweiterte Version
  0.5 - 08.12.2017 (nm) - Erste Versuche mit mbox und xspace
  0.6 - 11.12.2017 (nm) - "thinspace " statt "\," in LaTeX

  WICHTIG:
  ========
    Benoetigt python3 !
    -> https://www.howtogeek.com/197947/how-to-install-python-on-windows/
    oder
    -> https://www.youtube.com/watch?v=dX2-V2BocqQ
    Bei *nix und macOS Systemen muss diese Datei als "executable" markiert
    sein!
    Also bitte ein
      > chmod a+x typography.py
   ausfuehren!

  LaTeX:
  ======
  Der Befehl "xspace" benötigst das Paket "xspace".
  Also bitte "usepackage{xspace}" einbauen!
  Ab Version 0.6 wird von "\," auf "thinspace" umgestellt.

  Informationen zur Typographie:
  ==============================
  URL: https://www.korrekturen.de/fehler_und_stilblueten/die_sieben_haeufigsten_typographie-suenden.shtml
  URL: http://www.typolexikon.de/abstand/
  URL: https://de.wikipedia.org/wiki/Schmales_Leerzeichen


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

'''


import panflute as pf

thinSpaceLaTeX = "\\thinspace{}"  # Schmales Leerzeichen in LaTeX equiv. "\,"
thinSpaceHTML = "&thinsp;"      # Schmales Leerzeichen in HTML
xspace = "\\xspace{}"

'''
    RawInline fuer LaTeX und HTML vorbereiten
'''
inlineLatex = pf.RawInline(thinSpaceLaTeX, format="latex")
succLatex = pf.RawInline(xspace, format="latex")
inlineHTML = pf.RawInline(thinSpaceHTML, format="html")
succHTML = pf.RawInline("", format="html")


def latexBlock(first, second):
    return pf.RawInline("\mbox{"+first+thinSpaceLaTeX+second+"}"+xspace)


def latexBlockThree(first, second, third, succtxt="", succ=""):
    return pf.RawInline("\mbox{"+first+thinSpaceLaTeX+second+thinSpaceLaTeX+third+"}"+xspace)
    # return [pf.Str(first), inline, pf.Str(second), inline, pf.Str("m."+succtxt), succ]


def action(elem, doc):
    '''
        Der eigentliche Filter
    '''
    '''
        Waehle für die Zielsprache (LaTeX / HTML) die
        passende RawInline Zeile aus
    '''
    inline = inlineLatex
    succ = succLatex
    if doc.format == "html":
        inline = inlineHTML
        succ = succHTML

    '''
        Der Filter
    '''
    if isinstance(elem, pf.Str):
        txtlen = len(elem.text)
        '''
            Hier wird:
            u.a. / z.B. / d.h. / c.p. / s.u. / s.o.
            angepasst!
        '''
        text = elem.text
        succtxt = ""
        pretxt = ""
        '''
            Manchmal steht noch ein ':', ';' oder ','
            dahinter. Finden und dennoch nutzen.
        '''
        if (txtlen == 6):
            if (text[1] == "(") & (text[-1] == ")"):
                pretxt = "("
                succtxt = ")"
                text = text[1:5]
                txtlen = 4
        if (txtlen == 5):
            if (text[1] == "("):
                pretxt = "("
                text = text[1:]
                txtlen=4
            if (text[-1] == ":"):
                succtxt = ":"
                text = text[:4]
                txtlen = 4
            if (text[-1] == ","):
                succtxt = ","
                text = text[:4]
                txtlen = 4
            if (text[-1] == ";"):
                succtxt = ";"
                text = text[:4]
                txtlen = 4

        if (txtlen == 4):
            if (text == "u.a."):
                return [pf.Str(pretxt+"u."), inline, pf.Str("a."+succtxt), succ]
            if (text == "z.B."):
                return [pf.Str("z."), inline, pf.Str("B."+succtxt), succ]
            if (text == "d.h."):
                return [pf.Str("d."), inline, pf.Str("h."+succtxt), succ]
            if (text == "c.p."):
                return [pf.Str("c."), inline, pf.Str("p."+succtxt), succ]
            if (text == "s.u."):
                return [pf.Str("s."), inline, pf.Str("u."+succtxt), succ]
            if (text == "s.o."):
                return [pf.Str("s."), inline, pf.Str("o."+succtxt), succ]
            if (text == "m.W."):
                return [pf.Str("m."), inline, pf.Str("W."+succtxt), succ]
            if (text == "s.S."):
                return [pf.Str("s."), inline, pf.Str("S."+succtxt), succ]
            if (text == "o.S."):
                return [pf.Str("o."), inline, pf.Str("S."+succtxt), succ]
            if (text == "d.h."):
                return [pf.Str("d."), inline, pf.Str("h."+succtxt), succ]          


        '''
            Hier wird:
            u.v.m. / i.d.R
            angepasst!
        '''
        if (txtlen == 6):
            if (elem.text == "u.v.m."):
                return latexBlockThree("u.", "v.", "m.", succ=succ)
            if (elem.text == "i.d.R."):
                return latexBlockThree("i.", "d.", "R.", succ=succ)
            if (elem.text == "M.a.W."):
                return latexBlockThree("M.", "a.", "W.", succ=succ)
            if (elem.text == "m.a.W."):
                return latexBlockThree("m.", "a.", "W.", succ=succ)

        if (txtlen == 7):
            if (elem.text == "i.d.R.:"):
                return latexBlockThree("i.", "d.", "R.:", succ=succ)
            if (elem.text == "M.a.W.:"):
                return latexBlockThree("M.", "a.", "W.:", succ=succ)
            if (elem.text == "m.a.W.:"):
                return latexBlockThree("m.", "a.", "W.:", succ=succ)

        '''
            Hier wird
            Text/ Text -> Text\,/
            angepasst!
        '''
        if txtlen > 2:
            if (elem.text[-1] == "/") and isinstance(elem.next, pf.Space):
                return [pf.Str(elem.text[:-1]), inline, pf.Str("/")]
        if (elem.text == "/") and isinstance(elem.prev, pf.Para):
            return [inline, pf.Str("/")]
    if isinstance(elem, pf.Space):
        '''
            Hier wird
            Text/ Text -> Text\,/ Text
            angepasst!
        '''
        if (isinstance(elem.next, pf.Str) and elem.next.text[0] == "/"):
            return inline
        '''
        '''
        if (isinstance(elem.prev, pf.Str)):
            if elem.prev.text[-1] == "/":
                return inline
            '''
               Hier wird
               u. a. / z. B. / Z. B. / d. h. / D. h. / u. "A. / c. p.
               angepasst!
            '''
            if (isinstance(elem.next, pf.Str)) and (len(elem.prev.text) >= 2) and (len(elem.next.text) >= 2):
                prevStr = elem.prev.text[-2:]  # letzen zwei Zeichen
                nextStr = elem.next.text[0:2]  # naechsten zwei Zeichen
                if (prevStr[1] == ".") and (nextStr[1] == "."):
                    if (prevStr[0] in ["u", "z", "Z", "d", "D", "p", "c", "s", "m"]):  # u. z. Z. d. p. u. c. m.
                        if (nextStr[0] in ["a", "B", "h", "a", "Ä", "p", "o", "u", "W"]):  # a. B. B. h. a. Ä p. W.
                            return inline


def main():
    pf.toJSONFilter(action=action)


if __name__ == "__main__":
    main()
