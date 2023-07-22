import threading
import time
import winsound

NUM_DRIVERS = 20


def beep_thread():
    # Function to play a beep sound with frequency 1500 Hz for 70 milliseconds
    winsound.Beep(1500, 70)


def beep_with_interval(driver_name, interval):
    # Function to print a message with driver's completion time and play the beep sound asynchronously
    if interval > 0:
        print(
            f"Driver {driver_name} has completed his lap within {interval} milliseconds.")
    else:
        print(f"Driver {driver_name} has finished the race first.")
    # Create a new thread to play the beep sound asynchronously
    thread = threading.Thread(target=beep_thread)
    thread.start()


def main():
    drivers = [
        # List of drivers with their names and lap completion intervals in milliseconds
        ("Lewis HAMILTON", 0),
        ("Max VERSTAPPEN", 3),
        ("Lando NORRIS", 82),
        ("Oscar PIASTRI", 211),
        ("Guanyu ZHOU", 66),
        ("Charles LECLERC", 21),
        ("Valtteri BOTTAS", 42),
        ("Fernando ALONSO", 1),
        ("Sergio PÉREZ", 10),
        ("Nico HULKENBERG", 141),
        ("Carlos SAINZ", 517),
        ("Esteban OCON", 138),
        ("Daniel RICCIARDO", 163),
        ("Lance STROLL", 140),
        ("Pierre GASLY", 73),
        ("Alexander ALBON", 700),
        ("Yuki TSUNODA", 2),
        ("George RUSSELL", 108),
        ("Kevin MAGNUSSEN", 179),
        ("Logan SARGEANT", 42),
    ]  # Add your desired driver names and intervals in milliseconds to this dictionary

    print("Welcome to the beep program!")
    print("Beeps will start automatically...\n")

    start_time = time.perf_counter()

    total_interval_time_ms = 0

    # Use a thread pool to manage a limited number of threads efficiently (e.g., 5 threads)
    pool = [5]

    # Simulate the race for each driver
    for i, (name, interval) in enumerate(drivers):
        if i > 0:
            time_to_wait = interval / 1000.0
            start = time.perf_counter()

            # Busy-wait to create a more precise delay before starting the beep sound thread
            while time.perf_counter() - start < time_to_wait:
                pass

         # Create a thread for each driver to play the beep sound with interval
        thread = threading.Thread(
            target=beep_with_interval, args=(name, interval))
        thread.start()
        pool.append(thread)
        total_interval_time_ms += interval  # Accumulate the total interval time

    # Wait for all threads in the pool to finish
    for thread in pool:
        thread.join()

    end_time = time.perf_counter()

    execution_time = end_time - start_time

    # Display race and execution results
    print("\nTotal interval time: {} milliseconds".format(total_interval_time_ms))
    print("Total execution time: {:.3f} seconds".format(execution_time))


if __name__ == "__main__":
    main()
