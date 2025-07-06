#include "model.hpp"
#include "constants.hpp"

#define PLAY_DOUBLE 0
#define PLAY_SPLIT 1
#define PLAY_STAND 2
#define PLAY_HIT 3

const char *str_play[] = {"double", "split", "stand", "hit"};
const char *str_cards[] = {"", "", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "ace"};
const char *str_soft[] = {"hard", "soft", "pair"};

//
Model::Model(std::string strategy, std::string playbook) {
 	std::string dataPath = getResourcesUrl() + "/data/" + playbook + "-" + strategy;

	for (int p = 0; p < 4; p++) {
		for (int s = 0; s < 2; s++) {
			for (int t = 0; t <= 21; t++) {
				for (int x = 0; x <= 11; x++) {
					for (int u = 0; u <= 11; u++) {
						summary[p][s][t][x][u] = 0;
						count[p][s][t][x][u] = 0;
					}
				}
			}
		}
	}

	filenameDouble = dataPath + "-double.csv";
    fileDouble.open(filenameDouble);
    if (!fileDouble.is_open()) {
        std::cerr << "Error: Could not open the file: " << filenameDouble << std::endl;
		exit(1);
    }
    fileDouble << "play,soft,total,pair,up,win\n";

	filenameSplit = dataPath + "-split.csv";
    fileSplit.open(filenameSplit);
    if (!fileSplit.is_open()) {
        std::cerr << "Error: Could not open the file." << std::endl;
		exit(1);
    }
    fileSplit << "play,soft,total,pair,up,win\n";

	filenameStand = dataPath + "-stand.csv";
    fileStand.open(filenameStand);
    if (!fileStand.is_open()) {
        std::cerr << "Error: Could not open the file." << std::endl;
		exit(1);
    }
    fileStand << "play,soft,total,pair,up,win\n";

	filenameHit = dataPath + "-hit.csv";
    fileHit.open(filenameHit);
    if (!fileHit.is_open()) {
        std::cerr << "Error: Could not open the file." << std::endl;
		exit(1);
    }
    fileHit << "play,soft,total,pair,up,win\n";

	filenameSummary = dataPath + "-summary.csv";
    fileSummary.open(filenameSummary);
    if (!fileSummary.is_open()) {
        std::cerr << "Error: Could not open the file." << std::endl;
		exit(1);
    }
    fileSummary << "play,soft,total,pair,up,win\n";
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
}

//
void Model::writeDoubleStrategy(int soft, int total, int up, int win) {
	writeStrategy(fileDouble, PLAY_DOUBLE, soft, total, 0, up, win);
}

//
void Model::writeSplitStrategy(int pair, int win, int up) {
	writeStrategy(fileSplit, PLAY_SPLIT, 2, 0, pair, up, win);
}

//
void Model::writeStandStrategy(int total, int soft, int win, int up) {
	writeStrategy(fileStand, PLAY_STAND, soft, total, 0, up, win);
}

//
void Model::writeHitStrategy(int total, int soft, int win, int up) {
	writeStrategy(fileHit, PLAY_HIT, soft, total, 0, up, win);
}

//
void Model::writeStrategy(std::ofstream& fileOut, int play, int soft, int total, int pair, int up, int win) {
	if(win > 8 || win < -8) {
		return;
	}

	fileOut << (std::to_string(play)) << ",";
	fileOut << (std::to_string(soft)) << ",";
	fileOut << (total > 0 ? std::to_string(total) : "0") << ",";
	fileOut << (std::to_string(pair)) << ",";
	fileOut << (std::to_string(up)) << ",";
	fileOut << (std::to_string(win)) << std::endl;

	fileOut.flush();

    writeAllStrategy(play, soft, total, pair, up, win);
}

//
void Model::writeAllStrategy(int play, int soft, int total, int pair, int up, int win) {
	summary[play][soft][total][pair][up] += win;
	count[play][soft][total][pair][up]++;
}

//
void Model::write() {
    char buffer[MAX_BUFFER_SIZE];

	printf("\n");
	for (int play = 0; play < 4; play++) {
		if (play == 1) {
			for (int p = 2; p <= 11; p++) {
				for (int u = 2; u <= 11; u++) {
					if (count[play][0][0][p][u] > 0) {
						std::snprintf(buffer, MAX_BUFFER_SIZE, "%-6s - %-4s %-6s vs %-6s = %8ld", str_play[play], "pair", str_cards[p], str_cards[u], summary[play][0][0][p][u]);
						fileSummary << buffer << std::endl;
					}
				}
			}
		} else {
			for (int s = 0; s < 2; s++) {
				for (int t = 0; t <= 21; t++) {
					for (int u = 2; u <= 11; u++) {
						if (count[play][s][t][0][u] > 0) {
							std::snprintf(buffer, MAX_BUFFER_SIZE, "%-6s - %-4s %2d vs %-6s = %8ld", str_play[play], str_soft[s], t, str_cards[u], summary[play][s][t][0][u]);
							fileSummary << buffer << std::endl;
						}
					}
				}
			}
		}
	}
	fileSummary.flush();
}

