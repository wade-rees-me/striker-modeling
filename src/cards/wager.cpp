#include <algorithm>
#include <iostream>
#include "wager.hpp"

// Constructor: Reset the wager to its initial state
Wager::Wager(int64_t minimum_bet, int64_t maximum_bet)
		: minimum_bet(minimum_bet), maximum_bet(maximum_bet) {
	reset();
}

void Wager::reset() {
	Hand::reset();
	amount_bet = 0;
	amount_won = 0;
	insurance_bet = 0;
	insurance_won = 0;
}

// Split the hand
void Wager::splitHand(Wager *split) {
	split->amount_bet = amount_bet;
	split->drawCard(splitPair());
}

void Wager::displayHand() {
	for (const auto& card : cards) {
		std::cout << card->getRank() << ", ";
	}
	std::cout << getHandTotal() << ", " << isSoft() << ": ";
	std::cout << amount_bet << ": " << amount_won << std::endl;
}

