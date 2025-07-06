#!/usr/bin/env python3

import os

os.environ["XLA_FLAGS"] = "--xla_gpu_cuda_data_dir=/usr/lib/nvidia-cuda-toolkit/nvvm"

import sys

import model
import chart
import chart_neural
import diagram
import constant
from arguments import Arguments

#
#
#
if __name__ == "__main__":
    args = Arguments(sys.argv)

    print("Starting...")

    if args.model_flag:
        model.build_models(constant.BASIC, constant.SINGLE_DECK)
        model.build_models(constant.BASIC, constant.DOUBLE_DECK)
        model.build_models(constant.BASIC, constant.SIX_SHOE)

    if args.chart_flag:
        chart.build_charts(constant.LINEAR, constant.SINGLE_DECK)
        chart.build_charts(constant.LINEAR, constant.DOUBLE_DECK)
        chart.build_charts(constant.LINEAR, constant.SIX_SHOE)

        chart.build_charts(constant.POLYNOMIAL, constant.SINGLE_DECK)
        chart.build_charts(constant.POLYNOMIAL, constant.DOUBLE_DECK)
        chart.build_charts(constant.POLYNOMIAL, constant.SIX_SHOE)

        chart_neural.build_charts_neural(constant.NEURAL, constant.SINGLE_DECK)
        chart_neural.build_charts_neural(constant.NEURAL, constant.DOUBLE_DECK)
        chart_neural.build_charts_neural(constant.NEURAL, constant.SIX_SHOE)

    if args.diagram_flag:
        diagram.build_diagrams(constant.SINGLE_DECK, "Single Deck: ")
        diagram.build_diagrams(constant.DOUBLE_DECK, "Double Deck: ")
        diagram.build_diagrams(constant.SIX_SHOE, "Six Shoe: ")

    print("Ending...\n")
