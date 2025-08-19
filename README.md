# The Factory SCP Generator (AI-Powered)

This project generates unique SCP entries (anomalous objects, entities, and phenomena) using Google's **Gemini 1.5 Flash** model.  
It takes inspiration from existing SCP files and rules, then creates new SCPs complete with descriptions, containment procedures, classifications, and sometimes event logs.

---

## 📂 Project Structure

```
RootFolder
│── results/                     # Generated SCPs will be saved here
│── rules/                       # Context rules for generation
│   ├── examples/                # Example SCPs to guide generation
│   │   ├── 005.txt
│   │   ├── 008.txt
│   │   ├── 096.txt
│   │   ├── 173.txt
│   │   ├── 2935.txt
│   │   ├── 3000.txt
│   │   ├── 3008.txt
│   │   ├── 3930.txt
│   │   ├── 500.txt
│   │   ├── seed1.txt
│   │   ├── seed2.txt
│   │   ├── seed3.txt
│   │   ├── seed4.txt
│   │   ├── seed5.txt
│   ├── classes.txt              # Possible SCP object classes
│   ├── constraints.txt          # Writing constraints for SCPs
│   ├── info.txt                 # Additional SCP lore/context
│   ├── requirements.txt         # Extra dependencies for rules (optional)
│
│── .gitignore
│── config.txt                   # Store your Google API key here
│── program.py                   # Main script to generate SCPs
│── requirements.txt             # Python dependencies
```

---

## ⚙️ Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/valkbit/the-factory.git
   cd the-factory
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your **Google API key**:  
   Open the file named `config.txt` in the project root and set the variable:
   ```txt
   GOOGLE_API_KEY=your_api_key_here
   ```

---

## 🚀 Usage

Run the program:
```bash
python program.py
```

The program will:
1. Collect context from `rules/` and example SCPs.  
2. Generate a new SCP file with description, containment procedures, object class, and sometimes an event log.  
3. Display the SCP in the terminal with colorized formatting.  
4. Ask if you want to save it in the `results/` folder.

---

## 📑 Example Output

```
Item #: SCP-9342

Object Class: Euclid

Special Containment Procedures:
[Generated text...]

Description:
[Generated text...]

Event Log:
[Generated log text...]
```

---

## 🛠️ Dependencies

- [colorama](https://pypi.org/project/colorama/) – For colorful terminal output.  
- [google-genai](https://pypi.org/project/google-genai/) – Gemini API client.  
- Python 3.9+ recommended.

Install via:
```bash
pip install -r requirements.txt
```

---

## 📌 Notes

- Generated SCP IDs are random (`SCP-9000`–`SCP-9999`).  
- Event logs are not always included (40% chance).  
- The system adapts log type (exploration, interview, breach, etc.) based on SCP description.  
- You can expand the training context by adding more files to the `rules/` or `examples/` folders.

---

## ⚠️ Disclaimer

This project is a **fan-made tool** and is not affiliated with the SCP Foundation.  
All SCP lore belongs to the [SCP Wiki](http://www.scpwiki.com/) community (under [CC BY-SA 3.0 License](https://creativecommons.org/licenses/by-sa/3.0/)).
