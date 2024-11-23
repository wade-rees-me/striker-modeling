#ifndef MODEL_HPP
#define MODEL_HPP

#include <iostream>
#include <fstream>
#include <string>

//
class Model {
	public:
		Model(std::string strategy, std::string playbook);
    	~Model();

	private:
		std::string buffer = "";

    	std::string filenameDouble;
    	std::ofstream fileDouble;

    	std::string filenameSplit;
    	std::ofstream fileSplit;

    	std::string filenameStand;
    	std::ofstream fileStand;

	public:
		//void saveStrategy(int total, int soft, int up);
		//void saveStrategy(int pair, int up);
		void writeDoubleStrategy(int total, int soft, int win, int up);
		void writeSplitStrategy(int total, int win, int up);
		void writeStandStrategy(int total, int soft, int win, int up);
};

#endif // MODEL_HPP
