# Env just for intermediate work without need to rebuild project.
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-24.05"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.conan
    pkgs.clang
    pkgs.cmake
    pkgs.gnumake
    pkgs.clang-clang-tools
  ];

  # Sets environment variables in the workspace
  env = {};
  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      "llvm-vs-code-extensions.vscode-clangd"
      "ms-python.debugpy"
      "ms-python.python"
      "streetsidesoftware.code-spell-checker"
    ];

    # Workspace lifecycle hooks
    workspace = {
      # Runs when a workspace is first created
      onCreate = {
        # Example: install JS dependencies from NPM
        # npm-install = "npm install";
        conan-profile = "conan profile detect";
      };
      # Runs when the workspace is (re)started
      onStart = {
        # Example: start a background task to watch and re-build backend code
        # watch-backend = "npm run watch-backend";
      };
    };
  };
}