#include "model.hpp"

//
Model::Model(std::string strategy, std::string playbook) {
	filenameDouble = "./models/" + playbook + "-" + strategy + "-double.csv";
    fileDouble.open(filenameDouble);
    if (!fileDouble.is_open()) {
        std::cerr << "Error: Could not open the file: " << filenameDouble << std::endl;
		exit(1);
    }
    fileDouble << "win,total,soft,up\n";

	filenameSplit = "./models/" + playbook + "-" + strategy + "-split.csv";
    fileSplit.open(filenameSplit);
    if (!fileSplit.is_open()) {
        std::cerr << "Error: Could not open the file." << std::endl;
		exit(1);
    }
    fileSplit << "win,total,up\n";

	filenameStand = "./models/" + playbook + "-" + strategy + "-stand.csv";
    fileStand.open(filenameStand);
    if (!fileStand.is_open()) {
        std::cerr << "Error: Could not open the file." << std::endl;
		exit(1);
    }
    fileStand << "win,total,soft,up\n";
}

//
Model::~Model() {
	fileDouble.flush();
    fileDouble.close();

	fileSplit.flush();
    fileSplit.close();

	fileStand.flush();
    fileStand.close();
}

/*
//
void Model::saveStrategy(int total, int soft, int up) {
	buffer = "";
	buffer.append(std::to_string(total));
	buffer.append(",");
	buffer.append(std::to_string(soft));
	buffer.append(",");
	buffer.append(std::to_string(up));
}

//
void Model::saveStrategy(int pair, int up) {
	buffer = "";
	buffer.append(std::to_string(pair));
	buffer.append(",");
	buffer.append(std::to_string(up));
}
*/

//
void Model::writeDoubleStrategy(int total, int soft, int win, int up) {
	fileDouble << (win / 2) << ",";
	fileDouble << (std::to_string(total)) << ",";
	fileDouble << (std::to_string(soft)) << ",";
	fileDouble << (std::to_string(up)) << std::endl;
	fileDouble.flush();
}

//
void Model::writeSplitStrategy(int total, int win, int up) {
	fileSplit << (win / 2) << ",";
	fileSplit << (std::to_string(total)) << ",";
	fileSplit << (std::to_string(up)) << std::endl;
	fileSplit << "\n";
	fileSplit.flush();
}

//
void Model::writeStandStrategy(int total, int soft, int win, int up) {
	fileStand << (win / 2) << ",";
	fileStand << (std::to_string(total)) << ",";
	fileStand << (std::to_string(soft)) << ",";
	fileStand << (std::to_string(up)) << std::endl;
	fileStand.flush();
}

