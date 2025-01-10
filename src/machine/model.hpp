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
		//std::string buffer = "";
		long summary[4][2][22][12][12]; // play, soft, total, pair, up
		long count[4][2][22][12][12];

    	std::string filenameDouble;
    	std::ofstream fileDouble;

    	std::string filenameSplit;
    	std::ofstream fileSplit;

    	std::string filenameStand;
    	std::ofstream fileStand;

    	std::string filenameHit;
    	std::ofstream fileHit;

    	//std::string filenameAll;
    	//std::ofstream fileAll;

    	std::string filenameSummary;
    	std::ofstream fileSummary;

	private:
		void writeStrategy(std::ofstream& fileOut, int play, int soft, int total, int pair, int up, int win);
		void writeAllStrategy(int play, int soft, int total, int pair, int up, int win);

	public:
		void writeDoubleStrategy(int soft, int total, int up, int win);
		void writeSplitStrategy(int total, int win, int up);
		void writeStandStrategy(int total, int soft, int win, int up);
		void writeHitStrategy(int total, int soft, int win, int up);
		void write();
};

#endif // MODEL_HPP
