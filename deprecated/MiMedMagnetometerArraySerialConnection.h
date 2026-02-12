#pragma once
#include <common_output.h>

#include <boost/asio.hpp>
#include <boost/circular_buffer.hpp>
#include <boost/regex.hpp>
#include <chrono>
#include <ranges>

#include "Array.h"
#include "MagneticFluxDensityData.h"
#include "Message.h"

template <std::size_t N>
class MiMedMagnetometerArraySerialConnection {
	std::chrono::system_clock::time_point start = std::chrono::system_clock::now();
	boost::asio::io_context& io;
	boost::asio::serial_port serial;

   public:
	static constexpr boost::regex get_regex() {
		std::stringstream regex;
		char space[]{0, 0};  //, 0}

		regex << R"(\[0*([0-9]+)\]: )";
		for (std::size_t i = 0; i < N; ++i) regex << space << R"('([A-Z0-9]+) (0?[0-9]+)'\(([0-9]+),(-?[0-9]+.[0-9][0-9]),(-?[0-9]+.[0-9][0-9]),(-?[0-9]+.[0-9][0-9])\))", *space = ',';  //, *(space + 1) = ' ';
		regex << R"(;)";

		return boost::regex(regex.str().c_str());
	}

#ifdef __APPLE__
	explicit MiMedMagnetometerArraySerialConnection(boost::asio::io_context& io, std::string const& port = "/dev/cu.usbserial-0001", unsigned int const baud_rate = 230400)
#else
	explicit MiMedMagnetometerArraySerialConnection(boost::asio::io_context& io, std::string const& port = "/dev/ttyUSB0", unsigned int const baud_rate = 230400)
#endif
	    : io(io), serial(io, port) {

		serial.set_option(boost::asio::serial_port_base::baud_rate(baud_rate));
		serial.set_option(boost::asio::serial_port_base::character_size(8));
		serial.set_option(boost::asio::serial_port_base::parity(boost::asio::serial_port_base::parity::none));
		serial.set_option(boost::asio::serial_port_base::stop_bits(boost::asio::serial_port_base::stop_bits::one));
		serial.set_option(boost::asio::serial_port_base::flow_control(boost::asio::serial_port_base::flow_control::none));
	}
	Message<Array<MagneticFluxDensityData, N>> push() {
		static std::array<char, 4096> buf{};
		static boost::circular_buffer<char> buffer = boost::circular_buffer<char>(8192);
		static boost::regex const regex = get_regex();

		boost::match_results<boost::circular_buffer<char>::const_iterator> match;
		boost::system::error_code ec;
		do {
			std::size_t const bytes_transferred = serial.read_some(boost::asio::buffer(buf), ec);
			buffer.insert(buffer.end(), buf.begin(), buf.begin() + bytes_transferred);

			if (ec) {
				common::println_critical_loc(ec.message());
			}
		} while (!boost::regex_search(buffer.cbegin(), buffer.cend(), match, regex));

		Message<Array<MagneticFluxDensityData, N>> out;
		out.timestamp = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now() - start).count();
		out.src = "array_v1";

		std::array<unsigned int, N> timestamps;
		for (auto i = 4, j = 0; j < N; ++j, i += 2) {
			// if (match.str(i++) == "LIS3MDL") {
			//	out[j].sensor_type = SENSOR_TYPE::LIS3MDL;
			// } else if (match.str(i) == "MMC5983MA") {
			//	out[j].sensor_type = SENSOR_TYPE::MMC5983MA;
			// } else {
			//	out[j].sensor_type = SENSOR_TYPE::UNKNOWN;
			// }

			// out[j].sensor_id = std::stoul(match.str(i++));

			timestamps[j] = std::stoul(match.str(i++));

			out[j].x = std::stod(match.str(i++)) * 1e-6;
			out[j].y = std::stod(match.str(i++)) * 1e-6;
			out[j].z = std::stod(match.str(i++)) * 1e-6;
		}

		auto [min, max] = std::ranges::minmax_element(timestamps);
		if (*max - *min > 5) {
			common::println_warn_loc("Time difference across all measurements exceeds 5ms! Is '", std::chrono::milliseconds(*max - *min), "'.");
		}

		return out;
	}

	~MiMedMagnetometerArraySerialConnection() { common::println_debug_loc("Closing connection."); }
};