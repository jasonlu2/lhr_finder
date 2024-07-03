import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Dictionary of years and links
run_dict = {
    "2017" : "https://mychiptime.com/searchevent.php?id=1055"
}

# Dictionary of marathon categories and last digit of website link for 5k distance
fiveK_last_num = {
    "open" : "6",
    "undergrad" : "7",
    "grad" : "8",
    "faculty/staff" : "9"
}

# Dictionary of marathon categories and last digit of website link for 10k distance
tenK_last_num = {
    "open" : "2",
    "undergrad" : "3",
    "grad" : "4",
    "faculty/staff" : "5"
}

# Lists of times
female_times = []
male_times = []
female_converted_times = []
male_converted_times = []


# Function to convert time string to an int
def convert_time_to_int(time_str):
    # Remove colons and periods to convert to int
    return int(time_str.replace(":", "").replace(".", ""))

# Function to search for overall place
def binary_search(data, value):
    # Convert time from str to int
    value = convert_time_to_int(value)

    # Binary search for index
    data_len = len(data)
    left = 0
    right = data_len - 1

    while left <= right:
        mid = (left + right) // 2

        if value < data[mid]:
            right = mid - 1
        elif value > data[mid]:
            left = mid + 1
        else:
            return mid + 1

    return left + 1

def get_link(distance, category):

    # URL to access website
    link = "https://mychiptime.com/searchevent.php?id=1055"

    # Finish link
    if distance == "5k":
        return link + fiveK_last_num[category.lower()], ".d01:nth-child(8)"

    if distance == "10k":
        return link + tenK_last_num[category.lower()], ".d01:nth-child(14)"

    return -1


# Take tuple of (link, element tag)
def send_request(link_and_element):
    # Define headers with User-Agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }

    # Send HTTP GET request with headers and get response
    response = requests.get(link_and_element[0], headers=headers)

    # Parse HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all elements with the given HTML tag
    time_elements = soup.select(link_and_element[1])

    return time_elements

def convert_time(time_list):
    # Extract text from all selected elements
    times = [element.get_text(strip = True) for element in time_list]

    # Convert the time from a string to an integer
    converted_times = [(convert_time_to_int(time)) for time in times]

    return converted_times

def get_index(converted_times):
    male_start_index = 0
    # Female times
    for j in range(0, len(converted_times) - 1):
        if converted_times[j+1] < converted_times[j]:
            male_start_index = j+1
            break
        female_times.append(converted_times[j])

    # Male times
    for k in range(male_start_index, len(converted_times)):
        male_times.append(converted_times[k])


    # Return split index between genders
    return male_start_index


def find_place(gender, time, converted_times, index):
    # Filter times based on the selected gender
    if gender == "females":
        female_converted_times = converted_times[0:index]
        return binary_search(female_converted_times, time)

    if gender == "males":
        male_converted_times = converted_times[index:]
        return binary_search(male_converted_times, time)

    if gender == "both":
        all_converted_times = sorted(converted_times)
        return binary_search(all_converted_times, time)

    return -1


def plot_and_highlight_times(converted_times, time_ran, gender, index):
    # Convert the specific time ran to an integer
    time_ran_int = convert_time_to_int(time_ran)

    # Filter times based on the selected gender
    if gender == "females":
        times_to_plot = converted_times[:index]
    elif gender == "males":
        times_to_plot = converted_times[index:]
    else:
        times_to_plot = converted_times

    # Create a data frame for plotting
    df = pd.DataFrame(times_to_plot, columns=["Time"])

    # Plot boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df["Time"], color="lightblue")

    # Highlighting user's time ran
    plt.axvline(x=time_ran_int, color="red", linestyle="--", label=f"Time Ran: {time_ran}")

    # Add title and x-axis label
    plt.title("Distribution of Run Times with Highlighted Time")
    plt.xlabel("Times")
    plt.legend()

    # Display plot
    plt.show()


def main():
    # Inputs
    distance_chosen = input("Would you like to race in the 5K or 10K marathon: ")
    category_chosen = input("Would you like to race in the open, undergrad, grad, or faculty/staff category: ")
    gender_chosen = input("Would you like to race against females, males, or both: ")
    time_ran = input("What time did you run (only include 1 millisecond): ")

    # Run program
    link = get_link(distance_chosen, category_chosen)
    time_list = send_request(link)
    converted_list = convert_time(time_list)
    index = get_index(converted_list)
    place = find_place(gender_chosen, time_ran, converted_list, index)

    # Output calculated place
    print(f"You would have placed {place} with a time of {time_ran} in the marathon.")

    # Output boxplot of results
    plot_and_highlight_times(converted_list, time_ran, gender_chosen, index)


if __name__ == "__main__":
    main()
