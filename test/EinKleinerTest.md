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

D. h. aber auch, dass wir alle anderen Abkürzungen finden sollten.

D.h. -- Das heißt

d.h. -- das heißt

s.o. -- siehe oben

s.u. -- siehe unten

Was passiert hier: s. o.,  s. u.,  d. h.,  z. B.?
Im Vergleich zu hier: s.o., s.u., d.h., z.B.?

## Ein paar weitere Tests

Läuft das auch so: (Wie sieht es z.B. hier aus?)

Was kommt hier raus? (*z.B.*) (*z. B.*), (**z.B.**) (**z. B.**), (***z.B.***) (***z. B.***)


## Übung `r nextExercise()`: Skalenniveau (I/II)


## Übung `r nextExercise()`: Skalenniveau (I/ II)

## Übung `r nextExercise()`: Skalenniveau (*I/II*)
