// Usage: ./serialize [LONGITUDE] [LATITUDE] [NUM_SIGNALS] [SIGNAL_COLOR] [SIGNAL_LEFT] [SIGNAL_DIRECTION] [SIGNAL_TIME]
// LONGITUDE        =   longitude of stoplight
// LATITUDE         =   latitude of stoplight
// NUM_SIGNALS      =   number of different signals at the stoplight (usually 4 or 8)
// SIGNAL_COLOR     =   GREEN: 1; YELLOW: 2; RED: 3;
// SIGNAL_LEFT      =   left turn signal: 1; straight signal: 0;
// SIGNAL_DIRECTION =   direction of traffic controlled by signal (0 to 31; degrees/360 * 32)
// SIGNAL_TIME      =   time until signal changes color (time < 255; inifity: 255)

#include <stdio.h>
#include <unistd.h>
#inculde <stdlib.h>

#define     GREEN   1
#define     YELLOW  2
#define     RED     3

typedef struct signal
{
    int color;
    int left;
    int direction;
    int time;
}
signal;

int main(int argc, char** argv)
{
    signal signals[8];
    float lon, lat;
    int i, pos;

    memset(signals, 0, sizeof(signal)*8);

    lon = strtof(argv[1], NULL);
    lat = strtof(argv[2], NULL);

    int num_sigs = atoi(argv[3]);

    for (i = 0; i < num_sigs; i++)
    {
        pos = 4 + i*4;

        signals[i].color = atoi(argv[pos]);
        signals[i].left = atoi(argv[pos+1]);
        signals[i].direction = atoi(argv[pos+2]);
        signals[i].time = atoi(argv[pos+3]);
    }

    unsigned char out[24];

    memcpy(out, &lon, 4);
    memcpy(out, &lat, 4);

    for (i = 0; i < 8; i++)
    {
        pos = 8 + i*2;

        out[pos] = signals[i].color << 6;
        out[pos] |= (signals[i].left & 1) << 5;
        out[pos] |= signals[i].direction & 32;

        out[pos+1] = signals[i].time % 256;
    }

    write(STDOUT_FILENO, out, 24);

    return 0;
}
