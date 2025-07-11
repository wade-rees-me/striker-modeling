#include "shoe.hpp"
#include "player.hpp"

#define SOFT 1
#define HARD 0

// Constructor for Player
Player::Player(Rules *rules, Strategy *strategy, int number_of_cards, std::string playbook, std::string decks)
		: rules(rules), strategy(strategy), wager(MINIMUM_BET, MAXIMUM_BET), number_of_cards(number_of_cards) {
	model = new Model(playbook, decks);
}

// Place a bet for the player
void Player::placeBet() {
	splits.clear();
	wager.reset();
	wager.placeAmountBet(MINIMUM_BET);
}

// Play the hand
void Player::playDouble(Card *up, Shoe *shoe) {
	total = wager.getHandTotal();
	soft = wager.isSoft();
	wager.doubleBet();
	drawCard(&wager, shoe->drawCard());
}

//
void Player::writeDouble(Card *up) {
	if (total == 21) {
		model->writeDoubleStrategy(HARD, 21, up->getValue(), 0 - wager.getAmountBet());
	}
	if (soft) {
		model->writeDoubleStrategy(SOFT, total, up->getValue(), wager.getAmountWon());
		return;
	}
	model->writeDoubleStrategy(HARD, total, up->getValue(), wager.getAmountWon());
}

// Play the hand
void Player::playSplit(Card *up, Shoe *shoe) {
	if (wager.isPair()) {
		splitCard = wager.getCardPair();

		Wager *split = new Wager(MINIMUM_BET, MAXIMUM_BET);
		wager.splitHand(split);
		splits.push_back(split);

		if (wager.isPairOfAces()) {
			drawCard(&wager, shoe->drawCard());
			drawCard(split, shoe->drawCard());
			return;
		}

	  	drawCard(&wager, shoe->drawCard());
		playSplitHand(&wager, shoe, up);
		drawCard(split, shoe->drawCard());
		playSplitHand(split, shoe, up);
	}
}

//
void Player::writeSplit(Card *up) {
	int win = 0;

	win += wager.getAmountWon();
	for (const auto& split : splits) {
		win += split->getAmountWon();
	}
	model->writeSplitStrategy(splitCard->getValue(), win, up->getValue());
}

// Play the hand
void Player::playStand(Card *up, Shoe *shoe) {
	// Stand on all
}

//
void Player::writeStand(Card *up) {
	if (wager.getHandTotal() == 21) {
		model->writeStandStrategy(21, HARD, wager.getAmountWon(), up->getValue());
	}
	if (wager.isSoft()) {
		model->writeStandStrategy(wager.getHandTotal(), SOFT, wager.getAmountWon(), up->getValue());
		return;
	}
	model->writeStandStrategy(wager.getHandTotal(), HARD, wager.getAmountWon(), up->getValue());
}

// Play the hand
void Player::playHit(Card *up, Shoe *shoe) {
	total = wager.getHandTotal();
	soft = wager.isSoft();

	bool doStand = false;
	while (!wager.isBusted() && !doStand) {
		drawCard(&wager, shoe->drawCard());
		if (!wager.isBusted()) {
			doStand = strategy->getStand(seen_cards, wager.getHandTotal(), wager.isSoft(), up);
		}
	}
}

//
void Player::writeHit(Card *up) {
	if (soft) {
		model->writeHitStrategy(total, SOFT, wager.getAmountWon(), up->getValue());
		return;
	}
	if (total == 20) {
		model->writeHitStrategy(21, HARD, 0 - wager.getAmountBet(), up->getValue());
	}
	model->writeHitStrategy(total, HARD, wager.getAmountWon(), up->getValue());
}

//
void Player::playSplitHand(Wager *wager, Shoe *shoe, Card *up) {
	if (wager->isPair()) {
		Wager *split = new Wager(MINIMUM_BET, MAXIMUM_BET);
		splits.push_back(split);
		wager->splitHand(split);

  		drawCard(wager, shoe->drawCard());
		playSplitHand(wager, shoe, up);
		drawCard(split, shoe->drawCard());
		playSplitHand(split, shoe, up);
		return;
	}

	bool doStand = strategy->getStand(seen_cards, wager->getHandTotal(), wager->isSoft(), up);
	while (!wager->isBusted() && !doStand) {
		drawCard(wager, shoe->drawCard());
		if (!wager->isBusted()) {
			doStand = strategy->getStand(seen_cards, wager->getHandTotal(), wager->isSoft(), up);
		}
	}
}

// Draw a card
void Player::drawCard(Hand *hand, Card *card) {
	hand->drawCard(card);
}

// Check if player busted or has blackjack
bool Player::bustedOrBlackjack() const {
	if (splits.size() == 0) {
		return wager.isBusted() || wager.isBlackjack();
	}

	for (const auto& split : splits) {
		if (!split->isBusted()) {
			return false;
		}
	}
	return true;
}

//
void Player::payoff(bool dealer_blackjack, bool dealer_busted, int dealer_total) {
	if (splits.size() == 0) {
		payoffHand(&wager, dealer_blackjack, dealer_busted, dealer_total);
		return;
	}

	payoffSplit(&wager, dealer_busted, dealer_total);
	for (const auto& split : splits) {
		payoffSplit(split, dealer_busted, dealer_total);
	}
}

//
void Player::payoffHand(Wager *wager, bool dealer_blackjack, bool dealer_busted, int dealer_total) {
	if (dealer_blackjack) {
		wager->wonInsurance();
		if (wager->isBlackjack()) {
			wager->push();
		} else {
			wager->lost();
		}
	} else {
		wager->lostInsurance();
		if (wager->isBlackjack()) {
			wager->wonBlackjack(rules->blackjack_pays, rules->blackjack_bets);
		} else if (wager->isBusted()) {
			wager->lost();
		} else if (dealer_busted || (wager->getHandTotal() > dealer_total)) {
			wager->won();
		} else if (dealer_total > wager->getHandTotal()) {
			wager->lost();
		} else {
			wager->push();
		}
	}

	report.total_bet += wager->getAmountBet() + wager->getInsuranceBet();
	report.total_won += wager->getAmountWon() + wager->getInsuranceWon();
}

//
void Player::payoffSplit(Wager *wager, bool dealer_busted, int dealer_total) {
	if (wager->isBusted()) {
		wager->lost();
	} else if (dealer_busted || (wager->getHandTotal() > dealer_total)) {
		wager->won();
	} else if (dealer_total > wager->getHandTotal()) {
		wager->lost();
	} else {
		wager->push();
	}

	report.total_won += wager->getAmountWon();
	report.total_bet += wager->getAmountBet();
}

//
bool Player::mimicStand() {
	if (wager.isSoft17()) {
		return false;
	}
	return wager.getHandTotal() >= 17;
}

void Player::write() {
	model->write();
}

