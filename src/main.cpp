#include "arguments.hpp"
#include "parameters.hpp"
#include "rules.hpp"
#include "simulator.hpp"
#include "strategy.hpp"
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <string>

//
int main(int argc, char *argv[]) {
  std::cout << "Start: " << STRIKER_WHO_AM_I << std::endl;
  Arguments arguments(argc, argv);
  Parameters parameters(&arguments);
  Rules rules(arguments.getDecks());
  Strategy strategy(arguments.getDecks(), arguments.getStrategy(), arguments.getNumberOfDecks());
  Simulator simulator(&parameters, &rules, &strategy);

  std::cout << "  -- arguments -------------------------------------------------------------------" << std::endl;
  parameters.print();
  rules.print();
  std::cout << "  --------------------------------------------------------------------------------" << std::endl << std::endl;

  simulator.runDouble();
  simulator.runSplit();
  simulator.runStand();
  simulator.runHit();

  simulator.write();

  std::cout << "End: " << STRIKER_WHO_AM_I << std::endl;

  return 0;
}

