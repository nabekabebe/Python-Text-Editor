# Text Editor with Python Tkinter

This is a simple text editor created using Python Tkinter, a popular GUI toolkit. The editor provides essential features for text editing along with some additional functionalities to enhance the user experience.

## Features

### 1. Line Numbering

The editor displays line numbers, making it easier to navigate through the document.

### 2. Syntax Highlighting

Supports syntax highlighting for various programming languages, enhancing code readability.

### 3. Custom Color Schemes

Users can customize the editor's appearance by defining their color schemes using a JSON-based configuration file.

### 4. Find and Replace

Allows users to search for specific text within the document and replace it with another string.

### 5. Font Customization

Users can customize the font style, size, and other related properties according to their preferences.

## Getting Started

### Prerequisites

- Python 3.x installed on your system
- Required Python libraries (Tkinter, json, etc.)

### Installation

#### Clone the repository:

```bash
git clone https://github.com/nabekabebe/simple-text-editor
```

```bash
cd simple-text-editor
```

### Usage

Run the following command to start the text editor:

```bash
python texteditor.py
```

## Configuration

### Color Scheme

The color scheme is defined in a JSON file (`scheme_color.json`) which can be customized by the user. Here's an example of the color scheme configuration:

```json
{ "fg": "#000000", "bg": "#c4bbbc", "tfg": "#000000", "tbg": "#eceed9" }
```

### IDE-Style Configuration

The editor supports customization through an IDE-like configuration format. The configuration is defined in a JSON file (highlight_config.json) and follows this structure:

```json
{
  "category": {
    "keywords": {
      "color": "orange",
      "matches": ["for", "def", "while", "from", "import", "as", "with", "self"]
    },
    "variables": {
      "color": "red",
      "matches": ["True", "False", "None"]
    },
    "conditionals": {
      "color": "green",
      "matches": ["try", "except", "if", "else", "elif"]
    },
    "functions": {
      "color": "blue",
      "matches": ["int", "str", "dict", "list", "set", "float", "print"]
    },
    "builtins": {
      "color": "brown",
      "matches": "dir"
    }
  },
  "numbers": {
    "color": "purple"
  },
  "strings": {
    "color": "pink"
  },
  "parenthesis": {
    "color": "teal"
  }
}
```

## Contributing

Feel free to contribute and submit pull requests to enhance the functionality of the text editor.

**Happy Coding!**
