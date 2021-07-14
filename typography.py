#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-FileCopyrightText: 2017-2021 by Norman Markgraf <nmarkgraf@hotmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
release = "2.5.5"
"""
  Quick-Pandoc-Typographie-Filter: typography.py

  (C)opyleft in 2017-21 by Norman Markgraf (nmarkgraf@hotmail.com)

  Release:
  ========
  1.0.0 - 01.04.2018 (nm) - Neue Fassung aller Module
  1.0.1 - 04.04.2018 (nm) - Kleine Codeverbesserungen
  1.1   - 14.06.2018 (nm) - Kleinere Fehler ausgebessert.
  1.2   - 27.12.2018 (nm) - Noch ein paar kleinere Fehler ausgebessert.
  2.0   - 27.12.2018 (nm) - Anpassung an autofilter!
  2.1   - 03.01.2019 (nm) - Bugfixe
  2.2   - 28.04.2019 (nm) - narrowSlash eingeführt. LaTeX braucht das Paket "trimclip"!
  2.3   - 02.05.2019 (nm) - LaTeX Paket "XSPACE" nun via finalize eingebunden!
  2.3.1 - 07.07.2019 (nm) - Hoffentlich eine Lösung für den Bug von Tobias.
  2.4.0 - 08.07.2019 (nm) - Code Refaktor (Anpassungen an PEP8)
  2.5.0 - 01.03.2021 (nm) - Add html5 support
  2.5.1 - 01.03.2021 (nm) - Wenn schon, denn schon: html4, slidy, revealjs ...
  2.5.2 - 11.07.2021 (nm) - RegEx-Ausdrücke optimiert, SPDX-Eintrag spendiert
  2.5.3 - 12.07.2021 (nm) - McCabe Value hacking ;-)
  2.5.4 - 13.07.2021 (nm) - Minimale Performance-Tweaks
  2.5.5 - 14.07.2021 (nm) - McCabe Value hacking und Zeitnahme in log-Datei
  
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
  Der Befehl "XSPACE" benötigst das Paket "XSPACE".
  Also bitte "usepackage{XSPACE}" einbauen!
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

"""

import logging  # logging fuer die 'typography.log'-Datei
import os as os  # check if file exists.
import re as re  # re fuer die Regulaeren Ausdruecke
import time  # Performace timer 

import panflute as pf  # panflute fuer den pandoc AST

# Eine Log-Datei "typography.log" erzeugen um einfacher zu debuggen
debuglevels = {
  "debug": logging.DEBUG, 
  "info": logging.INFO, 
  "warning": logging.WARNING, 
  "error": logging.ERROR
}
for dl_key, dl_value in debuglevels.items():
  if os.path.exists("typography.loglevel."+dl_key):
    DEBUGLEVEL = dl_value
    break
else:
    DEBUGLEVEL = logging.ERROR  # .ERROR or .DEBUG  or .INFO

logging.basicConfig(filename='typography.log', level=DEBUGLEVEL)



"""
 Tuppel aller HTML Varianten in pandoc
"""

HTML_LIKE = ("html", "html4", "html5", "slideous", 
             "slidy", "dzslides", "revealjs", "s5")

"""
 Tuppel aller LaTeX Varianten in pandoc
"""
LATEX_LIKE= ("latex", "beamer", "tex")


"""
 Halbeleerzeichen für LaTeX und HTML
"""
THIN_SPACE_LATEX = r"\thinspace{}"  # Schmales Leerzeichen in LaTeX equiv. "\,"
THIN_SPACE_HTML = "&thinsp;"  # Schmales Leerzeichen in HTML

"""
 Das verbesserte LaTeX Zeichen Slash /
"""
NARROW_SLASH_LATEX = r"\clipbox{0pt 3pt 0pt 0pt}{/}"
NARROW_SLASH_HTML = "/"

"""
 Das Pakete 'XSPACE' wird benutzt um am Ende der Einfuegung ggf. noch ein
 Leerzeichen abzuhaengen. Das wird hiermit vorbereitet:
"""
XSPACE = r"\xspace{}"

"""
 LaTeX-mbox Begin und Ende
"""
BEGIN_BOX = r"\mbox{"
END_BOX = "}"

"""
    RawInline fuer LaTeX und HTML vorbereiten
"""
INLINE_LATEX = pf.RawInline(THIN_SPACE_LATEX, format="latex")
SUCC_LATEX = pf.RawInline(XSPACE, format="latex")
INLINE_HTML = pf.RawInline(THIN_SPACE_HTML, format="html")
SUCC_HTML = pf.RawInline("", format="html")

