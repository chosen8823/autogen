/**
 * Resonance Bus - Fast C++ Communication Channel
 * Sophiael Platform v1.0
 *
 * Central pub/sub communication bus for all layers.
 * Provides high-speed messaging between C++, Python, and other components.
 */

#pragma once

#include <string>
#include <vector>
#include <map>
#include <functional>
#include <mutex>
#include <memory>
#include <queue>
#include <chrono>

namespace sophiael {

/**
 * Message structure for the resonance bus
 */
struct ResonanceMessage {
    std::string channel;           // Channel name (e.g., "instinct", "bio", "semantic")
    std::string sender;            // Who sent it
    std::string payload;           // Message content (JSON string)
    double resonance_frequency;    // Hz - alignment frequency
    int64_t timestamp_us;          // Microsecond timestamp

    ResonanceMessage()
        : resonance_frequency(432.0)
        , timestamp_us(0) {}
};

/**
 * Message handler callback type
 */
using MessageHandler = std::function<void(const ResonanceMessage&)>;

/**
 * Resonance Bus - Central communication hub
 *
 * Features:
 * - Multi-channel pub/sub
 * - Lock-free message passing (where possible)
 * - Microsecond timestamps
 * - Resonance tracking (frequency alignment)
 * - Thread-safe operations
 */
class ResonanceBus {
public:
    ResonanceBus();
    ~ResonanceBus();

    // Initialize the bus
    void initialize();
    void shutdown();

    // Subscribe to a channel
    void subscribe(const std::string& channel, const std::string& subscriber, MessageHandler handler);

    // Unsubscribe from a channel
    void unsubscribe(const std::string& channel, const std::string& subscriber);

    // Publish a message to a channel
    void publish(const std::string& channel,
                 const std::string& sender,
                 const std::string& payload,
                 double resonance_frequency = 432.0);

    // Get resonance statistics
    double get_average_resonance() const;
    size_t get_message_count() const;

    // Get channel statistics
    std::vector<std::string> get_active_channels() const;
    size_t get_subscriber_count(const std::string& channel) const;

    // Clear all messages and reset
    void reset();

private:
    struct Subscription {
        std::string subscriber_name;
        MessageHandler handler;
    };

    std::map<std::string, std::vector<Subscription>> m_subscriptions;
    std::mutex m_mutex;

    // Statistics
    size_t m_message_count;
    double m_total_resonance;

    bool m_initialized;

    // Get current timestamp in microseconds
    int64_t get_timestamp_us() const;

    // Dispatch message to subscribers
    void dispatch_message(const ResonanceMessage& message);
};

/**
 * Singleton accessor for global resonance bus
 */
ResonanceBus& get_global_resonance_bus();

} // namespace sophiael
