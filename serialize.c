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
#include <stdlib.h>
#include <string.h>

#define     GREEN   1
#define     YELLOW  2
#define     RED     3

typedef struct signal
{
    int valid;
    int color;
    int left;
    int direction;
    int time;
}
signal;

void serialize(char**);
void deserialize(void);

int main(int argc, char** argv)
{
    if (argc == 1)
        deserialize();
    else
        serialize(argv);

    return 0;
}

void deserialize()
{
    signal signals[8];
    float lon, lat;
    int i, pos, num_signals;
    unsigned char in[24];
    
    memset(signals, 0, sizeof(signal)*8);

    read(STDIN_FILENO, in, 24);

    memcpy(&lon, in, 4);
    memcpy(&lat, in+4, 4);

    num_signals = 0;
    for (i = 0; i < 8; i++)
    {
        pos = 8 + i*2;

        if (!(in[pos] & 0xc0))
            continue;

        num_signals++;
        signals[i].valid = 1;
        signals[i].color = (in[pos] >> 6) & 3;
        signals[i].left = (in[pos] >> 5) & 1;
        signals[i].direction = in[pos] & 31;
        signals[i].time = in[pos+1];
    }

    printf("%f %f %d", lon, lat, num_signals);

    for (i = 0; i < 8; i++)
    {
        if (!signals[i].valid)
            continue;

        printf(" %d %d %d %d", signals[i].color, signals[i].left, signals[i].direction, signals[i].time);
    }

    printf("\n");
}

void serialize(char** argv)
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

        signals[i].valid = 1;
        signals[i].color = atoi(argv[pos]);
        signals[i].left = atoi(argv[pos+1]);
        signals[i].direction = atoi(argv[pos+2]);
        signals[i].time = atoi(argv[pos+3]);
    }

    unsigned char out[24];
    memset(out, 0, 24);

    memcpy(out, &lon, 4);
    memcpy(out+4, &lat, 4);

    for (i = 0; i < 8; i++)
    {
        if (!signals[i].valid)
            continue;

        pos = 8 + i*2;

        out[pos] = signals[i].color << 6;
        out[pos] |= (signals[i].left & 1) << 5;
        out[pos] |= signals[i].direction & 31;

        out[pos+1] = signals[i].time % 256;
    }

    write(STDOUT_FILENO, out, 24);
}
