import re

class Term:
    def __init__(self, coefficient: int, degree: int):
        self.coefficient = coefficient
        self.degree = degree
        self.next = None

class Polynomial:
    def __init__(self):
        self.head = None

    def add_term(self, coefficient: int, degree: int):
        new_term = Term(coefficient, degree)
        new_term.next = self.head
        self.head = new_term

    def input_from_string(self, poly_str: str):
        # Удаление пробелов
        poly_str = poly_str.replace(' ', '')
        pattern = re.compile(r'([+-]?[^+-]+)')
        terms = pattern.findall(poly_str)
        for term_str in terms:
            try:
                coef, deg = self.parse_term(term_str)
                self.add_term(coef, deg)
            except Exception as e:
                print(f"Ошибка при разборе слагаемого '{term_str}': {e}")
                continue

    def parse_term(self, term_str: str):
        term_str = term_str.strip()
        if 'y' not in term_str:
            coefficient = int(term_str)
            degree = 0
        else:
            # Обработка знаков
            coefficient = 1
            degree = 1
            if term_str.startswith('-'):
                sign = -1
                term_str = term_str[1:]
            elif term_str.startswith('+'):
                sign = 1
                term_str = term_str[1:]
            else:
                sign = 1
            parts = term_str.split('y')
            coef_part = parts[0]
            if coef_part == '' or coef_part == '+':
                coefficient = 1
            elif coef_part == '-':
                coefficient = -1
            else:
                coefficient = int(coef_part)
            coefficient *= sign
            if '^' in term_str:
                match = re.search(r'\^(\d+)', term_str)
                if match:
                    degree = int(match.group(1))
                else:
                    raise ValueError("Некорректный формат степени")
            else:
                degree = 1
        return coefficient, degree

    def simplify(self):
        # Объединение подобных слагаемых
        deg_dict = {}
        current = self.head
        while current:
            deg_dict[current.degree] = deg_dict.get(current.degree, 0) + current.coefficient
            current = current.next
        new_poly = Polynomial()
        for deg, coef in deg_dict.items():
            if coef != 0:
                new_poly.add_term(coef, deg)
        self.head = None
        for deg in sorted(deg_dict.keys(), reverse=True):
            coef = deg_dict[deg]
            if coef != 0:
                self.add_term(coef, deg)

    def output_to_string(self):
        if not self.head:
            return "0"
        terms = []
        current = self.head
        while current:
            coef = current.coefficient
            deg = current.degree
            # Форматирование с учетом знака
            if coef > 0 and terms:
                sign_str = '+ '
            elif coef < 0:
                sign_str = '- '
            else:
                sign_str = ''
            abs_coef = abs(coef)
            if deg == 0:
                term_str = f"{abs_coef}"
            elif deg == 1:
                if abs_coef == 1:
                    term_str = "y"
                else:
                    term_str = f"{abs_coef}y"
            else:
                if abs_coef == 1:
                    term_str = f"y^{deg}"
                else:
                    term_str = f"{abs_coef}y^{deg}"
            if terms:
                if sign_str.strip() == '+':
                    terms.append(f"+ {term_str}")
                elif sign_str.strip() == '-':
                    terms.append(f"- {term_str}")
                else:
                    terms.append(f"{sign_str}{term_str}")
            else:
                if coef < 0:
                    terms.append(f"- {term_str}")
                else:
                    terms.append(f"{term_str}")
            current = current.next
        return ' '.join(terms)

    def save_to_file(self, filename: str):
        with open(filename, 'a', encoding='utf-8') as f:
            poly_str = self.output_to_string()
            f.write(poly_str + '\n')

# Основной интерфейс
def main():
    filename ='polynomial.txt'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            line = f.readline()
        poly = Polynomial()
        poly.input_from_string(line)
        print("Исходный многочлен:")
        print(poly.output_to_string())

        poly.simplify()

        print("Объединенный многочлен:")
        print(poly.output_to_string())

        poly.save_to_file(filename)
        print("Результат добавлен в файл ")

    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

main()