"""
 Suchmuster (pattern) für die einzelnen Situationen

 pattern1
 ========

 Dieses Pattern sucht nach x.y. in den Fassungen:
    x.y. / (x.y. / (x.y.: / (x.y.) / x.y.: ...
 für alle Buchstaben x und y abdecken.
 Wichtig ... \\D, damit keine Datumsangaben in die Mangel genommen werden!
 So soll z.B. 15.9.  eben _nicht_ in Muster fallen!
"""
# old: pattern1 = "([\(,\[,<,\{]?\w\.)(?:[~|\xa0]?)(\D\.[\),\],>]?[:,\,,\.,\!,\?]?[\),\],\},>]?)"
pattern1 = r"([(\[<{]?\w\.)(?:[~\xa0]?)(\D\.[)\]>]?[:,\.!\?]?[\)\]}>]?)"

"""
 pattern2
 ========
 Dieses Pattern findet alle "/" am Ende einer Zeichenkette.

 Also "Test/" oder "Super/", aber nicht "/" oder "Test/Test"!
"""
pattern2 = "([\w(\[{]+)\/$"

"""
 pattern3a/b
 ===========

 Diesen Pattern pruefen ob der vorherige und nachfolgende Text
 zu einem halben Leerzeichen fuehrt.
 Also "z. B." oder "u. a.". Die Leerzeichen werden im pandoc AST
 zu [String,c="z."][Space][String,c="B."]. Wir testen also beim [Space]
 das vorherige und nachfolgende String Element.
"""
pattern3a = "([\(\[<{]?\w\.)"
pattern3b = "^(\w\.[)\]>]?[:,\.!\?]?[)\]}>]?)$"

"""
 pattern4
 ========
 Aufspueren von Seitenangaben: "211." und "211-212."
"""
pattern4 = "\d+[-\d+]?\.?"

"""
 pattern5
 ========
 Aufspueren von Seitenforsetzungsmarkierungen: "211 f." und "211 ff."
"""
pattern5 = "^ff?\.?$"

"""
 pattern6
 ========
 Aufspueren von Temperaturangaben mit °C oder °F in der Form 21°C korrigieren,
 ebenso cm, mm, ccm, kg, EUR, km, Meter, m und %
"""
pattern6 = "([-+]?\d+?-{0,2})(K[.,;:]?|°F[.,;:]?|°C[.,;:]?|€[.,;:]?|T€[.,;:]?|EUR?[.,;:]?|Euro[.,;:]?|kg[.,;:]?|g[.,;:]?|km[.,;:]?|m[.,;:]?|Meter[.,;:]?|cm[.,;:]?|mm[.,;:]?|ccm[.,;:]?|\$[.,;:]?|US\-\$[.,;:]?|%[.,;:]?)$"

"""Vorkompilieren der Muster.
"""
recomp1 = re.compile(pattern1)
recomp2 = re.compile(pattern2)
recomp3a = re.compile(pattern3a)
recomp3b = re.compile(pattern3b)
recomp4 = re.compile(pattern4)
recomp5 = re.compile(pattern5)
recomp6 = re.compile(pattern6)

"""

"""


def make_latex_inline(a):
    """
        Erzeugt aus einer Liste von 2 oder 3 Einträgen den
        passenden LaTeX-RawInline Code:
            "\\mbox{x_y}\\XSPACE{}" bzw. "\\mbox{x_y_z}\\XSPACE{}"
        Wobei _ jeweils ein THIN_SPACE_LATEX ist und x,y,z die 2 bzw. 3
        Einträge in der Liste
    """
    tmp = BEGIN_BOX + \
          THIN_SPACE_LATEX.join(make_latex_escapes(x) for x in a) + \
          END_BOX + XSPACE
    logging.debug("make_latex_inline: " + tmp)
    return pf.RawInline(tmp, format="latex")


def make_html_inline(a):
    """
        Erzeugt aus einer Liste von 2 oder 3 Einträgen den
        passenden HTML-RawInline Code:
            "x_y" bzw. "x_y_z"
        Wobei _ jeweils ein THIN_SPACE_HTML ist und x,y,z die 2 bzw. 3
        Einträge in der Liste
    """
    tmp = THIN_SPACE_HTML.join(a)
    logging.debug("make_html_inline: " + tmp)
    return pf.RawInline(tmp, format="html")


