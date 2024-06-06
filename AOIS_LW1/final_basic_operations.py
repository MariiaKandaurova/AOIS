def convert_positive_to_binary(positive_string):
    result = ''
    num = int(positive_string)
    while num > 0:
        result = str((num % 2)) + result
        num = num // 2
    return result.zfill(8)


def convert_negative_to_binary(negative_str):
    negative_result = ''
    num = int(negative_str)
    if num >= 0:
        return "Number is not negative."
    num = abs(num)
    while num > 0:
        negative_result = str((num % 2)) + negative_result
        num = num // 2
    final_negative_result = '1' + negative_result.zfill(7)
    return final_negative_result


def convert_to_twos_complement(input_num, check_negative=True):
    if isinstance(input_num, str):
        try:
            input_num = int(input_num)
        except ValueError:
            return "Ошибка: входное значение должно быть числом или строкой, представляющей число."
    negative_num = abs(input_num)
    incremental_figure = 1
    reverse_result = ''
    result_of_translation = ''

    while negative_num > 0:
        reverse_result = str(negative_num % 2) + reverse_result
        negative_num //= 2

    reverse_result = reverse_result.zfill(8)

    if check_negative and input_num < 0:
        not_reverse_result = reverse_result.translate(str.maketrans('01', '10'))

        final_reverse_result = not_reverse_result
        for index in range(len(final_reverse_result) - 1, -1, -1):
            if final_reverse_result[index] == '1' and incremental_figure == 1:
                result_of_translation = '0' + result_of_translation
            elif final_reverse_result[index] == '0' and incremental_figure == 1:
                result_of_translation = '1' + result_of_translation
                incremental_figure = 0
            else:
                result_of_translation = final_reverse_result[index] + result_of_translation

        if incremental_figure == 1:
            result_of_translation = '1' + result_of_translation
    else:
        result_of_translation = reverse_result

    result_of_translation = result_of_translation.zfill(8)

    return result_of_translation


def add_two_complements(first_term_value, second_term_value, mode='twos_complement'):
    first_term = first_term_value
    second_term = second_term_value
    if mode == 'twos_complement':
        first_term = convert_to_twos_complement(first_term_value)
        second_term = convert_to_twos_complement(second_term_value)
    elif mode == 'direct_code':
        pass

    sum_of_two_digit = ''
    carry = '0'

    for index1, index2 in zip(reversed(first_term), reversed(second_term)):
        ones_count = sum([index1 == '1', index2 == '1', carry == '1'])
        if ones_count == 0:
            sum_of_two_digit = '0' + sum_of_two_digit
            carry = '0'
        elif ones_count == 1:
            sum_of_two_digit = '1' + sum_of_two_digit
            carry = '0'
        elif ones_count == 2:
            sum_of_two_digit = '0' + sum_of_two_digit
            carry = '1'
        else:
            sum_of_two_digit = '1' + sum_of_two_digit
            carry = '1'

    if carry == '1':
        sum_of_two_digit = '1' + sum_of_two_digit

    sum_of_two_digit = sum_of_two_digit[-8:]

    return sum_of_two_digit


def difference(reduced_value, subtracted_value):
    reduced = convert_to_twos_complement(reduced_value, check_negative=True)
    subtracted = convert_to_twos_complement(-subtracted_value, check_negative=True)

    sum_of_digits = ''
    shift = '0'

    for index1, index2 in zip(reversed(reduced), reversed(subtracted)):
        ones_count = sum([index1 == '1', index2 == '1', shift == '1'])
        if ones_count == 0:
            sum_of_digits = '0' + sum_of_digits
            shift = '0'
        elif ones_count == 1:
            sum_of_digits = '1' + sum_of_digits
            shift = '0'
        elif ones_count == 2:
            sum_of_digits = '0' + sum_of_digits
            shift = '1'
        else:
            sum_of_digits = '1' + sum_of_digits
            shift = '1'

    if shift == '1':
        sum_of_digits = '1' + sum_of_digits

    sum_of_digits = sum_of_digits[-8:]

    return sum_of_digits


def multiplication(mltplcnd_value, mltplr_value):
    multiplication_result = "0" * 16
    result_sign = '0' if mltplcnd_value * mltplr_value >= 0 else '1'

    multiplicand = convert_positive_to_binary(abs(mltplcnd_value))
    multiplier = convert_positive_to_binary(abs(mltplr_value))
    multiplier = multiplier[::-1]
    for index, value in enumerate(multiplier):
        if index == 0 and value == "1":
            multiplication_result = multiplicand
            continue
        if value == '1':
            multiplicand = multiplicand[1:] + "0"
            multiplication_result = add_two_complements(multiplication_result, multiplicand, mode='direct_code')
        else:
            multiplicand = multiplicand[1:] + "0"
            continue

    return multiplication_result


def convert_to_ones_complement(input_num):
    if isinstance(input_num, str):
        try:
            input_num = int(input_num)
        except ValueError:
            return "Ошибка: входное значение должно быть числом или строкой, представляющей число."
    if input_num >= 0:
        return convert_positive_to_binary(input_num)
    else:
        abs_num = abs(input_num)
        binary_representation = convert_positive_to_binary(abs_num)
        ones_complement = binary_representation.translate(str.maketrans('01', '10'))
        return ones_complement


def main():
    # Пример положительного числа
    positive_string = 42
    positive_binary = convert_positive_to_binary(positive_string)
    print(f"Положительное число {positive_string} в прямом коде: {positive_binary}")

    # Пример отрицательного числа
    negative_string = -42
    negative_binary = convert_negative_to_binary(negative_string)
    print(f"Отрицательное число {negative_string} в прямом коде: {negative_binary}")

    # Пример числа в дополнительном коде
    twos_complement_number = -42
    twos_complement_binary = convert_to_twos_complement(twos_complement_number)
    print(f"Число {twos_complement_number} в дополнительном коде: {twos_complement_binary}")

    # Пример сложения чисел в дополнительном коде
    first_term_value = -42
    second_term_value = 23
    sum_result = add_two_complements(first_term_value, second_term_value)
    print(f"Сумма {first_term_value} и {second_term_value} в дополнительном коде: {sum_result}")

    # Пример вычитания чисел в дополнительном коде
    reduced_value = 42
    subtracted_value = 23
    difference_result = difference(reduced_value, subtracted_value)
    print(f"Разность {reduced_value} и {subtracted_value} в дополнительном коде: {difference_result}")

    # Пример умножения чисел в прямом коде
    multiplicand_value = 6
    multiplier_value = 7
    multiplication_result = multiplication(multiplicand_value, multiplier_value)
    print(f"Произведение {multiplicand_value} и {multiplier_value} в прямом коде: {multiplication_result}")

    # Пример числа в обратном коде
    ones_complement_number = -42
    ones_complement_binary = convert_to_ones_complement(ones_complement_number)
    print(f"Число {ones_complement_number} в обратном коде: {ones_complement_binary}")


if __name__ == "__main__":
    main()
