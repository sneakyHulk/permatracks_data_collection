#pragma once

#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>

#include "EigenJsonUtils.h"

struct ZeroingResult : Eigen::Vector<double, 3> {};

template <std::size_t N>
std::array<ZeroingResult, N> load_zeroing(std::filesystem::path const& path) {
	std::ifstream stream(path);
	nlohmann::json json = nlohmann::json::parse(stream);
	std::vector transformations = json | std::ranges::views::transform([](nlohmann::basic_json<> const& value) { return value["zeroing"].template get<Eigen::Matrix<double, 3, 1>>(); }) | std::ranges::to<std::vector>();

	std::array<ZeroingResult, N> zeroings;
	for (auto const& [transformation, zeroing] : std::ranges::views::zip(transformations, zeroings)) {
		zeroing << transformation;
	}

	return zeroings;
}