def make_inline(a, frmt):
    """Wähle die passende make(LaTeX/HTML)Inline gemäß dem Format aus.

    :param a:
    :param frmt: format
    """
    if frmt in LATEX_LIKE:
        return make_latex_inline(a)
    if frmt in HTML_LIKE:
        return make_html_inline(a)


def make_latex_escapes(strg):
    if strg[0] in ("$", "%"):
        strg = "\\" + strg
    if strg[0:4] == "US-$":
        strg = "US-\\" + strg[3:]
    return strg


def get_narrow_slash_latex():
    return pf.RawInline(NARROW_SLASH_LATEX, format="latex")


def get_narrow_slash_html():
    return pf.Str(NARROW_SLASH_HTML)


def get_narrow_slash(frmt):
    if frmt in LATEX_LIKE:
        return get_narrow_slash_latex()
    if frmt in HTML_LIKE:
        return get_narrow_slash


def get_inline(doc):
    if doc.format in HTML_LIKE:
        return INLINE_HTML
    if doc.format in LATEX_LIKE:
        return INLINE_LATEX


def is_this_a_string(e):
    return isinstance(e, pf.Str)


def is_next_a_string(e):
    return is_this_a_string(e.next)


def is_prev_a_string(e):
    return is_this_a_string(e.prev)


def are_prev_and_next_strings(e):
    return is_next_a_string(e) and is_prev_a_string(e)


def is_this_a_space(e):
    return isinstance(e, pf.Space)


def is_next_a_space(e):
    return is_this_a_space(e.next)


def is_next_a_paragaph(e):
    return isinstance(e.next, pf.Para)


def ends_string_with_a_slash(strg):
    return strg[-1] == "/"


def is_string_just_a_slash(strg):
    return strg == "/"


def is_string_and_slash(elem):
    if isinstance(elem, pf.Str):
        if isinstance(elem.next, pf.Str):
            return elem.next.text[0] == "/"
    return False


def is_prev_and_next_and_this_string_a_space(e):
    return is_this_a_space(e) and are_prev_and_next_strings(e)


def handle_string_pattern1(elem, doc):
    splt = recomp1.split(elem.text)
    logging.debug(f"handle_string_pattern1: {elem.text} \t split{str(splt)}")
    if len(splt) == 4:
        if splt[3] == "":
            logging.debug(f"Replacing {elem.text} to {splt[1]}(Halfspace){splt[2]} at recomp1")
            return make_inline(splt[1:3], doc.format)
        else:
            logging.debug(f"Replacing {elem.text} to {splt[1]}(Halfspace){splt[2]}(Halfspace){splt[3]} at recomp1")
            return make_inline(splt[1:4], doc.format)


def handle_string_pattern6(elem, doc):
    splt = recomp6.split(elem.text)
    logging.debug(f"handle_string_pattern6: {elem.text} \t {str(splt)}")
    if len(splt) == 4:
        if splt[0] is not None:
            splt[1] = splt[0] + splt[1]
        logging.debug(f"Replacing {elem.text} to {splt[1]}(Halfspace){splt[2]} at recomp6")
        return make_inline(splt[1:3], doc.format)


def handle_string_pattern2(elem, doc):
    splt = recomp2.split(elem.text)
    logging.debug(f"handle_string_pattern2: {elem.text} \t {str(splt)}")
    if len(splt) == 3 and isinstance(elem.next, pf.Space):
        logging.debug(f"Replacing {elem.text} to {splt[1]}(Halfspace)/ at recomp2")
        return [pf.Str(splt[1]), get_inline(doc), get_narrow_slash(doc.format)]


def handle_space_between_strings(elem, doc):
    logging.debug(f"handle_space_between_strings: {elem.prev.text} {elem.next.text}")
    if recomp4.match(elem.next.text):
        if elem.prev.text == "S.":
            return get_inline(doc)
    if recomp4.match(elem.prev.text):
        if recomp5.match(elem.next.text):
            return get_inline(doc)


def handle_space_prev_string(elem, doc):
    logging.debug("handle_space_prev_string:")
    if is_prev_a_string(elem):
        if elem.prev.text[-1] == "/":
            return get_inline(doc)


def is_between_long_strings(elem):
    return (len(elem.prev.text) >= 2 and
            len(elem.next.text) >= 2)


