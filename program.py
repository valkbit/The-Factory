from colorama import Fore
import random
import os
from pathlib import Path
from google import genai

# Generate SCP file and return it for later display.
def generate_scp(context: str, client):

    scp_file = {
        "id": f"SCP-{random.randint(9000, 9999)}",
        "class": None,
        "procedures": None,
        "description": None,
        "log": None
    }

    # Generate a description for the SCP
    def generate_description():
        prompt = f"""Based on the SCP Foundation documentation provided, generate a detailed description for a new SCP anomaly.

        {context}

        Generate ONLY the description section content (do not include "Description:" header). Keep it between 150-400 words."""

        try:
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error generating description: {e}")
            return "A standard anomalous object requiring further research."
    
    # Generate containment procedures for the SCP based off the description
    def generate_containment_procedures():
        prompt = f"""Based on the SCP Foundation documentation and the following anomaly description, generate specific Special Containment Procedures:

        {context}

        ANOMALY DESCRIPTION:
        {scp_file["description"]}

        Generate ONLY the containment procedures content (do not include "Special Containment Procedures:" header). Keep it between 100-300 words."""

        try:
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error generating containment procedures: {e}")
            return "Standard containment protocols are to be followed."

    # Generate the object class based off containment procedures and object description.
    def generate_object_class():
        prompt = f"""Based on the SCP Foundation documentation and the following anomaly information, determine the appropriate Object Class:

        {context}

        CONTAINMENT PROCEDURES: {scp_file["procedures"]}
        DESCRIPTION: {scp_file["description"]}

        Respond with ONLY the Object Class name (e.g., "Safe", "Euclid", "Keter", etc.)."""

        try:
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt
            )
            class_name = response.text.strip()
            # Validate the response
            #valid_classes = ["Safe", "Euclid", "Keter", "Thaumiel", "Apollyon", "Archon", "Neutralized", "Explained"]
            #if class_name in valid_classes:
            #    return class_name
            #else:
            #    return "Euclid"
            return class_name
        except Exception as e:
            print(f"Error generating object class: {e}")
            return "Euclid"

    # Generate an event log based off the stored information in scp_file.
    def generate_event_log(obj_class: str, containment_procedures: str, description: str):
        # Determine log type based on description content
        description_lower = description.lower()
        
        if any(keyword in description_lower for keyword in ['location', 'area', 'room', 'building', 'zone']):
            log_type = "Exploration Log"
        elif any(keyword in description_lower for keyword in ['humanoid', 'entity', 'sentient', 'sapient', 'intelligence', 'intelligent', 'creature']):
            log_type = random.choice(["Interview Log", "Breach Report"])
        else:
            log_type = random.choice(["Test Log", "Discovery Log", "Event Log"])

        prompt = f"""Based on the SCP Foundation documentation and the following anomaly information, generate a {log_type}:

        {context}

        OBJECT CLASS: {obj_class}
        CONTAINMENT PROCEDURES: {containment_procedures}
        DESCRIPTION: {description}

        Generate a complete {log_type} that is 200-600 words long and includes proper log headers and structure."""

        try:
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error generating event log: {e}")
            return None

    # Generate each section
    print("Generating SCP description...")
    scp_file["description"] = generate_description()
    
    print("Generating containment procedures...")
    scp_file["procedures"] = generate_containment_procedures()
    
    print("Determining object class...")
    scp_file["class"] = generate_object_class()

    # Random chance to generate an event log.
    if random.random() < 0.4:
        print("Generating event log...")
        scp_file["log"] = generate_event_log(scp_file["class"], scp_file["procedures"], scp_file["description"])

    return scp_file

def save_file(scp_file, results_dir: Path) -> None:
    """Save the generated SCP to a text file"""
    if not results_dir.exists():
        results_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{scp_file["id"]}.txt"
    filepath = results_dir / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"Item #: {scp_file['id']}\n\n")
        f.write(f"Object Class: {scp_file['class']}\n\n")
        f.write(f"Special Containment Procedures: {scp_file['procedures']}\n\n")
        f.write(f"Description: {scp_file['description']}\n\n")
        
        if scp_file["log"]:
            f.write(f"{scp_file['log']}\n")

    print(f"\n{Fore.GREEN}Saved {scp_file["id"]} to {filepath}.")

# Function to display scp file contents after generation.
def display_file(scp_file):
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"{Fore.RED}Item #: {scp_file['id']}\n")
    print(f"{Fore.MAGENTA}Object Class: {scp_file['class']}\n")
    print(f"{Fore.YELLOW}Special Containment Procedures: {scp_file['procedures']}\n")
    print(f"{Fore.CYAN}Description: {scp_file['description']}\n")

    if scp_file["log"]:
        print(f"{Fore.GREEN}Event Log: {scp_file['log']}")

    print(Fore.RESET)

def main() -> None:
    # Get folder paths
    base_dir = Path(__file__).parent
    result_dir = base_dir / "results" # We will save the generated files here.
    rules_dir = base_dir / "rules"
    examples_dir = rules_dir / "examples"

    # Read API key from config.txt
    config_path = base_dir / "config.txt"
    API_KEY = None
    with open(config_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GOOGLE_API_KEY="):
                API_KEY = line.strip().split("=", 1)[1]
                break

    if not API_KEY or "your_api_key" in API_KEY:
        raise ValueError("API key not found in config.txt")

    # Set the API key variable
    client = genai.Client(api_key=API_KEY)

    # Group and collect all text files
    file_paths = list(rules_dir.glob("*.txt")) + list(examples_dir.glob("*.txt"))
    file_contents = []
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as f:
            file_contents.append(f.read())

    # Combine all files into one string
    combined_text = "\n\n".join(file_contents)

    # Generate an SCP file based off the context given by the text documents.
    scp = generate_scp(combined_text, client)
    display_file(scp)

    should_save = input("Do you want to save this file to the results folder? (y/n): ")
    if "y" in str.lower(should_save):
        save_file(scp_file=scp, results_dir=result_dir)

if __name__ == "__main__":
    main()