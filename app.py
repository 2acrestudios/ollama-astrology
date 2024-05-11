import os
import csv
from tqdm import tqdm
from termcolor import colored
import re
import sys
import datetime
from branding_astrology import boxes, title, subtitle

import requests

ollama_api_base = "http://localhost:11434"
ollama_model = "llama3:8b"

current_date = datetime.date.today()

def choose_author_style():
    print("\nChoose an author style:")
    print("1. Default Style")
    print("2. Style of Popular Authors")
    choice = input("Enter your choice (1/2): ")
    return choice

def choose_popular_author():
    authors = [
        "William Shakespeare",
        "Mark Twain",
        "Douglas Adams",
        "Dr Seuss",
        "Oscar Wilde",
        "Franz Kafka",
        "Jane Austen",
        "Roald Dahl",
        "William S. Burroughs",
        "Allen Ginsberg",
        "Jack Kerouac",
        "William Blake",
    ]  
    print("\nChoose a popular author style:")
    for i, author in enumerate(authors, start=1):
        print(f"{i}. {author}")
    choice = input("Enter the number of your chosen author: ")
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(authors):
        print("Invalid choice. Please select a valid author.")
        return choose_popular_author()
    return authors[int(choice) - 1]

def print_colored_text(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

def get_horoscope(sign, author_style="Default"):
    prompt = (
        f"As {author_style}, a writer known for a unique literary style and expertise in both Modern and Whole Sign Astrology, "
        f"Rising sign: Your rising sign represents how you appear to others, your outward style, and how you approach new situations. It's the mask you wear in public and can influence your physical appearance and first impressions. The rising sign is also linked to your life path, personal interests, and the kind of experiences you're drawn to. "
        f"Sun Sign: Your Sun sign symbolizes your core being, your identity, and your sense of self. It reflects your primary drive in life and your overall approach to life's challenges. The Sun sign is often associated with your life's purpose and the expression of your creative energy. It's the essence of who you are. "
        f"Moon Sign: The Moon sign is tied to your inner world and represents your emotional landscape, instincts, and intuitive responses. It's about how you process emotions and your inherent reactions to things. Your Moon sign can also indicate the type of nurturing and care you seek, as well as your instinctual habits and unconscious patterns. "
        f"create a daily horoscope for {name}, using {current_date} for astrological calculations. "
        f"Your analysis should primarily focus on the influence of {name}'s Rising sign, {sign}, "
        f"considering today's planetary alignments and transits, while subtly incorporating the aspects of their Sun sign, {sun_sign}, and Moon sign, {moon_sign}, without mentioning their Sun sign, {sun_sign}, and Moon sign in the reading. "
        f"The horoscope should reflect your distinctive prose or poetry style, include a witty title that does not directly reference any zodiac signs, "
        f"and offer detailed, specific guidance, gently addressing any challenging aspects. "
        f"Conclude with an inspirational quote that complements the day's horoscope. "
        f"Ensure your writing captures the essence of {author_style}'s style, focusing on today's relevant experiences and emotions, "
        f"and avoid repeating content or generalizing zodiac traits or making the readin about their Sun sign and Moon sign. "
    )
    response = requests.post(
        f"{ollama_api_base}/api/generate",
        json={"model": ollama_model, "prompt": prompt, "stream": False},
    )

    if response.status_code == 200:
        return response.json()["response"]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return ""

def print_title():
    os.system("clear")
    print_colored_text(boxes, "0;34;40")
    print_colored_text(title, "0;36;40")
    print_colored_text(subtitle, "0;33;40")

print_title()

def generate_horoscope(
    name,
    rising_sign,
    sun_sign,
    moon_sign,
    interest_area,
    overwrite=False,
    author_style="Default",
):
    file_name = (
        f"data/horoscope_daily_{name}_{rising_sign}_{sun_sign}_{moon_sign}.txt"
    )
    if not overwrite and os.path.exists(file_name):
        try:
            with open(file_name, "r") as f:
                # Read and return the existing horoscope text
                return f.read().split(
                    "\n\n", 1
                )[1]  # Splits title and horoscope, returns just the horoscope
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
    # Generate a new horoscope

    horoscope = get_horoscope(rising_sign, author_style)
    # Write the new horoscope to a file
    colored_title = colored(
        f"{name}'s Daily reading for {rising_sign} rising, {sun_sign} sun, {moon_sign} moon person!",
        "cyan",
    )
    colored_title_without_s = colored_title.replace("'s", "")
    colored_title_without_escape_codes = re.sub(
        r"\033\[[0-9;]+m", "", colored_title_without_s
    )
    with open(file_name, "w") as f:
        f.write(colored_title_without_escape_codes + "\n\n" + horoscope)
    return horoscope

def choose_sign(prompt, signs):
    sys.stdout.write("\033c")
    print_title()
    print("Please choose from the following signs:")
    for i, sign in enumerate(signs):
        print(f"{i + 1}: {sign}")
    choice = int(input(f"{prompt}: ")) - 1
    if choice < 0 or choice >= len(signs):
        raise ValueError("Invalid choice.")
    return signs[choice]

def load_from_csv(file_path):
    horoscopes = []
    with open(file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row["Name"]
            rising_sign = row["Rising Sign"]
            sun_sign = row["Sun Sign"]
            moon_sign = row["Moon Sign"]
            interest_area = row["Interest Area"]
            horoscopes.append((name, rising_sign, sun_sign, moon_sign, interest_area))
    return horoscopes

def generate_horoscope_for_two_people(
    person1_name,
    person1_rising_sign,
    person1_sun_sign,
    person1_moon_sign,
    person2_name,
    person2_rising_sign,
    person2_sun_sign,
    person2_moon_sign,
    interest_area,
    author_style,
    overwrite=False,
):
    """Generates a horoscope for two people."""
    file_name = f"data/horoscope_daily_{person1_name}_{person2_name}.txt"
    # Check if the file exists and whether to overwrite it
    if not overwrite and os.path.exists(file_name):
        try:
            with open(file_name, "r") as f:
                # Read and return the existing horoscope text
                return f.read().split(
                    "\n\n", 1
                )[1]  # Splits title and horoscope, returns just the horoscope
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
    prompt = (
        f"Create a daily horoscope as if it were written by {author_style}, that combines the energy of {person1_name}'s {person1_rising_sign} rising, "
        f"{person1_sun_sign} sun, and {person1_moon_sign} moon signs with "
        f"{person2_name}'s {person2_rising_sign} rising, {person2_sun_sign} sun, "
        f"and {person2_moon_sign} moon signs, focus on their synergy in {interest_area}. "
        f"Reflect on today's unique astrological aspects and how they might influence their joint endeavors. "
        f"Highlight potential emotional dynamics and experiences specific to today, "
        f"tailoring insights to their combined energies. Avoid repeating general sign traits. "
        f"End with an uplifting quote related to today's theme."
        f"Stay true to the writing style of {author_style}. "
    )
    completion = requests.post(
        f"{ollama_api_base}/api/generate",
        json={"model": ollama_model, "prompt": prompt, "stream": False},
    )
    if completion.status_code == 200:
        horoscope = completion.json()["response"]
        # Write the horoscope to a file
        colored_title = colored(
            f"{person1_name} and {person2_name}'s Daily reading", "cyan"
        )
        colored_title_without_s = colored_title.replace("'s", "")
        colored_title_without_escape_codes = re.sub(
            r"\033\[[0-9;]+m", "", colored_title_without_s
        )
        with open(file_name, "w") as f:
            f.write(colored_title_without_escape_codes + "\n\n" + horoscope)
        return horoscope
    else:
        print(f"Error: {completion.status_code} - {completion.text}")
        return None

operation = input(
    "Choose Your Path:\n1. Generate horoscopes for all combinations of rising, Sun, and Moon signs - 1728 records\n2. Horoscope for one person with famous authors mode!\n3. Create multiple horoscopes from a CSV file\n4. Horoscope for two People\n"
).lower()
if operation == "1":
    signs = [
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces",
    ]
    combinations = [
        (name, rising, sun, moon)
        for name in [""]
        for rising in signs
        for sun in signs
        for moon in signs
    ]
    overwrite = False
    pbar = tqdm(total=len(combinations))
    with open("data/horoscopes_daily.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Rising Sign", "Sun Sign", "Moon Sign", "Horoscope"])
        for name, rising_sign, sun_sign, moon_sign in combinations:
            result = generate_horoscope(
                name, rising_sign, sun_sign, moon_sign, "General", overwrite
            )  # Adjust 'General' as needed
            if result:
                writer.writerow([name, rising_sign, sun_sign, moon_sign, result])
            pbar.update(1)
    pbar.close()
    print(f"{len(combinations)} horoscopes have been written to horoscopes_daily.csv.")
if operation == "2":
    overwrite = True
    signs = [
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces",
    ]
    name = input("What is your name? ")
    interest_area = input("Enter the area of interest: ")
    rising_sign = choose_sign("What is your rising sign?", signs)
    sun_sign = choose_sign("What is your Sun sign?", signs)
    moon_sign = choose_sign("What is your Moon sign?", signs)

    author_style_choice = choose_author_style()
    if author_style_choice == "2":
        author_style_choice = choose_popular_author()
    result = generate_horoscope(
        name,
        rising_sign,
        sun_sign,
        moon_sign,
        interest_area,
        overwrite,
        author_style_choice,
    )
    print(result)
elif operation == "3":
    print_title()
    # Prompt for file path with default option
    csv_path = input(
        "Enter the path to the CSV file (press enter to use 'horoscopes_input.csv'): "
    )
    if not csv_path:
        csv_path = "horoscopes_input.csv"  # Default file path
    overwrite = True
    horoscopes = load_from_csv(csv_path)
    pbar = tqdm(total=len(horoscopes))
    for horoscope_data in horoscopes:
        name, rising_sign, sun_sign, moon_sign, interest_area = horoscope_data
        horoscope = generate_horoscope(
            name, rising_sign, sun_sign, moon_sign, interest_area, overwrite
        )
        if horoscope:
            with open(
                f"data/horoscope_daily_{name}_{rising_sign}_{sun_sign}_{moon_sign}.txt",
                "w",
            ) as f:
                title = (
                    f"{name}'s Daily reading for {rising_sign} rising, {sun_sign} sun, {moon_sign} moon person!"
                )
                f.write(horoscope)
        pbar.update(1)
    pbar.close()
    print(colored(f"{len(horoscopes)} horoscopes have been processed.", "green"))
elif operation == "4":
    signs = [
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces",
    ]
    person1_name = input("What is the first person's name? ")
    person1_rising_sign = choose_sign("What is the first person's rising sign?", signs)
    person1_sun_sign = choose_sign("What is the first person's Sun sign?", signs)
    person1_moon_sign = choose_sign("What is the first person's Moon sign?", signs)
    person2_name = input("What is the second person's name? ")
    person2_rising_sign = choose_sign("What is the second person's rising sign?", signs)
    person2_sun_sign = choose_sign("What is the second person's Sun sign?", signs)
    person2_moon_sign = choose_sign("What is the second person's Moon sign?", signs)
    interest_area = input("Enter the area of interest: ")

    author_style_choice = choose_author_style()
    if author_style_choice == "2":
        author_style_choice = choose_popular_author()
    horoscope_for_two_people = generate_horoscope_for_two_people(
        person1_name,
        person1_rising_sign,
        person1_sun_sign,
        person1_moon_sign,
        person2_name,
        person2_rising_sign,
        person2_sun_sign,
        person2_moon_sign,
        interest_area,
        author_style_choice,  
        overwrite=True,  # Set overwrite to True if you want to overwrite existing files
    )
    print(horoscope_for_two_people)
else:
    print(colored("Invalid choice. Please choose either '1', '2', '3', or '4'.", "red"))
