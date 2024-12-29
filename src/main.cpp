#include <iostream>
#include <string>
#include <Windows.h>
#include <DbgHelp.h>
#include "DbgHelpManager.hpp"

void printUsage() {
    std::cout << "Usage: winaddr2line -e <PDB_FILE> <ADDRESS>" << std::endl;
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
        printUsage();
        return 1;
    }

    std::string executable, addressStr;
    for (int i = 1; i < argc; ++i) {
        if (std::string(argv[i]) == "-e" && i + 1 < argc) {
            executable = argv[++i];
        } else {
            addressStr = argv[i];
        }
    }

    if (executable.empty() || addressStr.empty()) {
        printUsage();
        return 1;
    }

    DbgHelpManager dbgHelpManager;

    auto baseAddr = dbgHelpManager.loadModule(executable.c_str());

    if (!baseAddr) {
        std::cerr << "Failed to load module.\n";
        return 1;
    }

    // Adding the base address to the input address
    // to align it with the address in the PDB file.
    auto address = parseAddress(addressStr) + baseAddr;

    auto functionName = dbgHelpManager.getSymbolFromAddress(address);
    if (functionName) {
        std::cout << "Function: " << *functionName << "\n";
    } else {
        std::cerr << "Failed to resolve symbol.\n";
    }

    std::string fileName;
    DWORD lineNumber;
    auto result = dbgHelpManager.getLineFromAddress(address);
    if (result) {
        std::tie(fileName, lineNumber) = result.value();
        std::cout << "File: " << fileName << ", Line: " << lineNumber << "\n";
    } else {
        std::cerr << "Failed to resolve line info.\n";
    }

    return 0;
}