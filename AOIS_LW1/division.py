def transform_to_twos(input_num, check_negative=True):
    if isinstance(input_num, str):
        try:
            input_num = int(input_num)
        except ValueError:
            return "Ошибка: входное значение должно быть числом или строкой, представляющей число."
    negative_num = abs(input_num)
    incremental_figure = 1
    reverse_operation_output = ''
    operation_output_of_translation = ''

    while negative_num > 0:
        reverse_operation_output = str(negative_num % 2) + reverse_operation_output
        negative_num //= 2

    reverse_operation_output = reverse_operation_output.zfill(8)

    if check_negative and input_num < 0:
        not_reverse_operation_output = reverse_operation_output.translate(str.maketrans('01', '10'))

        final_reverse_operation_output = not_reverse_operation_output
        for index in range(len(final_reverse_operation_output) - 1, -1, -1):
            if final_reverse_operation_output[index] == '1' and incremental_figure == 1:
                operation_output_of_translation = '0' + operation_output_of_translation
            elif final_reverse_operation_output[index] == '0' and incremental_figure == 1:
                operation_output_of_translation = '1' + operation_output_of_translation
                incremental_figure = 0
            else:
                operation_output_of_translation = final_reverse_operation_output[index] + operation_output_of_translation

        if incremental_figure == 1:
            operation_output_of_translation = '1' + operation_output_of_translation
    else:
        operation_output_of_translation = reverse_operation_output

    operation_output_of_translation = operation_output_of_translation.zfill(8)

    return operation_output_of_translation

def binary_to_decimal(binary_str):
    if '.' in binary_str:
        integer_part, fractional_part = binary_str.split('.')
        if integer_part[0] == '1':  # Отрицательное число
            inverted_binary_digits = ''.join('1' if binary_digit == '0' else '0' for binary_digit in integer_part)
            decimal_value = -(int(inverted_binary_digits, 2) + 1)
        else:
            decimal_value = int(integer_part, 2)

        fractional_value = 0
        for i, binary_digit in enumerate(fractional_part):
            if binary_digit == '1':
                fractional_value += 2 ** (-(i + 1))

        return decimal_value + fractional_value
    else:
        if binary_str[0] == '1':
            inverted_binary_digits = ''.join('1' if binary_digit == '0' else '0' for binary_digit in binary_str)
            return -(int(inverted_binary_digits, 2) + 1)
        else:
            return int(binary_str, 2)

def diff_search(reduced, subtracted, mode1="not_conversed"):
    if mode1 == "conversed":
        reduced = int(transform_to_twos(reduced, check_negative=True), 2)
        subtracted = int(transform_to_twos(-int(subtracted, 2), check_negative=True), 2)
    elif mode1 == "not_conversed":
        reduced = int(reduced, 2)
        subtracted = int(subtracted, 2)

    operation_output = reduced - subtracted

    if operation_output < 0:
        operation_output = bin(operation_output & ((1 << (max(len(bin(reduced)), len(bin(subtracted))) - 2)) - 1))[2:]
    else:
        operation_output = bin(operation_output)[2:]

    max_length = max(len(bin(reduced)), len(bin(subtracted))) - 2
    operation_output = operation_output.zfill(max_length)

    return operation_output

def comparement_leading_zeros(first_binary_number, second_binary_number):
    first_binary_number = first_binary_number.lstrip('0') or '0'
    second_binary_number = second_binary_number.lstrip('0') or '0'

    if len(first_binary_number) > len(second_binary_number):
        return True
    elif len(first_binary_number) < len(second_binary_number):
        return False
    else:
        return first_binary_number >= second_binary_number

def div_in_direct(division_numerator, division_denominator, decimal_precision=10):
    division_numerator = bin(int(division_numerator))[2:].zfill(8)
    division_denominator = bin(int(division_denominator))[2:].zfill(8)

    division_numerator = division_numerator.lstrip('0') or '0'
    division_denominator = division_denominator.lstrip('0') or '0'

    if division_denominator == '0':
        raise ValueError("Division by zero is not allowed.")

    binary_quotient = ''
    intermediate_remainder = ''

    for binary_digit in division_numerator:
        intermediate_remainder += binary_digit
        if comparement_leading_zeros(intermediate_remainder, division_denominator):
            intermediate_remainder = diff_search(intermediate_remainder, division_denominator, "not_conversed")
            binary_quotient += '1'
        else:
            binary_quotient += '0'
        intermediate_remainder = intermediate_remainder.lstrip('0') or '0'

    if decimal_precision > 0:
        binary_quotient += '.'
        while decimal_precision > 0:
            intermediate_remainder += '0'
            if comparement_leading_zeros(intermediate_remainder, division_denominator):
                intermediate_remainder = diff_search(intermediate_remainder, division_denominator, "not_conversed")
                binary_quotient += '1'
            else:
                binary_quotient += '0'
            intermediate_remainder = intermediate_remainder.lstrip('0') or '0'
            decimal_precision -= 1

    return binary_quotient

def representation_in_decimal (binary_operation_output):
    return binary_to_decimal(binary_operation_output)

division_numerator = "15"
division_denominator = "8"
binary_operation_output = div_in_direct(division_numerator, division_denominator)
print("Результат деления в бинарном формате:", binary_operation_output)

decimal_operation_output = representation_in_decimal (binary_operation_output)
print("Результат деления в десятичном формате:", decimal_operation_output)
