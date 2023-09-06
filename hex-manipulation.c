#include <stdio.h>
#include <stdint.h>

int main()
{
    uint8_t raw_data[] = {
	    0x73, 0x6E, 0x70, 0xE4, 0x70, 0xFF, 0xAB, 0x00, 0xB4, 0x0F, 0x8A, 0x00,
	    0x00, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00, 0x43, 0x80, 0x1C,
	    0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x00,
	    0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x45
    };

    /* uint8_t raw_data[] = { */
	    /* 0x73, 0x6E, 0x70, 0x80, 0x55, 0x00, 0x00, 0x00, 0x01, 0x02, 0x27 */
    /* }; */

    uint8_t PT = raw_data[3];
    uint8_t address = raw_data[4];

    uint8_t packet_has_data = (PT >> 7) & 0x01;
    uint8_t packet_is_batch = (PT >> 6) & 0x01;
    uint8_t batch_length = (PT >> 2) & 0x0F;

    uint8_t data_length = 4;
    if (packet_has_data && packet_is_batch)
        data_length *= batch_length;

    printf("has_data: %d; is_batch: %d; batch_len: %d\n", packet_has_data, packet_is_batch, batch_length);
    printf("data_len: %d\n", data_length);

    uint16_t computed_checksum = 's' + 'n' + 'p' + PT + address;
    for (int i = 0; i < data_length; i++)
    {
        computed_checksum += raw_data[i+5];
    }
    printf("computed_checksum: %d\n", computed_checksum);
    uint16_t received_checksum = (raw_data[5 + data_length] << 8);
    received_checksum |= raw_data[6 + data_length];
    printf("received_checksum: %d\n", received_checksum);
}

