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
  0.9.3 - 09.02.2018 (nm) - HotBugFix-Release!
  0.9.4 - 10.02.2018 (nm) - Zitationen wie "S. 211" oder "S. 211 f." und "S. 211 ff."
                            werden nun durch halbe Leerzeichen getrennt.
                            (Funktioniert _nicht_ im Literaturverzeichnissen die von LaTeX
                             automatisch erzeugt werden!!!)
  0.9.4 - 11.02.2018 (nm) - Dokumentation erweitert.
  0.9.5 - 14.03.2018 (nm) - Datumsangaben werden nach Typographieregeln nicht mit einem
                            halben Leerzeichen getrennt. Sondern ganz nicht! - Jetzt korrekt
                            implementiert.
  0.9.6 - 14.03.2018 (nm) - Temperatur-, cm-, m-, mm-, km-, ccm-, und Euro-Angaben korrigieren.

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


import panflute as pf  # panflute fuer den pandoc AST
import re as re  # re fuer die Regulaeren Ausdruecke
import logging  # logging fuer die 'typography.log'-Datei


'''
 Eine Log-Datei "typography.log" erzeugen um einfacher zu debuggen
'''
#logging.basicConfig(filename='typography.log', level=logging.ERROR)
logging.basicConfig(filename='typography.log', level=logging.DEBUG)


'''
 Halbeleerzeichen für LaTeX und HTML
'''
thinSpaceLaTeX = "\\thinspace{}"  # Schmales Leerzeichen in LaTeX equiv. "\,"
thinSpaceHTML = "&thinsp;"      # Schmales Leerzeichen in HTML


'''
 Das Pakete 'xspace' wird benutzt um am Ende der Einfuegung ggf. noch ein
 Leerzeichen abzuhaengen. Das wird hiermit vorbereitet:
'''
xspace = "\\xspace{}"


'''

'''
beginBox = "\\mbox{"
endBox = "}"

'''
 Dieses Pattern sollte
 x.y. / (x.y. / (x.y.: / (x.y.) / x.y.: ...
 für alle Buchstaben x und y abdecken.
 Wichtig ... \D, damit keine Datumsangaben in die Mangel genommen werden!
 So soll z.B. 15.9.  eben nicht in Muster fallen!
'''
pattern1 = "([\(,\[,<,\{]?\w\.)(?:[~|\xa0]?)(\D\.[\),\],>]?[:,\,,\.,\!,\?]?[\),\],\},>]?)"


'''
 Dieses Pattern sollte alle / am Ende eines Strings finden.
'''
pattern2 = "([\w|\(|\[|\{]+)\/$"


'''
 Diesen Pattern soll pruefen ob der vorherige und nachfolgende Text
 zu einem halben Leerzeichen fuehrt.
'''
pattern3a = "([\(,\[,<,\{]?\w\.)"
pattern3b = "^(\w\.[\),\],>]?[:,\,,\.,\!,\?]?[\),\],\},>]?)$"


'''
 Aufspueren von Seitenangaben: "211." und "211-212."
'''
pattern4 = "\d+[-\d+]?\.?"

'''
 Aufspueren von Seitenforsetzungsmarkierungen: "211 f." und "211 ff."
'''
pattern5 = "^ff?\.?$"


'''
 Aufspueren von Temperaturangaben mit °C oder °F in der Form 21°C korrigieren
'''
pattern6 = "([-|+]?\d+,?-{0,2})(K[.,;:]?|°F[.,;:]?|°C[.,;:]?|€[.,;:]?|T€[.,;:]?|EUR[.,;:]?|Euro[.,;:]?|kg[.,;:]?|g[.,;:]?|km[.,;:]?|m[.,;:]?|Meter[.,;:]?|cm[.,;:]?|mm[.,;:]?|ccm[.,;:]?|\$[.,;:]?|US\-\$[.,;:]?)$"

'''
 Ab hier werden die Muster von oben voruebersetzt:
'''

