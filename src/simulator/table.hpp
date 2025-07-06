#ifndef TABLE_HPP
#define TABLE_HPP

#include "parameters.hpp"
#include "rules.hpp"
#include "player.hpp"
#include "dealer.hpp"
#include "shoe.hpp"
#include "report.hpp"
#include "strategy.hpp"

class Table {
	public:
		Table(Parameters *params, Rules *rules, Strategy *strategy);
		~Table();

	private:
		Parameters *parameters;
		Shoe *shoe;
		Dealer *dealer;
		Player *player;
		Report report;
		Card *up;
		Card *down;

	public:
		void runDouble();
		void runSplit();
		void runStand();
		void runHit();
		void dealCards(Hand *hand);
		void show(Card *card);
		Player *getPlayer() {
			return player;
		}
		Report *getReport() {
			return &report;
		}
		void write();

	private:
		void status(int64_t round, int64_t hand);
};

#endif // TABLE_HPP
