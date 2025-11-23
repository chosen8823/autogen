/**
 * Resonance Bus Implementation
 * Sophiael Platform v1.0
 */

#include "resonance_bus.hpp"
#include <algorithm>
#include <iostream>

namespace sophiael {

ResonanceBus::ResonanceBus()
    : m_message_count(0)
    , m_total_resonance(0.0)
    , m_initialized(false)
{
}

ResonanceBus::~ResonanceBus() {
    shutdown();
}

void ResonanceBus::initialize() {
    std::lock_guard<std::mutex> lock(m_mutex);

    if (m_initialized) {
        return;
    }

    m_message_count = 0;
    m_total_resonance = 0.0;
    m_subscriptions.clear();
    m_initialized = true;
}

void ResonanceBus::shutdown() {
    std::lock_guard<std::mutex> lock(m_mutex);

    if (!m_initialized) {
        return;
    }

    m_subscriptions.clear();
    m_initialized = false;
}

void ResonanceBus::subscribe(const std::string& channel,
                             const std::string& subscriber,
                             MessageHandler handler) {
    std::lock_guard<std::mutex> lock(m_mutex);

    Subscription sub;
    sub.subscriber_name = subscriber;
    sub.handler = handler;

    m_subscriptions[channel].push_back(sub);
}

void ResonanceBus::unsubscribe(const std::string& channel,
                               const std::string& subscriber) {
    std::lock_guard<std::mutex> lock(m_mutex);

    auto it = m_subscriptions.find(channel);
    if (it == m_subscriptions.end()) {
        return;
    }

    auto& subs = it->second;
    subs.erase(
        std::remove_if(subs.begin(), subs.end(),
            [&subscriber](const Subscription& sub) {
                return sub.subscriber_name == subscriber;
            }),
        subs.end()
    );
}

void ResonanceBus::publish(const std::string& channel,
                          const std::string& sender,
                          const std::string& payload,
                          double resonance_frequency) {
    ResonanceMessage message;
    message.channel = channel;
    message.sender = sender;
    message.payload = payload;
    message.resonance_frequency = resonance_frequency;
    message.timestamp_us = get_timestamp_us();

    // Update statistics
    {
        std::lock_guard<std::mutex> lock(m_mutex);
        m_message_count++;
        m_total_resonance += resonance_frequency;
    }

    // Dispatch to subscribers (outside lock to avoid deadlock)
    dispatch_message(message);
}

double ResonanceBus::get_average_resonance() const {
    std::lock_guard<std::mutex> lock(m_mutex);

    if (m_message_count == 0) {
        return 432.0; // Default base frequency
    }

    return m_total_resonance / static_cast<double>(m_message_count);
}

size_t ResonanceBus::get_message_count() const {
    std::lock_guard<std::mutex> lock(m_mutex);
    return m_message_count;
}

std::vector<std::string> ResonanceBus::get_active_channels() const {
    std::lock_guard<std::mutex> lock(m_mutex);

    std::vector<std::string> channels;
    for (const auto& pair : m_subscriptions) {
        if (!pair.second.empty()) {
            channels.push_back(pair.first);
        }
    }

    return channels;
}

size_t ResonanceBus::get_subscriber_count(const std::string& channel) const {
    std::lock_guard<std::mutex> lock(m_mutex);

    auto it = m_subscriptions.find(channel);
    if (it == m_subscriptions.end()) {
        return 0;
    }

    return it->second.size();
}

void ResonanceBus::reset() {
    std::lock_guard<std::mutex> lock(m_mutex);

    m_message_count = 0;
    m_total_resonance = 0.0;
}

int64_t ResonanceBus::get_timestamp_us() const {
    auto now = std::chrono::high_resolution_clock::now();
    auto duration = now.time_since_epoch();
    return std::chrono::duration_cast<std::chrono::microseconds>(duration).count();
}

void ResonanceBus::dispatch_message(const ResonanceMessage& message) {
    // Copy subscribers to avoid holding lock during callback
    std::vector<Subscription> subscribers_copy;
    {
        std::lock_guard<std::mutex> lock(m_mutex);
        auto it = m_subscriptions.find(message.channel);
        if (it != m_subscriptions.end()) {
            subscribers_copy = it->second;
        }
    }

    // Call handlers outside lock
    for (const auto& sub : subscribers_copy) {
        try {
            if (sub.handler) {
                sub.handler(message);
            }
        } catch (const std::exception& e) {
            std::cerr << "Error in message handler for "
                     << sub.subscriber_name << ": " << e.what() << std::endl;
        }
    }
}

// Global singleton
ResonanceBus& get_global_resonance_bus() {
    static ResonanceBus instance;
    if (!instance.m_initialized) {
        instance.initialize();
    }
    return instance;
}

} // namespace sophiael
