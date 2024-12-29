#!/usr/local/bin/python3

import sys

import model
import chart
import diagram
from arguments import Arguments

BASIC = 'basic'
LINEAR = 'linear'
POLYNOMIAL = 'polynomial'
NEURAL = 'neural'

SINGLE_DECK = 'single-deck'
DOUBLE_DECK = 'double-deck'
SIX_SHOE = 'six-shoe'

#
#
#
if __name__ == "__main__":
    args = Arguments(sys.argv)

    print("Starting...")

    if args.model_flag:
        model.build_models(BASIC, SINGLE_DECK)
        #model.build_models(BASIC, DOUBLE_DECK)
        #model.build_models(BASIC, SIX_SHOE)

    if args.chart_flag:
        chart.build_charts(LINEAR, SINGLE_DECK)
        #chart.build_charts(LINEAR, DOUBLE_DECK)
        #chart.build_charts(LINEAR, SIX_SHOE)

        chart.build_charts(POLYNOMIAL, SINGLE_DECK)
        #chart.build_charts(POLYNOMIAL, DOUBLE_DECK)
        #chart.build_charts(POLYNOMIAL, SIX_SHOE)

        chart.build_charts_neural(NEURAL, SINGLE_DECK)
        #chart.build_charts_neural(NEURAL, DOUBLE_DECK)
        #chart.build_charts_neural(NEURAL, SIX_SHOE)

    if args.diagram_flag:
        diagram.build_diagrams(SINGLE_DECK, "Single Deck: ")
        #diagram.build_diagrams(DOUBLE_DECK, "Double Deck: ")
        #diagram.build_diagrams(SIX_SHOE, "Six Shoe: ")

    print("Ending...\n")

