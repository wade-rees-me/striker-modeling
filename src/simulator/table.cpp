#include <iostream>
#include <cstdio>
#include <iomanip>
#include <ctime>
#include <string>
#include "table.hpp"
#include "shoe.hpp"

//
Table::Table(Parameters *parameters, Rules *rules, Strategy *strategy)
		: parameters(parameters) {
	shoe = new Shoe(parameters->number_of_decks, rules->penetration);
	dealer = new Dealer(rules->hit_soft_17);
	player = new Player(rules, strategy, shoe->getNumberOfCards(), parameters->strategy, parameters->decks);
	report = Report();
}

//
Table::~Table() {
	delete shoe;
	delete dealer;
	delete player;
}

//
void Table::runDouble() {
    char buffer[256];
	std::snprintf(buffer, sizeof(buffer), "      Start: table, playing %lld hands", parameters->number_of_hands);
	std::cout << buffer << std::endl;

	report.start = std::time(nullptr);
	report.total_hands = 0;
	report.total_rounds = 0;
	while (report.total_hands < parameters->number_of_hands) {
		status(report.total_rounds, report.total_hands);
		shoe->shuffle();
		//player->shuffle();
		report.total_rounds++;

		while (!shoe->shouldShuffle()) {
			report.total_hands++;
			dealer->reset();
			player->placeBet();

			dealCards(player->getWager());
			if (dealer->isBlackjack()) {
				continue;
			}

			player->playDouble(up, shoe);
			if (!player->bustedOrBlackjack()) {
				while (!dealer->shouldStand()) {
					Card *card = shoe->drawCard();
					dealer->drawCard(card);
					//player->showCard(card);
				}
			}

			//player->showCard(down);
			player->payoff(dealer->isBlackjack(), dealer->isBusted(), dealer->getHandTotal());
			player->writeDouble(up);
		}
	}
	std::cout << "\n";

	report.end = std::time(nullptr);
	report.duration = report.end - report.start;
	std::snprintf(buffer, sizeof(buffer), "      End: table\n");
	std::cout << buffer;
}

//
void Table::runSplit() {
    char buffer[256];
	std::snprintf(buffer, sizeof(buffer), "      Start: table, playing %lld hands", parameters->number_of_hands);
	std::cout << buffer << std::endl;

	report.start = std::time(nullptr);
	report.total_hands = 0;
	report.total_rounds = 0;
	while (report.total_hands < parameters->number_of_hands) {
		status(report.total_rounds, report.total_hands);
		shoe->shuffle();
		player->shuffle();
		report.total_rounds++;

		while (!shoe->shouldShuffle()) {
			dealer->reset();
			player->placeBet();

			dealCards(player->getWager());
			if (player->getWager()->isPair()) {
				report.total_hands++;
				if (!dealer->isBlackjack()) {
					player->playSplit(up, shoe);
					if (!player->bustedOrBlackjack()) {
						while (!dealer->shouldStand()) {
							Card *card = shoe->drawCard();
							dealer->drawCard(card);
							player->showCard(card);
						}
					}
				}

				player->showCard(down);
				player->payoff(dealer->isBlackjack(), dealer->isBusted(), dealer->getHandTotal());
				player->writeSplit(up);
			}
		}
	}
	std::cout << "\n";

	report.end = std::time(nullptr);
	report.duration = report.end - report.start;
	std::snprintf(buffer, sizeof(buffer), "      End: table\n");
	std::cout << buffer;
}

//
void Table::runStand() {
    char buffer[256];
	std::snprintf(buffer, sizeof(buffer), "      Start: table, playing %lld hands", parameters->number_of_hands);
	std::cout << buffer << std::endl;

	report.start = std::time(nullptr);
	report.total_hands = 0;
	report.total_rounds = 0;
	while (report.total_hands < parameters->number_of_hands) {
		status(report.total_rounds, report.total_hands);
		shoe->shuffle();
		player->shuffle();
		report.total_rounds++;

		while (!shoe->shouldShuffle()) {
			report.total_hands++;
			dealer->reset();
			player->placeBet();

			dealCards(player->getWager());
			if (dealer->isBlackjack()) {
				continue;
			}

			player->playStand(up, shoe);
			if (!player->bustedOrBlackjack()) {
				while (!dealer->shouldStand()) {
					Card *card = shoe->drawCard();
					dealer->drawCard(card);
					//player->showCard(card);
				}
			}

			//player->showCard(down);
			player->payoff(dealer->isBlackjack(), dealer->isBusted(), dealer->getHandTotal());
			player->writeStand(up);
		}
	}
	std::cout << "\n";

	report.end = std::time(nullptr);
	report.duration = report.end - report.start;
	std::snprintf(buffer, sizeof(buffer), "      End: table\n");
	std::cout << buffer;
}

//
void Table::runHit() {
    char buffer[256];
	std::snprintf(buffer, sizeof(buffer), "      Start: table, playing %lld hands", parameters->number_of_hands);
	std::cout << buffer << std::endl;

	report.start = std::time(nullptr);
	report.total_hands = 0;
	report.total_rounds = 0;
	while (report.total_hands < parameters->number_of_hands) {
		status(report.total_rounds, report.total_hands);
		shoe->shuffle();
		player->shuffle();
		report.total_rounds++;

		while (!shoe->shouldShuffle()) {
			report.total_hands++;
			dealer->reset();
			player->placeBet();

			dealCards(player->getWager());
			if (dealer->isBlackjack()) {
				continue;
			}

			player->playHit(up, shoe);
			if (!player->bustedOrBlackjack()) {
				while (!dealer->shouldStand()) {
					Card *card = shoe->drawCard();
					dealer->drawCard(card);
					//player->showCard(card);
				}
			}

			//player->showCard(down);
			player->payoff(dealer->isBlackjack(), dealer->isBusted(), dealer->getHandTotal());
			player->writeHit(up);
		}
	}
	std::cout << "\n";

	report.end = std::time(nullptr);
	report.duration = report.end - report.start;
	std::snprintf(buffer, sizeof(buffer), "      End: table\n");
	std::cout << buffer;
}

// Function to deal cards
void Table::dealCards(Hand *hand) {
	player->drawCard(hand, shoe->drawCard());
	up = shoe->drawCard();
	dealer->drawCard(up);
	//player->showCard(up);

	player->drawCard(hand, shoe->drawCard());
	down = shoe->drawCard();
	dealer->drawCard(down);
}

//
void Table::status(int64_t round, int64_t hand) {
	if(round == 0) {
		std::cout << std::string("        ") << std::flush;
	}
	if((round + 1) % STATUS_DOT == 0) {
		std::cout << std::string(".") << std::flush;
	}
	if((round + 1) % STATUS_LINE == 0) {
    	char buffer[256];
		std::snprintf(buffer, sizeof(buffer), " : %lld (rounds), %lld (hands)\n", (round + 1), hand);
		std::cout << buffer;
		std::cout << std::string("        ") << std::flush;
	}
}

