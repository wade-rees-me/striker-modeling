#include "model.hpp"

//
Model::Model(std::string strategy, std::string playbook) {
	filenameDouble = "./data/" + playbook + "-" + strategy + "-double.csv";
    fileDouble.open(filenameDouble);
    if (!fileDouble.is_open()) {
        std::cerr << "Error: Could not open the file: " << filenameDouble << std::endl;
		exit(1);
    }
    fileDouble << "win,total,soft,up\n";

	filenameSplit = "./data/" + playbook + "-" + strategy + "-split.csv";
    fileSplit.open(filenameSplit);
    if (!fileSplit.is_open()) {
        std::cerr << "Error: Could not open the file." << std::endl;
		exit(1);
    }
    fileSplit << "win,total,up\n";

	filenameStand = "./data/" + playbook + "-" + strategy + "-stand.csv";
    fileStand.open(filenameStand);
    if (!fileStand.is_open()) {
        std::cerr << "Error: Could not open the file." << std::endl;
		exit(1);
    }
    fileStand << "win,total,soft,up\n";

	filenameHit = "./data/" + playbook + "-" + strategy + "-hit.csv";
    fileHit.open(filenameHit);
    if (!fileHit.is_open()) {
        std::cerr << "Error: Could not open the file." << std::endl;
		exit(1);
    }
    fileHit << "win,total,soft,up\n";

	filenameAll = "./data/" + playbook + "-" + strategy + ".csv";
    fileAll.open(filenameAll);
    if (!fileAll.is_open()) {
        std::cerr << "Error: Could not open the file." << std::endl;
		exit(1);
    }
    fileAll << "play,total,soft,up,win\n";
}

//
Model::~Model() {
	fileDouble.flush();
    fileDouble.close();

	fileSplit.flush();
    fileSplit.close();

	fileStand.flush();
    fileStand.close();

	fileHit.flush();
    fileHit.close();

	fileAll.flush();
    fileAll.close();
}

//
void Model::writeDoubleStrategy(int total, int soft, int win, int up) {
	fileDouble << win << ",";
	fileDouble << (std::to_string(total)) << ",";
	fileDouble << (std::to_string(soft)) << ",";
	fileDouble << (std::to_string(up)) << std::endl;
	fileDouble.flush();
    writeStrategy(total, 1, soft, win, up);
}

//
void Model::writeSplitStrategy(int total, int win, int up) {
	fileSplit << win << ",";
	fileSplit << (std::to_string(total)) << ",";
	fileSplit << (std::to_string(up)) << std::endl;
	fileSplit.flush();
    writeStrategy(total, 2, 0, win, up);
}

//
void Model::writeStandStrategy(int total, int soft, int win, int up) {
	fileStand << win << ",";
	fileStand << (std::to_string(total)) << ",";
	fileStand << (std::to_string(soft)) << ",";
	fileStand << (std::to_string(up)) << std::endl;
	fileStand.flush();
    writeStrategy(total, 3, soft, win, up);
}

//
void Model::writeHitStrategy(int total, int soft, int win, int up) {
	fileHit << win << ",";
	fileHit << (std::to_string(total)) << ",";
	fileHit << (std::to_string(soft)) << ",";
	fileHit << (std::to_string(up)) << std::endl;
	fileHit.flush();
    writeStrategy(total, 4, soft, win, up);
}

//
void Model::writeStrategy(int total, int play, int soft, int win, int up) {
	fileAll << (std::to_string(play) ) << ",";
	fileAll << (std::to_string(total)) << ",";
	fileAll << (std::to_string(soft)) << ",";
	fileAll << (std::to_string(up)) << ",";
	fileAll << (std::to_string(win)) << std::endl;
	fileAll.flush();
}