def handle_between_long_string(elem, doc):
    logging.debug(f"handle_between_long_string: {elem.prev.text} {elem.next.text}")
    mtcha = recomp3a.match(elem.prev.text)
    mtchb = recomp3b.match(elem.next.text)
    logging.debug(f"recomp3a-Text: {elem.prev.text} \t recomp3b-Text: {elem.next.text}")
    if mtcha and mtchb:
        logging.debug("Replacing (Space) to (Hlfspace) at recomp3")
        return get_inline(doc)


def handle_space(elem, doc):
    
    def __is_next_string_and_slash(elem):
        return is_string_and_slash(elem.next)
    
    def __be_true(*args):
        return True
    
    def __joined(elem):
        return are_prev_and_next_strings(elem) and is_between_long_strings(elem)
      
    logging.debug("handle_space:")
    
    fkts = (  # (condition, function)
      (are_prev_and_next_strings, handle_space_between_strings), 
      (__is_next_string_and_slash, get_inline),
      (__be_true, handle_space_prev_string),
      (__joined, handle_between_long_string)
  )

    for c, f in fkts:
        logging.debug(f"{c.__name__} - {f.__name__}")
        if c(elem):
            ret = f(elem, doc)
            if ret:
              return ret
    return None


def handle_slash_after_paragraph(elem, doc):
    if elem.text == "/" and isinstance(elem.prev, pf.Para):
        return [get_inline(doc), get_narrow_slash(doc.format)]


def handle_string(elem, doc):
    logging.debug(f"handle_string:{elem.text}")
    if elem.text == ".":
        logging.debug("handle_string - fast pass!")
        return None

    fkts = (handle_string_pattern1, 
            handle_string_pattern6,
            handle_string_pattern2,
            handle_slash_after_paragraph)

    for f in fkts:
      logging.debug(f.__name__)
      ret = f(elem, doc)
      if ret:
        return ret
    return None
  

def action(elem, doc):
    """
    """
    logging.debug(f"Next Element: {pf.stringify(elem, newlines=False)} <{str(type(elem.parent))}>")
    if not isinstance(elem.parent, pf.MetaValue):
        if is_this_a_space(elem):
            return handle_space(elem, doc)
        elif is_this_a_string(elem):
            ret = handle_string(elem, doc)
            if ret:
                logging.debug("Got a ret:")
                return ret


def _prepare(doc):
    pass



  
  
def _finalize(doc):
    hdr_inc = "header-includes"

    def __add_header_includes(doc):
      # Add header-includes if necessary
      if "header-includes" not in doc.metadata:
          if doc.get_metadata("output.beamer_presentation.includes") is None:
              logging.info("No 'header-includes' nor `includes` ? Created 'header-includes'!")
              doc.metadata[hdr_inc] = pf.MetaList()
          else:
              logging.ERROR("Found 'includes'! SAD THING!")
              exit(1)
      return doc
  
    def __append_header_includes(rawstr, frmt):
        logging.debug(f"Append line '{rawstr}' to `header-includes`")
        if not rawstr in doc.get_metadata("header-includes"):
            doc.metadata[hdr_inc].append(
                pf.MetaInlines(pf.RawInline(rawstr, frmt))
            )
  
    logging.debug("Finalize doc!")

    doc = __add_header_includes(doc)
    # Convert header-includes to MetaList if necessary

    logging.debug("Append background packages to `header-includes`")

    if not isinstance(doc.metadata[hdr_inc], pf.MetaList):
        logging.info(f"The '{hdr_inc}' is not a list? Converted!")
        doc.metadata[hdr_inc] = pf.MetaList(doc.metadata[hdr_inc])

    if doc.format in LATEX_LIKE:
        __append_header_includes(r"\usepackage{xspace}  % added by typography.py!", "latex")
        __append_header_includes(r"\usepackage{trimclip}  % added by typography.py!", "latex")


def main(doc=None):
    """main function.
    """
    logging.info(78*"=")
    logging.info(f"THIS IS typography.py release {release}. A pandoc filter using panflute.")
    logging.info("(C) in 2017-2021 by Norman Markgraf")
    logging.info(78*"-")
    logging.debug("Start pandoc filter 'typography.py'")
    t = time.perf_counter()
    ret = pf.run_filter(action,
                        prepare=_prepare,
                        finalize=_finalize,
                        doc=doc)
    elapsed_time = time.perf_counter() - t
    logging.debug("End pandoc filter 'typography.py'")
    logging.info(f"Running time: {elapsed_time} seconds.")
    logging.info(78*"=")
    return ret


if __name__ == "__main__":
    main()
