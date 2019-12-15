import os
from conans import ConanFile, CMake, tools


class OpenpnpCaptureConan(ConanFile):
    name = "openpnp-capture"
    version = "0.0.17"
    license = "MIT"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/openpnp/openpnp-capture"
    description = "A cross platform video capture library with a focus on machine vision."
    topics = ("vision", "capture")
    settings = "os", "compiler", "build_type", "arch"
    requires = "libjpeg-turbo/2.0.2@bincrafters/stable"
    generators = "cmake"
    _source_subfolder = "openpnp-capture-0.0.17"

    def patch_sources(self):
        tools.replace_in_file(
            os.path.join(self._source_subfolder, "CMakeLists.txt"),
            "project (openpnp-capture)", '''project (openpnp-capture)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)''')
        tools.replace_in_file(
            os.path.join(self._source_subfolder, "CMakeLists.txt"),
            "add_subdirectory(linux/contrib/libjpeg-turbo-dev)", '''
find_package(JPEG REQUIRED)
message("JPEG library found: ${JPEG_FOUND}")''')
        tools.replace_in_file(
            os.path.join(self._source_subfolder, "CMakeLists.txt"),
            "target_link_libraries(openpnp-capture turbojpeg-static)",
            "target_link_libraries(openpnp-capture CONAN_PKG::libjpeg-turbo)")
        tools.replace_in_file(
            os.path.join(self._source_subfolder, "CMakeLists.txt"),
            "add_subdirectory(linux/tests)", "")
        tools.replace_in_file(
            os.path.join(self._source_subfolder, "CMakeLists.txt"),
            "add_subdirectory(mac/tests)", "")
        tools.replace_in_file(
            os.path.join(self._source_subfolder, "CMakeLists.txt"),
            "add_subdirectory(win/tests)", "")

    def source(self):
        tools.get(
            "https://github.com/openpnp/openpnp-capture/archive/v0.0.17.zip")
        self.patch_sources()

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder)
        cmake.build()

    def package(self):
        self.copy("LICENSE.txt", dst="licenses", src=self._source_subfolder)
        self.copy("*.h",
                  dst="include",
                  src=os.path.join(self._source_subfolder, "include"))
        self.copy("*.*",
                  dst=os.path.join("include", "common"),
                  src=os.path.join(self._source_subfolder, "common"))
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
