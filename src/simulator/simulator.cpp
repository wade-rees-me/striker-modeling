#include "simulator.hpp"
//
//#include <cjson/cJSON.h>
//#include <curl/curl.h>

#include <cstdio>
#include <ctime>
#include <iostream>
#include <string>

//#include "player.hpp"
#include "table.hpp"

//
Simulator::Simulator(Parameters *parameters, Rules *rules, Strategy *strategy)
    : parameters(parameters), rules(rules), strategy(strategy) {
  table = new Table(parameters, rules, strategy);
  report = Report();
}

// The simulator process function
void Simulator::beg() {
  std::cout << "  Start: simulation " << parameters->name << std::endl;
}

// The simulator process function
void Simulator::end() {
  Report *tableReport = table->getReport();

  std::cout << "  End: simulation " << std::endl;
  printf("\n  -- results ---------------------------------------------------------------------\n");
  printf("    %-24s: %ld\n", "Number of hands", tableReport->total_hands);
  printf("    %-24s: %ld seconds\n", "Total time", tableReport->duration);
  printf("  --------------------------------------------------------------------------------\n\n");
}

// The simulator process function
void Simulator::runDouble() {
  beg();
  table->runDouble();
  end();
}

// The simulator process function
void Simulator::runSplit() {
  beg();
  table->runSplit();
  end();
}

// The simulator process function
void Simulator::runStand() {
  beg();
  table->runStand();
  end();
}

// The simulator process function
void Simulator::runHit() {
  beg();
  table->runHit();
  end();
}

void Simulator::write() {
	table->write();
}

