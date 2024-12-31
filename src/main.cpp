#include <iostream>
#include <string>
#include <Windows.h>
#include <DbgHelp.h>
#include "DbgHelpManager.hpp"
#include <vector>

void printUsage() {
    std::cout << "Usage: winaddr2line -e <PDB_FILE> [-f] <ADDRESS>" << std::endl;
    std::cout << "Options:" << std::endl;
    std::cout << "  -e <PDB_FILE>  Specify the PDB file to use for symbol resolution." << std::endl;
    std::cout << "  -f             Show the function name in addition to the address." << std::endl;
    std::cout << "  <ADDRESS>...   The address to resolve." << std::endl;
}

uintptr_t parseAddress(const std::string& address) {
    try {
        return std::stoull(address, nullptr, 0);
    } catch (const std::exception& e) {
        std::cerr << "Invalid address format: " << e.what() << std::endl;
        exit(1);
    }
}

int main(int argc, char *argv[]) {
    if (argc < 4) {
        std::cerr << "Invalid number of arguments: " << argc << std::endl;
        printUsage();
        return 1;
    }

    std::string executable;
    std::vector<std::string> addresses;
    bool showFunction = false;
    for (int i = 1; i < argc; ++i) {
        if (std::string(argv[i]) == "-e" && i + 1 < argc) {
            executable = argv[++i];
        } else if (std::string(argv[i]) == "-f") {
            showFunction = true;
        } else {
            addresses.push_back(argv[i]);
        }
    }

    if (executable.empty() || addresses.empty()) {
        printUsage();
        return 1;
    }

    DbgHelpManager dbgHelpManager;

    auto baseAddr = dbgHelpManager.loadModule(executable.c_str());

    if (!baseAddr) {
        std::cerr << "Failed to load module.\n";
        return 1;
    }

    for (const auto& addressStr : addresses) {
        std::string addrStr = addressStr;
        if (addrStr.size() > 2 && addrStr.substr(0, 2) != "0x") {
            addrStr = "0x" + addrStr;
        }

        // Adding the base address to the input address
        // to align it with the address in the PDB file.
        auto address = parseAddress(addrStr) + baseAddr;

        if (showFunction) {
            auto functionName = dbgHelpManager.getSymbolFromAddress(address);
            if (functionName) {
                std::cout << *functionName << "\n";
            } else {
                std::cerr << "Failed to resolve symbol.\n";
            }
        }

        std::string fileName;
        DWORD lineNumber;
        auto result = dbgHelpManager.getLineFromAddress(address);
        if (result) {
            std::tie(fileName, lineNumber) = result.value();
            std::cout << fileName << ":" << lineNumber << "\n";
        } else {
            std::cerr << "Failed to resolve line info.\n";
        }
    }

    return 0;
}