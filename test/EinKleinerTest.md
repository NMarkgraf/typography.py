---
title: "Ein kleiner Test"
author: "Norman Markgraf"
date: "18 Dezember 2017"
output: 
    pdf_document:
        keep_tex: true
        includes:
            in_header: 
                - header.tex
        pandoc_args:
            - --filter
            - ../typography.py
---

## Ein paar Testsenarien

Was ist z.B. mit dem Problem des zum Beispiels in einem Test? (Z.B. hier?) oder (z.B.: gerade eben?)

Wir wollen doch, dass es gut aussieht. D.h. immer schön einen kleinen Abstand zwischen den Buchstaben mit den Punkten. 

M.a.W.: Typographie ist machbar, d.h. wir machen alle mit (i.d.R.!)
