#ifndef SIMULATOR_HPP
#define SIMULATOR_HPP

#include <string>
#include "parameters.hpp"
#include "rules.hpp"
#include "table.hpp"
#include "report.hpp"
#include "simulation.hpp"
#include "strategy.hpp"

//
class Simulator {
	public:
		Simulator(Parameters* params, Rules* rules, Strategy* strategy);

	private:
		Parameters* parameters;
		Rules* rules;
		Strategy* strategy;
		Table* table;
		Report report;

	public:
		void runDouble();
		void runSplit();
		void runStand();
		void runHit();
		void simulatorRunOnce();
		void write();

	private:
		void simulatorInsert(Simulation* sdt, std::string playbook);
};

#endif // SIMULATOR_HPP
