#include <iostream>
#include <ctime>
#include <cstdio>
#include <string>
#include <curl/curl.h>
#include <cjson/cJSON.h>
#include "table.hpp"
#include "player.hpp"
#include "simulator.hpp"
#include "constants.hpp"

//
Simulator::Simulator(Parameters* parameters, Rules* rules, Strategy* strategy)
		: parameters(parameters), rules(rules), strategy(strategy) {
	table = new Table(parameters, rules, strategy);
	report = Report();
}

// The simulator process function
void Simulator::runDouble() {
	//Simulation simulation;
    char buffer[MAX_BUFFER_SIZE];

    std::snprintf(buffer, sizeof(buffer), "  Start: simulation %s", parameters->name);
	std::cout << buffer << std::endl;
	//table = new Table(parameters, rules, strategy);
	report = Report();
	table->runDouble();
    std::snprintf(buffer, sizeof(buffer), "  End: simulation");
	std::cout << buffer << std::endl;

	// Print out the results
    printf("\n  -- results ---------------------------------------------------------------------\n");
    printf("    %-24s: %lld\n", "Number of hands", report.total_hands);
    printf("    %-24s: %lld seconds\n", "Total time", report.duration);
    printf("  --------------------------------------------------------------------------------\n");
}

// The simulator process function
void Simulator::runSplit() {
	//Simulation simulation;
    char buffer[MAX_BUFFER_SIZE];

    std::snprintf(buffer, sizeof(buffer), "  Start: simulation %s", parameters->name);
	std::cout << buffer << std::endl;
	//table = new Table(parameters, rules, strategy);
	report = Report();
	table->runSplit();
    std::snprintf(buffer, sizeof(buffer), "  End: simulation");
	std::cout << buffer << std::endl;

    printf("\n  -- results ---------------------------------------------------------------------\n");
    printf("    %-24s: %lld\n", "Number of hands", report.total_hands);
    printf("    %-24s: %lld seconds\n", "Total time", report.duration);
    printf("  --------------------------------------------------------------------------------\n");
}

// The simulator process function
void Simulator::runStand() {
	//Simulation simulation;
    char buffer[MAX_BUFFER_SIZE];

    std::snprintf(buffer, sizeof(buffer), "  Start: simulation %s", parameters->name);
	std::cout << buffer << std::endl;
	//table = new Table(parameters, rules, strategy);
	report = Report();
	table->runStand();
    std::snprintf(buffer, sizeof(buffer), "  End: simulation");
	std::cout << buffer << std::endl;

    printf("\n  -- results ---------------------------------------------------------------------\n");
    printf("    %-24s: %lld\n", "Number of hands", report.total_hands);
    printf("    %-24s: %lld seconds\n", "Total time", report.duration);
    printf("  --------------------------------------------------------------------------------\n");
}

/*
// Function to run the simulation
void Simulator::simulatorRunSimulation() {
	std::cout << "    Start: " + parameters->strategy + " table session" << std::endl;
	table->session(parameters->strategy == "mimic");
	std::cout << "    End: table session" << std::endl;

	//report.total_bet += table->getPlayer()->getReport()->total_bet;
	//report.total_won += table->getPlayer()->getReport()->total_won;
	report.total_rounds += table->getReport()->total_rounds;
	report.total_hands += table->getReport()->total_hands;
	report.duration += table->getReport()->duration;
}
*/

