#pragma once

#include <common_output.h>

#include <csv.hpp>
#include <filesystem>
#include <ranges>

#include "Array.h"
#include "DirectionVector.h"
#include "MagneticFluxDensityData.h"
#include "Message.h"
#include "Pack.h"
#include "Position.h"

template <std::size_t N>
class MagArrayMagneticFluxDensityDataFileReader {
	std::string const name;
	csv::CSVReader reader;
	csv::CSVReader::iterator it;

   public:
	explicit MagArrayMagneticFluxDensityDataFileReader(std::filesystem::path&& path, std::string&& name = "array_v1.1")
	    : name(std::forward<decltype(name)>(name)), reader(path.c_str()) /*path cant be initialized and be used here-> rename path to _path instead*/, it(reader.begin()) {}

	Message<Array<MagneticFluxDensityData, N>> push() {
		Message<Array<MagneticFluxDensityData, N>> ret{};

		if (++it != reader.end()) {
			auto row = *it;

			for (auto i = 0; auto const& out : ret) {
				out = {row[common::stringprint('x', i)].template get<double>(), row[common::stringprint('y', i)].template get<double>(), row[common::stringprint('z', i)].template get<double>()};
				++i;
			}

			ret.src = name;
			try {
				ret.timestamp = row["timestamp"].template get<std::uint64_t>();
			} catch (std::runtime_error const& e) {
				ret.timestamp = 0;
			}
		}

		return ret;
	}
};

template <std::size_t M>
class MagArrayPositionDirectionVectorDataFileReader {
	std::string const name;
	csv::CSVReader reader;
	csv::CSVReader::iterator it;

   public:
	MagArrayPositionDirectionVectorDataFileReader(std::filesystem::path&& path, std::string&& name = "array_v1.1")
	    : name(std::forward<decltype(name)>(name)), reader(path.c_str()) /*path cant be initialized and be used here-> rename path to _path instead*/, it(reader.begin()) {}

	Message<Array<Pack<Position, DirectionVector>, M>> push() {
		Message<Array<Pack<Position, DirectionVector>, M>> ret{};

		if (++it != reader.end()) {
			auto row = *it;

			for (auto i = 0; auto const& out : ret) {
				out = {row[common::stringprint("mag_x", i)].template get<double>(), row[common::stringprint("mag_y", i)].template get<double>(), row[common::stringprint("mag_z", i)].template get<double>(),
				    row[common::stringprint("mag_mx", i)].template get<double>(), row[common::stringprint("mag_my", i)].template get<double>(), row[common::stringprint("mag_mz", i)].template get<double>()};
				++i;
			}

			ret.src = name;
			try {
				ret.timestamp = row["timestamp"].template get<std::uint64_t>();
			} catch (std::runtime_error const& e) {
				ret.timestamp = 0;
			}
		}

		return ret;
	}
};