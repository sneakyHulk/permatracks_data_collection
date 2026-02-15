cmake_minimum_required(VERSION 3.22)
project(permatracks_data_collection)

include(FetchContent)

set(CMAKE_CXX_STANDARD 23)

### add local libraries
FetchContent_Declare(permatracks_msg SOURCE_DIR ${PROJECT_SOURCE_DIR}/external/msg)
FetchContent_MakeAvailable(permatracks_msg)
add_library(permatracks_msg_${PROJECT_NAME} ALIAS permatracks_msg)
set_target_properties(permatracks_msg PROPERTIES EXCLUDE_FROM_ALL TRUE)

FetchContent_Declare(common SOURCE_DIR ${PROJECT_SOURCE_DIR}/external/common)
FetchContent_MakeAvailable(common)
add_library(common_${PROJECT_NAME} ALIAS common)
set_target_properties(common PROPERTIES EXCLUDE_FROM_ALL TRUE)

FetchContent_Declare(csv SOURCE_DIR ${PROJECT_SOURCE_DIR}/thirdparty/csv)
FetchContent_MakeAvailable(csv)
add_library(csv_${PROJECT_NAME} ALIAS csv)
set_target_properties(csv PROPERTIES EXCLUDE_FROM_ALL TRUE)

### Boost
find_package(Boost CONFIG REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(nlohmann_json REQUIRED)

add_library(${PROJECT_NAME}
        src/MagArrayParser.cpp
        src/SerialConnection.cpp
)
target_include_directories(${PROJECT_NAME} PUBLIC include)
target_include_directories(${PROJECT_NAME} PUBLIC ${Boost_INCLUDE_DIRS})
target_link_libraries(${PROJECT_NAME} PUBLIC permatracks_msg)
target_link_libraries(${PROJECT_NAME} PUBLIC common)
target_link_libraries(${PROJECT_NAME} PUBLIC ${Boost_LIBRARIES})
target_compile_definitions(${PROJECT_NAME} PUBLIC SERIALCONNECTION_USE_BOOST)

add_library(${PROJECT_NAME}_file
        src/MagArrayMagneticFluxDensityDataFileReader.cpp
        src/MagArrayMagneticFluxDensityDataFileWriter.cpp
        src/zeroing.cpp
        src/calibration.cpp
)
target_include_directories(${PROJECT_NAME}_file PUBLIC ${Boost_INCLUDE_DIRS})
target_link_libraries(${PROJECT_NAME}_file PUBLIC csv)
target_link_libraries(${PROJECT_NAME}_file PUBLIC permatracks_msg)
target_link_libraries(${PROJECT_NAME}_file PUBLIC Eigen3::Eigen)
target_link_libraries(${PROJECT_NAME}_file PUBLIC nlohmann_json::nlohmann_json)
target_link_libraries(${PROJECT_NAME}_file PUBLIC eigen_utils)
target_link_libraries(${PROJECT_NAME}_file PUBLIC ${PROJECT_NAME})

# testing
add_executable(test_${PROJECT_NAME}
        test/test_${PROJECT_NAME}.cpp)
target_link_libraries(test_${PROJECT_NAME} PUBLIC ${PROJECT_NAME})

add_executable(test_${PROJECT_NAME}_file
        test/test_${PROJECT_NAME}_file.cpp)
target_link_libraries(test_${PROJECT_NAME}_file PUBLIC ${PROJECT_NAME}_file)

target_compile_definitions(test_${PROJECT_NAME}_file PRIVATE CMAKE_SOURCE_DIR="${CMAKE_SOURCE_DIR}")

enable_testing()

add_test(NAME test_${PROJECT_NAME} COMMAND $<TARGET_FILE:test_${PROJECT_NAME}> WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})
add_test(NAME test_${PROJECT_NAME}_file COMMAND $<TARGET_FILE:test_${PROJECT_NAME}_file> WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})