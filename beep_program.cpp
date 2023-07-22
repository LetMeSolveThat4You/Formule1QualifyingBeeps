#include <stdio.h>
#include <windows.h>

#define NUM_DRIVERS 20 // Adjust this value based on the actual number of drivers

// Function to play the beep sound asynchronously in a separate thread
DWORD WINAPI beep_thread(LPVOID  lpParameter) {
    Beep(1500, 70); // Play a beep sound with frequency 1500 Hz for 70 milliseconds
    return 0;
}

void beep_with_interval(const char* driver_name, int interval) {
    if (interval > 0) {
        printf("Driver %s has completed his lap within %d milliseconds.\n", driver_name, interval);
    } else {
        printf("Driver %s has finished P1.\n", driver_name);
    }
    DWORD thread_id;
    // Create a new thread to play the beep sound asynchronously
    HANDLE hThread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)beep_thread, &interval, 0, &thread_id);
    if (hThread) {
        CloseHandle(hThread); // Close the thread handle to release resources
    }
}

int main() {

    // Structure to store the name and interval of each driver
    struct DriverInterval {
        const char* name;
        int interval;
    };

    // List of drivers and their respective race intervals (in milliseconds)
    struct DriverInterval drivers[] = {
        {"Lewis HAMILTON", 0},
        {"Max VERSTAPPEN", 3},
        {"Lando NORRIS", 82},
        {"Oscar PIASTRI", 211},
        {"Guanyu ZHOU", 66},
        {"Charles LECLERC", 21},
        {"Valtteri BOTTAS", 42},
        {"Fernando ALONSO", 1},
        {"Sergio PÉREZ", 10},
        {"Nico HULKENBERG", 141},
        {"Carlos SAINZ", 517},
        {"Esteban OCON", 138},
        {"Daniel RICCIARDO", 163},
        {"Lance STROLL", 140},
        {"Pierre GASLY", 73},
        {"Alexander ALBON", 700},
        {"Yuki TSUNODA", 2},
        {"George RUSSELL", 108},
        {"Kevin MAGNUSSEN", 179},
        {"Logan SARGEANT", 42},
    };

    LARGE_INTEGER frequency;
    if (!QueryPerformanceFrequency(&frequency)) {
        printf("Error: QueryPerformanceFrequency not supported.\n");
        return 1;
    }

    printf("Welcome to the beep program!\n");
    printf("Beeps will start automatically...\n");

    LARGE_INTEGER start_time, end_time;
    QueryPerformanceCounter(&start_time);

    DWORD total_interval_time_ms = 0;

    // Simulate the race for each driver
    for (int i = 0; i < NUM_DRIVERS; i++) {
        if (i > 0) {
            Sleep(drivers[i].interval); // Introduce a delay before beeping based on the interval
        }
        beep_with_interval(drivers[i].name, drivers[i].interval); // Beep and print the status of the driver
        total_interval_time_ms += drivers[i].interval; // Accumulate the total interval time
    }

    QueryPerformanceCounter(&end_time);

    double execution_time = (double)(end_time.QuadPart - start_time.QuadPart) / frequency.QuadPart;

    printf("\nTotal interval time: %d milliseconds\n", total_interval_time_ms);
    printf("Total execution time: %.3f seconds\n", execution_time);

    return 0;
}
