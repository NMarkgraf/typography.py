#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
  Quick-Typographie-Filter: typography.py

  (C)opyleft in 2017/18 by Norman Markgraf (nmarkgraf@hotmail.com)

  Release:
  ========
  0.1   - 25.10.2017 (nm) - Erste Version
  0.2   - 25.10.2017 (rm) - Verbesserte Version
  0.3   - 10.11.2017 (nm) - Erweiterte Version
  0.4   - 28.11.2017 (nm) - Erweiterte Version
  0.5   - 08.12.2017 (nm) - Erste Versuche mit mbox und xspace
  0.6   - 11.12.2017 (nm) - "thinspace " statt "\," in LaTeX
  0.7   - 17.12.2017 (se) - Neue Abkürzungen eingeführt.
  0.8   - 18.12.2017 (nm) - Teilweise Umstellen auf RegEx.
  0.9   - 19.12.2017 (nm) - Noch weiter auch RegEx umgestellt.
  0.9.1 - 18.01.2018 (nm) - Ausdrücke wie "(I/ II)" wurden nicht richtig erkannt.
                            Ergebnis "I/ II)"! - gefixed!
  0.9.2 - 08.02.2018 (nm) - Jetzt wird auf "z.~B." etc. erkannt und korrigiert.

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
import re as re
import logging

# create logger with 'spam_application'
logging.basicConfig(filename='typography.log', level=logging.ERROR)

thinSpaceLaTeX = "\\thinspace{}"  # Schmales Leerzeichen in LaTeX equiv. "\,"
thinSpaceHTML = "&thinsp;"      # Schmales Leerzeichen in HTML
xspace = "\\xspace{}"

'''
 Dieses Pattern sollte
 x.y. / (x.y. / (x.y.: / (x.y.) / x.y.: ...
 für alle Buchstaben x und y abdecken.
'''
pattern1 = "([\(,\[,<,\{]?\w\.)(?:~?)(\w\.[\),\],>]?[:,\,,\.,\!,\?]?[\),\],\},>]?)"

'''
 Dieses Pattern sollte alle / am Ende eines Strings finden.
'''
pattern2 = "([\w|\(|\[|\{]+)\/$"

pattern3a = "([\(,\[,<,\{]?\w\.)"
pattern3b = "^(\w\.[\),\],>]?[:,\,,\.,\!,\?]?[\),\],\},>]?)$"


recomp1 = re.compile(pattern1)

recomp2 = re.compile(pattern2)

recomp3a = re.compile(pattern3a)
recomp3b = re.compile(pattern3b)

'''
    RawInline fuer LaTeX und HTML vorbereiten
'''
inlineLatex = pf.RawInline(thinSpaceLaTeX, format="latex")
succLatex = pf.RawInline(xspace, format="latex")
inlineHTML = pf.RawInline(thinSpaceHTML, format="html")
succHTML = pf.RawInline("", format="html")


def latexBlock(first, second):
    return pf.RawInline("\mbox{"+first+thinSpaceLaTeX+second+"}"+xspace,
                        format="latex")


def htmlBlock(first, second):
    return pf.RawInline(first+thinspaceHTML+second, format="html")


def newBlock(first, second, format):
    if format == "html":
        return htmlBlock(first, second)
    if format == "latex":
        return latexBlock(first, second)


def latexBlockThree(first, second, third):
    return pf.RawInline("\mbox{" + first + thinSpaceLaTeX +
                        second + thinSpaceLaTeX + third + "}" +
                        xspace, format="latex")


def htmlBlockThree(first, second, third,):
    return pf.RawInline(first + thinSpaceHTML + second +
                        thinSpaceHTML + third,
                        format="html")


def newBlockThree(first, second, third, format):
    if format == "html":
        return htmlBlockThree(first, second, third)

    if format == "latex":
        return latexBlockThree(first, second, third)


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
            Pruefung mittels RegEx!
        '''
        splt = recomp1.split(elem.text)
        logging.debug("recomp1-Text: "+elem.text+" \t "+str(splt))
        if len(splt) == 4:
            logging.debug("*#*")
            if splt[3] == "":
                return newBlock(splt[1], splt[2], doc.format)
            else:
                return newBlockThree(splt[1], splt[2], splt[3], doc.format)

        '''
            Hier wird
            Text/ Text -> Text\,/
            angepasst!
        '''
        splt = recomp2.split(elem.text)
        logging.debug("recomp2-Text: "+elem.text+" \t "+str(splt))
        if len(splt) == 3 and isinstance(elem.next, pf.Space):
            logging.debug("+#+")
            return [pf.Str(splt[1]), inline, pf.Str("/")]

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
               u. a. / z. B. / Z. B. / d. h. / D. h. / u. "A. / c. p. ect.
               angepasst!
            '''
            if (isinstance(elem.next, pf.Str) and
               len(elem.prev.text) >= 2 and
               len(elem.next.text) >= 2):
                    mtcha = recomp3a.match(elem.prev.text)
                    mtchb = recomp3b.match(elem.next.text)
                    logging.debug("recomp3a-Text: " +
                                  elem.prev.text +
                                  " \t " + "recomp3b-Text: " +
                                  elem.next.text)
                    if (mtcha and mtchb):
                        logging.debug("+++")
                        return inline


def main():
    logging.debug("Start typography.py")
    pf.toJSONFilter(action=action)
    logging.debug("End typography.py")


if __name__ == "__main__":
    main()
