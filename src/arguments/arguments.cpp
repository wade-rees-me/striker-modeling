#include <iostream>
#include <cstdlib>
#include <cstring>
#include <string>
#include "arguments.hpp"
#include "constants.hpp"

//
Arguments::Arguments(int argc, char *argv[]) {
	for (int i = 1; i < argc; ++i) {
		if ((std::strcmp(argv[i], "-h") == 0 || std::strcmp(argv[i], "--number-of-hands") == 0) && i + 1 < argc) {
			number_of_hands = std::atoll(argv[++i]);
			if (number_of_hands < MINIMUM_NUMBER_OF_HANDS || number_of_hands > MAXIMUM_NUMBER_OF_HANDS) {
				std::cerr << "Number of hands must be between " << MINIMUM_NUMBER_OF_HANDS << " and " << MAXIMUM_NUMBER_OF_HANDS << std::endl;
				std::exit(EXIT_FAILURE);
			}
		} else if (std::strcmp(argv[i], "-1") == 0 || std::strcmp(argv[i], "--single-deck") == 0) {
			single_deck_flag = true;
		} else if (std::strcmp(argv[i], "-2") == 0 || std::strcmp(argv[i], "--double-deck") == 0) {
			double_deck_flag = true;
		} else if (std::strcmp(argv[i], "-6") == 0 || std::strcmp(argv[i], "--six-shoe") == 0) {
			six_shoe_flag = true;
		} else if (std::strcmp(argv[i], "--help") == 0) {
			printHelpMessage();
			std::exit(EXIT_SUCCESS);
		} else if (std::strcmp(argv[i], "--version") == 0) {
			printVersion();
			std::exit(EXIT_SUCCESS);
		} else {
			std::cerr << "Error: Invalid argument: " << argv[i] << std::endl;
			std::exit(2);
		}
	}
}

//
void Arguments::printVersion() const {
	std::cout << STRIKER_WHO_AM_I << ": version: " << STRIKER_VERSION << std::endl;
}

//
void Arguments::printHelpMessage() const {
	std::cout << "Usage: strikerC++ [options]\n"
			  << "Options:\n"
			  << "  --help                                   Show this help message\n"
			  << "  --version                                Display the program version\n"
			  << "  -h, --number-of-hands <number of hands>  The number of hands to play in this simulation\n"
			  << "  -1, --single-deck                        Use a single deck of cards and rules\n"
			  << "  -2, --double-deck                        Use a double deck of cards and rules\n"
			  << "  -6, --six-shoe                           Use a six deck shoe of cards and rules\n"
			  << std::endl;
}

// Function to get the current strategy as a string
std::string Arguments::getStrategy() const {
	return "basic";
}

//
std::string Arguments::getDecks() const {
	if (double_deck_flag) {
		return "double-deck";
	}
	if (six_shoe_flag) {
		return "six-shoe";
	}
	return "single-deck";
}

//
int Arguments::getNumberOfDecks() const {
	if (double_deck_flag) {
		return 2;
	}
	if (six_shoe_flag) {
		return 6;
	}
	return 1;
}

