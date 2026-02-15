#pragma once

#include <Eigen/Dense>
#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>

#include "EigenJsonUtils.h"

struct EllipsoidFitResult {
	Eigen::Matrix<double, 3, 3> transformation;
	Eigen::Vector<double, 3> center;
};

template <std::size_t N>
std::array<EllipsoidFitResult, N> load_calibration(std::filesystem::path const& path) {
	std::ifstream stream(path);
	nlohmann::json json = nlohmann::json::parse(stream);
	std::vector transformations = json | std::ranges::views::transform([](nlohmann::basic_json<> const& value) { return value["transformation"].template get<Eigen::Matrix<double, 4, 4>>(); }) | std::ranges::to<std::vector>();

	std::array<EllipsoidFitResult, N> calibrations;
	for (auto const& [transformation, calibration] : std::ranges::views::zip(transformations, calibrations)) {
		calibration.transformation = transformation.template block<3, 3>(0, 0);
		calibration.center = -transformation.template block<3, 1>(0, 3);
	}

	return calibrations;
}