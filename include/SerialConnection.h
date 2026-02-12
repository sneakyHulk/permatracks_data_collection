#pragma once

#ifdef SERIALCONNECTION_USE_BOOST
#include <boost/asio.hpp>
#else
#include <fcntl.h>
#include <poll.h>
#include <termios.h>
#include <unistd.h>

#include <cerrno>
#endif

#include <common_error.h>

#include <atomic>
#include <cstdint>
#include <expected>
#include <iostream>
#include <span>
#include <thread>

enum Baudrate : unsigned int {
	BAUD9600 = 9600,
	BAUD19200 = 19200,
	BAUD38400 = 38400,
	BAUD57600 = 57600,
	BAUD115200 = 115200,
	BAUD230400 = 230400,
	BAUD460800 = 460800,
	BAUD921600 = 921600,
};

struct MessagePart {
	std::uint64_t timestamp;
	std::span<const char> data;
};

class SerialConnection {
	enum class ConnectionState {
		NONE,
		CONNECTED,
		// READING,
	};
	std::atomic<ConnectionState> state = ConnectionState::NONE;

	std::thread connection_thread;

#ifdef SERIALCONNECTION_USE_BOOST
	boost::asio::io_context _context;
	boost::asio::serial_port _serial_port;
#else
	int _serial_port = -1;
#endif

   protected:
	Baudrate baud = Baudrate::BAUD230400;

   public:
#ifdef SERIALCONNECTION_USE_BOOST
	SerialConnection() : _serial_port(_context) { std::cout << "Connection()" << std::endl; }
#else
	SerialConnection() { std::cout << "Connection()" << std::endl; }
#endif

	std::expected<void, common::Error> open_serial_port(std::string const& device);
	void close_serial_port();

	std::expected<void, common::Error> write_all(std::span<std::uint8_t const> const buffer);
	std::expected<MessagePart, common::Error> read_some();

   protected:
	~SerialConnection();

	bool connected() const;
};