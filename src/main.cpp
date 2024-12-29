#include <iostream>

int main(int argc, char *argv[]) {
  if (argc < 4) {
    std::cout << "Usage: winaddr2line -e <EXECUTABLE> <ADDRESS>";
  }

  return 0;
}