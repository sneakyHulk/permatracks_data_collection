#include <MagArrayParser.h>
#include <MagneticFluxDensityData.h>
#include <MagneticFluxDensityDataRawAK09940A.h>
#include <MagneticFluxDensityDataRawLIS3MDL.h>
#include <MagneticFluxDensityDataRawMMC5983MA.h>
#include <SerialConnection.h>
#include <calibration.h>
#include <zeroing.h>

#include <Eigen/Dense>
#include <expected>
#include <fstream>

class DataPrinterV1 : public virtual SerialConnection, public MagArrayParser<SENSOR_TYPE<MagneticFluxDensityDataRawLIS3MDL, 25, 16>, SENSOR_TYPE<MagneticFluxDensityDataRawMMC5983MA, 0, 25>> {
	void handle_parse_result(Message<Array<MagneticFluxDensityData, total_mag_sensors>>& magnetic_flux_density_message) override { std::cout << magnetic_flux_density_message << std::endl; }

   public:
#if defined(_WIN32)
	std::expected<void, common::Error> connect(std::string port) {
#elif defined(__APPLE__)
	std::expected<void, common::Error> connect(std::string port = "/dev/cu.usbserial-0001"){
#elif defined(__linux__)
	std::expected<void, common::Error> connect(std::string const& port = "/dev/ttyUSB0") {
#endif
		return open_serial_port(port);
	}
};

class DataWriterV2 : public virtual SerialConnection, public MagArrayParser<SENSOR_TYPE<MagneticFluxDensityDataRawAK09940A, 0, 111>> {
	void handle_parse_result(Message<Array<MagneticFluxDensityData, total_mag_sensors>>& magnetic_flux_density_message) override {
		for (auto const& [calibration, zeroing, magnetometer_datapoint] : std::ranges::views::zip(calibrations, zeroings, magnetic_flux_density_message)) {
			Eigen::Vector<double, 3> tmp;
			tmp << magnetometer_datapoint.x, magnetometer_datapoint.y, magnetometer_datapoint.z;

			tmp = calibration.transformation * (tmp - calibration.center) - zeroing;
			magnetometer_datapoint.x = tmp.x();
			magnetometer_datapoint.y = tmp.y();
			magnetometer_datapoint.z = tmp.z();
		}

		file << magnetic_flux_density_message.timestamp;
		for (const auto& [x, y, z] : magnetic_flux_density_message) {
			file << "," << x;
			file << "," << y;
			file << "," << z;
		}
		file << std::endl;
	}

	std::ofstream file;
	std::array<EllipsoidFitResult, total_mag_sensors> calibrations;
	std::array<ZeroingResult, total_mag_sensors> zeroings;

   public:
	DataWriterV2(std::array<EllipsoidFitResult, total_mag_sensors> const& calibrations, std::array<ZeroingResult, total_mag_sensors> const& zeroings,
	    std::filesystem::path const& filepath = std::filesystem::path(CMAKE_SOURCE_DIR) / "result" / common::stringprint("mag_data_111", std::chrono::system_clock::now()))
	    : calibrations(calibrations), zeroings(zeroings), file(filepath) {
		std::cout << "file created at " << filepath << std::endl;

		file << "timestamp";
		for (auto i = 0; i < total_mag_sensors; ++i) {
			file << ",x" << i;
			file << ",y" << i;
			file << ",z" << i;
		}
		file << std::endl;
	}

#if defined(_WIN32)
	std::expected<void, common::Error> connect(std::string port) {
#elif defined(__APPLE__)
	std::expected<void, common::Error> connect(std::string port = "/dev/cu.usbmodem3958386634341"){
#elif defined(__linux__)
	std::expected<void, common::Error> connect(std::string const& port = "/dev/ttyACM0") {
#endif
		return open_serial_port(port);
	}
};

int main() {
	auto const calibrations = load_calibration<111>(std::filesystem::path(CMAKE_SOURCE_DIR) / "data" / "examples" / "calibration_2026-02-13_14-21-51.json");
	auto const zeroings = load_zeroing<111>(std::filesystem::path(CMAKE_SOURCE_DIR) / "data" / "examples" / "zeroing_2026-02-13_17-30-08.json");

	DataWriterV2 test(calibrations, zeroings);

	if (auto const res = test.connect(); !res.has_value()) return EXIT_FAILURE;

	for (auto i = 0; i < 1000000000; ++i) {
		if (auto serial_data = test.read_some(); serial_data.has_value()) {
			test.parse(serial_data.value());
		} else {
			test.close_serial_port();
			return EXIT_FAILURE;
		}
	}

	return EXIT_SUCCESS;
}