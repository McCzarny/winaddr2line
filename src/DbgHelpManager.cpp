#include "DbgHelpManager.hpp"

DbgHelpManager::DbgHelpManager()
    : process(GetCurrentProcess()), initialized(false) {}

DbgHelpManager::~DbgHelpManager()
{
    cleanup();
}

bool DbgHelpManager::initialize()
{
    if (initialized)
    {
        std::cerr << "DbgHelp already initialized.\n";
        return false;
    }

    SymSetOptions(SYMOPT_LOAD_LINES);
    if (!SymInitialize(process, NULL, TRUE))
    {
        std::cerr << "Failed to initialize DbgHelp.\n";
        return false;
    }
    initialized = true;
    return true;
}

uintptr_t DbgHelpManager::loadModule(const char *pdb_file)
{
    if (!initialized)
    {
        // If not initialized, initialize and try again.
        initialize();
        if (!initialized)
        {
            return 0;
        }
    }

    // The input base address is 0x400000 as we cannot use 0x0.
    return (uintptr_t)SymLoadModuleEx(process, NULL, pdb_file, NULL, 0x400000, 0x7fffffff, NULL, 0);
}

void DbgHelpManager::cleanup()
{
    if (!initialized)
    {
        return;
    }
    initialized = false;
    SymCleanup(process);
}

HANDLE DbgHelpManager::getProcess() const
{
    return process;
}

std::optional<std::string> DbgHelpManager::getSymbolFromAddress(DWORD64 address) {
    DWORD64 displacement = 0;
    char buffer[sizeof(SYMBOL_INFO) + MAX_SYM_NAME * sizeof(TCHAR)] = {0};
    PSYMBOL_INFO symbol = reinterpret_cast<PSYMBOL_INFO>(buffer);
    symbol->SizeOfStruct = sizeof(SYMBOL_INFO);
    symbol->MaxNameLen = MAX_SYM_NAME;

    if (SymFromAddr(getProcess(), address, &displacement, symbol)) {
        return symbol->Name;
    }
    return std::nullopt;
}

std::optional<std::pair<std::string, DWORD>> DbgHelpManager::getLineFromAddress(DWORD64 address) {
    IMAGEHLP_LINE64 line = {0};
    line.SizeOfStruct = sizeof(IMAGEHLP_LINE64);
    DWORD lineDisplacement = 0;

    if (SymGetLineFromAddr64(getProcess(), address, &lineDisplacement, &line)) {

        return std::make_pair(line.FileName, line.LineNumber);
    }
    return std::nullopt;
}