recomp1 = re.compile(pattern1)

recomp2 = re.compile(pattern2)

recomp3a = re.compile(pattern3a)
recomp3b = re.compile(pattern3b)

recomp4 = re.compile(pattern4)
recomp5 = re.compile(pattern5)

recomp6 = re.compile(pattern6)

'''
    RawInline fuer LaTeX und HTML vorbereiten
'''
inlineLatex = pf.RawInline(thinSpaceLaTeX, format="latex")
succLatex = pf.RawInline(xspace, format="latex")
inlineHTML = pf.RawInline(thinSpaceHTML, format="html")
succHTML = pf.RawInline("", format="html")


def latexBlock(first, second):
    logging.debug("latexBlock: "+"\\mbox{"+first+thinSpaceLaTeX+second+"}"+xspace)
    return pf.RawInline("\\mbox{"+first+thinSpaceLaTeX+second+"}"+xspace,
                        format="latex")


def htmlBlock(first, second):
    logging.debug("htmlBlock: "+first+thinspaceHTML+second)
    return pf.RawInline(first+thinspaceHTML+second, format="html")


def newBlock(first, second, format):
    logging.debug("newBlock-format:"+format)
    if format == "html":
        tmp = htmlBlock(first, second)
    if format == "latex":
        tmp = latexBlock(first, second)
    if format == "beamer":
        tmp = latexBlock(first, second)
    logging.debug("newBlock: "+str(tmp))
    return tmp


def latexBlockThree(first, second, third):
    logging.debug("latexBlockThree: "+"\\mbox{" + first + thinSpaceLaTeX +
                        second + thinSpaceLaTeX + third + "}" +
                        xspace)
    return pf.RawInline("\\mbox{" + first + thinSpaceLaTeX +
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
    if format == "beamer":
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
            if splt[3] == "":
                logging.debug("Replacing "+elem.text+" to "+splt[1]+"(Halfspace)"+splt[2]+" at recomp1")
                return newBlock(splt[1], splt[2], doc.format)
            else:
                logging.debug("Replacing "+elem.text+" to "+splt[1]+"(Halfspace)"+splt[2]+"(Halfspace)"+splt[3]+" at recomp1")
                return newBlockThree(splt[1], splt[2], splt[3], doc.format)

        splt = recomp6.split(elem.text)
        logging.debug("recomp6-Text: "+elem.text+" \t "+str(splt))
        if len(splt) == 4:
            logging.debug("Replacing "+elem.text+" to "+splt[1]+"(Halfspace)"+splt[2]+" at recomp1")
            return newBlock(splt[1], splt[2], doc.format)
        '''
            Hier wird
            Text/ Text -> Text\,/
            angepasst!
        '''
        splt = recomp2.split(elem.text)
        logging.debug("recomp2-Text: "+elem.text+" \t "+str(splt))
        if len(splt) == 3 and isinstance(elem.next, pf.Space):
            logging.debug("Replacing "+elem.text+" to "+splt[1]+"(Halfspace)/ at recomp2")
            return [pf.Str(splt[1]), inline, pf.Str("/")]

        if (elem.text == "/") and isinstance(elem.prev, pf.Para):
            return [inline, pf.Str("/")]

    if isinstance(elem, pf.Space):
        if (isinstance(elem.prev, pf.Str) and
            isinstance(elem.next, pf.Str) and
            recomp4.match(elem.next.text) and
            elem.prev.text=="S."):
            return inline
        if (isinstance(elem.prev, pf.Str) and
            isinstance(elem.next, pf.Str) and
            recomp4.match(elem.prev.text) and
            recomp5.match(elem.next.text)):
            return inline
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
                        logging.debug("Replacing (Space) to (Hlfspace) at recomp3")
                        return inline


def main():
    logging.debug("Start typography.py")
    pf.toJSONFilter(action=action)
    logging.debug("End typography.py")


if __name__ == "__main__":
    main()
