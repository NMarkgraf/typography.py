[![CircleCI](https://circleci.com/gh/NMarkgraf/typography.py.svg?style=svg)](https://circleci.com/gh/NMarkgraf/typography.py)
[![StyleCI](https://styleci.io/repos/112326321/shield?branch=master)](https://styleci.io/repos/112326321)
[![BCH compliance](https://bettercodehub.com/edge/badge/NMarkgraf/typography.py?branch=master)](https://bettercodehub.com/)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![Minimal Python needed: 3.5+](https://img.shields.io/badge/Python-3.5%2B-brightgreen.svg)](https://www.python.org)
[![CodeFactor](https://www.codefactor.io/repository/github/nmarkgraf/typography.py/badge)](https://www.codefactor.io/repository/github/nmarkgraf/typography.py)

# typography.py

Dies ist ein [pandoc](https://pandoc.org) Filter, geschrieben in [Python3](https://www.python.org) und basierend auf [panflute](https://github.com/sergiocorreia/panflute).

Er sucht nach Ausdrücken wie "z.B.", "u.a." oder "i.d.R." und ersetzt diese in der *LaTeX*- oder *HTML*-Ausgabe durch die typographisch schöneren Ausdrücke "z.\\thinspace{}B.\xspace{}", "u.\&thinsp;a." bzw. "i.\\thinspace{}d.\\thinspace{}R.\xspace{}".

Als Zielsprachen werden zur Zeit *LaTeX* (inkl. Beamer) und *HTML* unterstützt. 

Für LaTeX muss das Paket **xspace** (durch ein passendes `\usepackage{xspace}`) geladen sein.

## Better Code Hub

Ich versuche diesen Code bei 7+/10 zu halten. Mehr als geht zur Zeit auch kaum.
