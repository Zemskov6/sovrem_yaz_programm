"""
PASCAL в PYTHON
1. WRITELN и IF-THEN-ELSE и FOR-TO-DO
"""

class PascalToPythonTranslator:
    def __init__(self):
        self.indent_level = 0

    def translate(self, pascal_code):
        lines = pascal_code.split('\n')
        python_lines = []
        in_main = False

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.upper().startswith('PROGRAM'):
                python_lines.append("# " + line)

            elif line.upper().startswith('VAR'):
                python_lines.append("# Объявление переменных")

            elif line.upper().startswith('BEGIN'):
                in_main = True
                python_lines.append("if __name__ == '__main__':")
                self.indent_level = 1

            elif line.upper() == 'END.':
                in_main = False
                self.indent_level = 0

            elif in_main:
                python_line = self.translate_construction(line)
                if python_line:
                    indent = "    " * self.indent_level
                    python_lines.append(indent + python_line)

            else:
                python_lines.append("# " + line)

        return '\n'.join(python_lines)

    def translate_construction(self, line):
        line = line.strip().rstrip(';')

        if 'WRITELN' in line.upper():
            return self.translate_writeln(line)

        elif line.upper().startswith('IF'):
            result = self.translate_if(line)
            self.indent_level += 1
            return result

        elif line.upper().startswith('FOR'):
            result = self.translate_for(line)
            self.indent_level += 1
            return result

        elif line.upper().startswith('ELSE'):
            self.indent_level -= 1
            return "else:"

        elif ':=' in line:
            return self.translate_assignment(line)

        elif 'READLN' in line.upper():
            return self.translate_readln(line)

        elif line.startswith('{') or line.startswith('//'):
            return "# " + line.lstrip('{').rstrip('}').lstrip('/')

        return None

    def translate_writeln(self, line):
        start = line.find('(')
        end = line.find(')')

        if start != -1 and end != -1:
            content = line[start+1:end]
            parts = self.split_arguments(content)
            return f"print({', '.join(parts)})"
        return "print()"

    def translate_if(self, line):
        line = line.replace('=', '==').replace('<>', '!=')

        if 'THEN' in line.upper():
            condition = line[2:line.upper().index('THEN')].strip()
            return f"if {condition}:"
        return f"if {line[2:].strip()}:"

    def translate_for(self, line):
        parts = line.split()
        if len(parts) >= 7 and parts[2] == ':=' and parts[4].upper() == 'TO' and parts[6].upper() == 'DO':
            var_name = parts[1]
            start_val = parts[3]
            end_val = parts[5]
            return f"for {var_name} in range({start_val}, {end_val} + 1):"
        return f"# Неверный FOR: {line}"

    def translate_assignment(self, line):
        var_name, value = line.split(':=', 1)
        value = value.replace('div', '//').replace('mod', '%')
        return f"{var_name.strip()} = {value.strip()}"

    def translate_readln(self, line):
        start = line.find('(')
        end = line.find(')')
        if start != -1 and end != -1:
            var_name = line[start+1:end].strip()
            return f"{var_name} = input()"
        return "# Ошибка READLN"

    def split_arguments(self, content):
        parts = []
        current = ""
        in_quotes = False

        for char in content:
            if char == "'":
                in_quotes = not in_quotes
                current += char
            elif char == ',' and not in_quotes:
                parts.append(current.strip())
                current = ""
            else:
                current += char

        if current:
            parts.append(current.strip())
        return parts


def main():
    translator = PascalToPythonTranslator()

    pascal_code = """
program DemoProgram;
var 
  i, number: integer;
  name: string;

begin
  writeln('Добро пожаловать в программу!');
  writeln('Как вас зовут?');
  
  readln(name);
  writeln('Привет, ', name, '!');
  
  writeln('Введите число:');
  readln(number);
  
  if number > 10 then
    writeln('Число больше 10')
  else
    writeln('Число 10 или меньше');
  
  if number = 5 then
    writeln('Это пятерка!');
  
  writeln('Счет от 1 до 5:');
  for i := 1 to 5 do
    writeln('i = ', i);
  
  writeln('Программа завершена.');
end.
"""

    python_code = translator.translate(pascal_code)

    print("ИСХОДНАЯ PASCAL ПРОГРАММА:")
    print(pascal_code)

    print("\nТРАНСЛИРОВАННАЯ PYTHON ПРОГРАММА:")
    print(python_code)

if __name__ == "__main__":
    main()
