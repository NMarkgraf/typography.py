[![StyleCI](https://styleci.io/repos/112326321/shield?branch=master)](https://styleci.io/repos/112326321)
[![BCH compliance](https://bettercodehub.com/edge/badge/NMarkgraf/typography.py?branch=master)](https://bettercodehub.com/)

# typography.py

Dies ist ein [pandoc](https://pandoc.org) Filter, geschrieben in [Python3](https://www.python.org) und basierend auf [panflute](https://github.com/sergiocorreia/panflute).

Er sucht nach Ausdrücken wie "z.B.", "u.a." oder "i.d.R." und ersetzt diese in der *LaTeX*- oder *HTML*-Ausgabe durch die typographisch schöneren Ausdrücke "z.\\,B.", "u.\&thinsp;a." bzw. "i.\\,d.\\,R.\xspace".

Als Zielsprachen werden zur Zeit *LaTeX* (inkl. Beamer) und *HTML* unterstützt. 

Für LaTeX muss das Paket **xspace** (durch ein passendes `\usepackage{xspace}`) geladen sein.

## Better Code Hub

Ich versuche diese Code bei 7+/10 zu halten. Mehr geht z.Z. auch kaum.
