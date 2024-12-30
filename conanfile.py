from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.build import check_min_cppstd
from conan.tools.env import Environment


class winaddr2lineRecipe(ConanFile):
    name = "winaddr2line"
    version = "0.0.1"
    package_type = "application"
    

    # Optional metadata
    license = "MIT"
    author = "Maciej Czarnecki"
    url = "https://github.com/McCzarny/winaddr2line"
    description = "A small tool for getting symbol based on the address"
    topics = ("windows", "debugging", "pdb")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "src/*", "include/*", "test_package/*"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)
    
    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

        environment = Environment()
        environment.define("CTEST_OUTPUT_ON_FAILURE", "1")
        envvars = environment.vars(self)
        with envvars.apply():
            cmake.test(cli_args=["--verbose"])

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def requirements(self):
        pass

    def build_requirements(self):
        pass

    def validate(self):
        check_min_cppstd(self, "17")
