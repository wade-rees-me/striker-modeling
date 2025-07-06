#!/usr/bin/env python3

# Import project modules
import sys
import model
import chart
import chart_neural
import diagram
import constant
from arguments import Arguments

# Entry point
if __name__ == "__main__":
    # Parse command-line arguments
    args = Arguments(sys.argv)

    print("Starting...")

    # Build models if --model flag is set
    if args.model_flag:
        model.build_models(constant.BASIC, constant.SINGLE_DECK)
        model.build_models(constant.BASIC, constant.DOUBLE_DECK)
        model.build_models(constant.BASIC, constant.SIX_SHOE)

    # Build charts if --chart flag is set
    if args.chart_flag:
        # Linear strategy charts
        chart.build_charts(constant.LINEAR, constant.SINGLE_DECK)
        chart.build_charts(constant.LINEAR, constant.DOUBLE_DECK)
        chart.build_charts(constant.LINEAR, constant.SIX_SHOE)

        # Polynomial strategy charts
        chart.build_charts(constant.POLYNOMIAL, constant.SINGLE_DECK)
        chart.build_charts(constant.POLYNOMIAL, constant.DOUBLE_DECK)
        chart.build_charts(constant.POLYNOMIAL, constant.SIX_SHOE)

        # Neural net-based charts
        chart_neural.build_charts_neural(constant.NEURAL, constant.SINGLE_DECK)
        chart_neural.build_charts_neural(constant.NEURAL, constant.DOUBLE_DECK)
        chart_neural.build_charts_neural(constant.NEURAL, constant.SIX_SHOE)

    # Build diagrams if --diagrams flag is set
    if args.diagram_flag:
        diagram.build_diagrams(constant.SINGLE_DECK, "Single Deck: ")
        diagram.build_diagrams(constant.DOUBLE_DECK, "Double Deck: ")
        diagram.build_diagrams(constant.SIX_SHOE, "Six Shoe: ")

    print("Ending...\n")
