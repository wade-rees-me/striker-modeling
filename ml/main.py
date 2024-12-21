#!/usr/local/bin/python3

import model
import chart
import diagram

BASIC = 'basic'
LINEAR = 'linear'
POLYNOMIAL = 'polynomial'

SINGLE_DECK = 'single-deck'
DOUBLE_DECK = 'double-deck'
SIX_SHOE = 'six-shoe'

#
#
#
if __name__ == "__main__":
    print("Starting...")

    model.build_models(BASIC, SINGLE_DECK)
    model.build_models(BASIC, DOUBLE_DECK)
    model.build_models(BASIC, SIX_SHOE)

    chart.build_charts(LINEAR, SINGLE_DECK)
    chart.build_charts(LINEAR, DOUBLE_DECK)
    chart.build_charts(LINEAR, SIX_SHOE)

    chart.build_charts(POLYNOMIAL, SINGLE_DECK)
    chart.build_charts(POLYNOMIAL, DOUBLE_DECK)
    chart.build_charts(POLYNOMIAL, SIX_SHOE)

    diagram.build_diagrams(SINGLE_DECK)
    diagram.build_diagrams(DOUBLE_DECK)
    diagram.build_diagrams(SIX_SHOE)

    print("Ending...\n")

