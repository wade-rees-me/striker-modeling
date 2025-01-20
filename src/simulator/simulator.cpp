#include <iostream>
#include <ctime>
#include <cstdio>
#include <string>
#include <curl/curl.h>
#include <cjson/cJSON.h>
#include "table.hpp"
#include "player.hpp"
#include "simulator.hpp"

//
Simulator::Simulator(Parameters *parameters, Rules *rules, Strategy *strategy)
		: parameters(parameters), rules(rules), strategy(strategy) {
	table = new Table(parameters, rules, strategy);
	report = Report();
}

// The simulator process function
void Simulator::runDouble() {
    char buffer[MAX_BUFFER_SIZE];

    std::snprintf(buffer, sizeof(buffer), "  Start: simulation %s", parameters->name);
	std::cout << buffer << std::endl;
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
    char buffer[MAX_BUFFER_SIZE];

    std::snprintf(buffer, sizeof(buffer), "  Start: simulation %s", parameters->name);
	std::cout << buffer << std::endl;
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
    char buffer[MAX_BUFFER_SIZE];

    std::snprintf(buffer, sizeof(buffer), "  Start: simulation %s", parameters->name);
	std::cout << buffer << std::endl;
	report = Report();
	table->runStand();
    std::snprintf(buffer, sizeof(buffer), "  End: simulation");
	std::cout << buffer << std::endl;

    printf("\n  -- results ---------------------------------------------------------------------\n");
    printf("    %-24s: %lld\n", "Number of hands", report.total_hands);
    printf("    %-24s: %lld seconds\n", "Total time", report.duration);
    printf("  --------------------------------------------------------------------------------\n");
}

// The simulator process function
void Simulator::runHit() {
    char buffer[MAX_BUFFER_SIZE];

    std::snprintf(buffer, sizeof(buffer), "  Start: simulation %s", parameters->name);
	std::cout << buffer << std::endl;
	report = Report();
	table->runHit();
    std::snprintf(buffer, sizeof(buffer), "  End: simulation");
	std::cout << buffer << std::endl;

    printf("\n  -- results ---------------------------------------------------------------------\n");
    printf("    %-24s: %lld\n", "Number of hands", report.total_hands);
    printf("    %-24s: %lld seconds\n", "Total time", report.duration);
    printf("  --------------------------------------------------------------------------------\n");
}

void Simulator::write() {
	table->write();
}

