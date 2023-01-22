from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.microsoft import check_min_vs, is_msvc_static_runtime, is_msvc
from conan.tools.files import apply_conandata_patches, export_conandata_patches, get, copy, rm, rmdir, replace_in_file
from conan.tools.build import check_min_cppstd
from conan.tools.scm import Version
from conan.tools.cmake import cmake_layout, CMake
from conan.tools.gnu import PkgConfigDeps
from conan.tools.env import VirtualBuildEnv
from conan.tools.env import Environment

import os


required_conan_version = ">=1.53.0"


class OpenpnpCaptureConan(ConanFile):
    name = "openpnp-capture"
    description = "A cross platform video capture library with a focus on machine vision."
    topics = ("vision", "capture")
    license = "MIT"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/openpnp/openpnp-capture"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "PkgConfigDeps", "CMakeDeps"

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": True,
        "fPIC": True,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        self.requires("libjpeg-turbo/2.1.4")

    #def build_requirements(self):
    #    if self.settings.os == "Linux":
    #        self.build_requires("pkgconf/1.7.4")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), 
        'include_directories(SYSTEM "${CMAKE_CURRENT_SOURCE_DIR}/linux/contrib/libjpeg-turbo-dev")', "")
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), 
        'if( TurboJPEG_FOUND )', "if( TurboJPEG_FOUND )\nmessage('------->>> >>>> JJJAJSDJSAKDKSKSKAJKKKDJ')")
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("LICENSE.md", src=self._source_subfolder, dst="licenses")
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["pthread"]
        self.cpp_info.libs = ["openpnp-capture"]
