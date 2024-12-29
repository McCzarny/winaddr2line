#pragma once

#include <Windows.h>
#include <DbgHelp.h>
#include <iostream>
#include <optional>

/**
 * @class DbgHelpManager
 * @brief Manages the DbgHelp library for symbol loading and debugging.
 * @details initialization and cleanup can be done with initialize() and cleanup()
 * or automatically when needed.
*/
class DbgHelpManager {
public:
    DbgHelpManager();
    ~DbgHelpManager();

    DbgHelpManager(const DbgHelpManager&) = delete;
    DbgHelpManager& operator=(const DbgHelpManager&) = delete;

    /**
     * @brief Initializes the DbgHelp library.
     * @return True if initialization is successful, false otherwise.
     */
    bool initialize();

    /**
     * @brief Loads a module from a PDB file.
     * @param pdb_file Path to the PDB file.
     * @return Base address of the loaded module or 0 if an error occurs.
     */
    uintptr_t loadModule(const char* pdb_file);

    /**
     * @brief Cleans up the DbgHelp library.
     */
    void cleanup();

    /**
     * @brief Returns the handle to the process used by DbgHelp.
     * @return Handle to the process.
     */
    HANDLE getProcess() const;

    std::optional<std::string> getSymbolFromAddress(DWORD64 address);
    std::optional<std::pair<std::string, DWORD>> getLineFromAddress(DWORD64 address);

private:
    HANDLE process; ///< Handle to the process.
    bool initialized; ///< Indicates if the library is initialized.
};
