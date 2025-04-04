def main():
    # Test file created
    test_filename = "test_input.txt"
    test_content = "x 45 5.4 -33 34RR size y1234 || x" #Write the example content to file
    create_test_file(test_filename, test_content)

    # Lexical analyzer created.
    analyzer = LexicalAnalyzer(test_filename)

    # Main loop
    while True:
        print("\nMenu:")
        print("1. Call lex()")
        print("2. Show symbol table")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            token = analyzer.lex()
            if token:
                print(token)
            else:
                print("End of file reached.")
                # Reset file to beginning for next reads
                analyzer = LexicalAnalyzer(test_filename)

        elif choice == '2':
            analyzer.show_symbol_table()

        elif choice == '3':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

class Token:


    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return f"<{self.token_type}, {self.value}>"


class LexicalAnalyzer:
    def __init__(self, filename):
        self.symbol_table = []  # To store identifiers
        self.filename = filename
        self.content = ""
        self.position = 0

        try:
            with open(filename, 'r') as f:
                self.content = f.read()
        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
            self.content = ""

    def add_to_symbol_table(self, identifier):

        if identifier in self.symbol_table:
            return self.symbol_table.index(identifier)
        else:
            self.symbol_table.append(identifier)
            return len(self.symbol_table) - 1

    def show_symbol_table(self):
        """Display the contents of the symbol table"""
        print("\nSymbol Table:")
        for i, symbol in enumerate(self.symbol_table):
            print(f"{i}: {symbol}")
        print()
    def lex(self):
        if self.position >= len(self.content):
            return None
        while self.position < len(self.content) and self.content[self.position].isspace():
            self.position += 1
        if self.position >= len(self.content):
            return None


        current = self.content[self.position]


        if current.isalpha() or current == '_':
            return self._handle_identifier()


        elif current.isdigit():
            return self._handle_number_starting_with_digit()

        elif current == '-' and self.position + 1 < len(self.content) and self.content[self.position + 1].isdigit():
            return self._handle_negative_number()


        elif current == '&':
            self.position += 1
            if self.position < len(self.content) and self.content[self.position] == '&':
                self.position += 1
                return Token("LOGICAL_AND", "nothing")
            return Token("BITWISE_AND", "nothing")

        elif current == '|':
            self.position += 1
            if self.position < len(self.content) and self.content[self.position] == '|':
                self.position += 1
                return Token("LOGICAL_OR", "nothing")
            return Token("BITWISE_OR", "nothing")

        else:
            error_lexeme = current
            self.position += 1

            # Continue until we hit whitespace or a valid token start
            while (self.position < len(self.content) and
                   not self.content[self.position].isspace() and
                   not self._is_valid_token_start(self.content[self.position])):
                error_lexeme += self.content[self.position]
                self.position += 1

            return Token("ERROR", f"\"{error_lexeme}\"")

    def _is_valid_token_start(self, char):
        """Check if a character could be the start of a valid token"""
        return (char.isalpha() or char == '_' or char.isdigit() or
                char == '-' or char == '&' or char == '|')

    def _handle_identifier(self):
        start = self.position
        self.position += 1

        # Continue collecting the identifier
        while (self.position < len(self.content) and
               (self.content[self.position].isalnum() or self.content[self.position] == '_')):
            self.position += 1

        identifier = self.content[start:self.position]
        index = self.add_to_symbol_table(identifier)
        return Token("ID", index)

    def _handle_number_starting_with_digit(self):
        """Process a number token that starts with a digit"""
        start = self.position
        self.position += 1

        # Continue collecting digits
        while self.position < len(self.content) and self.content[self.position].isdigit():
            self.position += 1

        # Check for an error case like "34RR"
        if (self.position < len(self.content) and
                (self.content[self.position].isalpha() or self.content[self.position] == '_')):
            # This is an error like "34RR", collect the whole lexeme
            while (self.position < len(self.content) and
                   (self.content[self.position].isalnum() or self.content[self.position] == '_')):
                self.position += 1

            error_lexeme = self.content[start:self.position]
            return Token("ERROR", f"\"{error_lexeme}\"")

        # Check for decimal point (float)
        if (self.position < len(self.content) and
                self.content[self.position] == '.'):
            self.position += 1  # Skip the decimal point

            # Continue collecting digits for the fractional part
            while self.position < len(self.content) and self.content[self.position].isdigit():
                self.position += 1

            # Convert to float
            float_value = float(self.content[start:self.position])
            return Token("FLOAT", float_value)

        # It's an integer
        int_value = int(self.content[start:self.position])
        return Token("INTEGER", int_value)

    def _handle_negative_number(self):
        """Process a negative number token"""
        start = self.position
        self.position += 2  # Skip the minus sign and the first digit

        # Continue collecting digits
        while self.position < len(self.content) and self.content[self.position].isdigit():
            self.position += 1

        # Check for decimal point (float)
        if (self.position < len(self.content) and
                self.content[self.position] == '.'):
            self.position += 1  # Skip the decimal point

            # Continue collecting digits for the fractional part
            while self.position < len(self.content) and self.content[self.position].isdigit():
                self.position += 1

            # Convert to float
            float_value = float(self.content[start:self.position])
            return Token("FLOAT", float_value)

        # It's an integer
        int_value = int(self.content[start:self.position])
        return Token("INTEGER", int_value)


def create_test_file(filename, content):
    """Create a test file with the given content"""
    try:
        with open(filename, 'w') as file:
            file.write(content)
        print(f"Test file '{filename}' created successfully.")
    except Exception as e:
        print(f"Error creating test file: {e}")


if __name__ == "__main__":
    main()