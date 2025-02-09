

#include <iostream>
#include <vector>

// Function to calculate Internet Checksum
uint16_t calculateChecksum(const std::vector<uint8_t>& data) {
    uint32_t checksum = 0;

    // Process 16-bit chunks
    for (size_t i = 0; i < data.size(); i += 2) {
        // Combine two bytes to form a 16-bit word
        uint16_t word = data[i] << 8;
        if (i + 1 < data.size()) {
            word += data[i + 1];
        }
        checksum += word;

        // Wrap around if overflow occurs
        checksum = (checksum & 0xFFFF) + (checksum >> 16);
    }

    // Final wrap-around for any remaining carry
    checksum = ~checksum & 0xFFFF;
    return static_cast<uint16_t>(checksum);
}

// Function to verify checksum
bool verifyChecksum(const std::vector<uint8_t>& data, uint16_t receivedChecksum) {
    uint16_t calculatedChecksum = calculateChecksum(data);
    // Sum with received checksum should be all 1s (0xFFFF) if correct
    return ((calculatedChecksum + receivedChecksum) & 0xFFFF) == 0xFFFF;
}

int main() {
    // Data to be sent
    std::vector<uint8_t> data = {'H', 'e', 'l', 'l', 'o', ',', ' ', 'W', 'o', 'r', 'l', 'd', '!'};
    
    // Calculating checksum
    uint16_t checksum = calculateChecksum(data);
    std::cout << "Calculated Checksum: 0x" << std::hex << checksum << std::dec << std::endl;

    // Verify with the calculated checksum
    bool is_valid = verifyChecksum(data, checksum);
    std::cout << "Is the received data valid? " << (is_valid ? "Yes" : "No") << std::endl;

    // Example with error introduction
    std::vector<uint8_t> corrupted_data = {'H', 'o', 'l', 'l', 'o', ',', ' ', 'W', 'o', 'r', 'l', 'd', '!'};
    is_valid = verifyChecksum(corrupted_data, checksum);
    std::cout << "Is the received data valid after introducing an error? " << (is_valid ? "Yes" : "No") << std::endl;

    return 0;
}