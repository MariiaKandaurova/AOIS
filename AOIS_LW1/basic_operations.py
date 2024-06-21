def transform_pos_to_bin(positive_string):
    result = ''
    num = int(positive_string)
    while num > 0:
        result = str((num % 2)) + result
        num = num // 2
    return result.zfill(8)

def transform_neg_to_bin(negative_str):
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

def transform_to_twos(input_num, check_negative=True):
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

def bin_to_dec(binary_str):
    return int(binary_str, 2)

def direct_code_to_dec(binary_str):
    if binary_str[0] == '0':  # Positive number
        return bin_to_dec(binary_str)
    else:  # Negative number
        return -bin_to_dec(binary_str[1:])

def twos_complement_to_dec(binary_str):
    n = len(binary_str)
    if binary_str[0] == '0':
        return bin_to_dec(binary_str)
    else:
        inverted_bits = ''.join('1' if bit == '0' else '0' for bit in binary_str)
        increment = bin_to_dec(inverted_bits) + 1
        return -increment


def ones_complement_to_decimal(bin_str):
    is_negative = bin_str[0] == '1'
    if is_negative:
        inverted_bin_str = ''.join('1' if bit == '0' else '0' for bit in bin_str)
        decimal_value = int(inverted_bin_str, 2)
        return -(decimal_value + 0)
    else:
        return int(bin_str, 2)

def dob_two_compl(first_term_value, second_term_value, mode='twos_complement'):
    first_term = first_term_value
    second_term = second_term_value
    if mode == 'twos_complement':
        first_term = transform_to_twos(first_term_value)
        second_term = transform_to_twos(second_term_value)
    elif mode == 'direct_code':
        pass

    two_digit_total = ''
    transfer_bit = '0'

    for index1, index2 in zip(reversed(first_term), reversed(second_term)):
        ones_count = sum([index1 == '1', index2 == '1', transfer_bit == '1'])
        if ones_count == 0:
            two_digit_total = '0' + two_digit_total
            transfer_bit = '0'
        elif ones_count == 1:
            two_digit_total = '1' + two_digit_total
            transfer_bit = '0'
        elif ones_count == 2:
            two_digit_total = '0' + two_digit_total
            transfer_bit = '1'
        else:
            two_digit_total = '1' + two_digit_total
            transfer_bit = '1'

    if transfer_bit == '1':
        two_digit_total = '1' + two_digit_total

    two_digit_total = two_digit_total[-8:]

    return two_digit_total

def do_the_diff(reduced_value, subtracted_value):
    reduced = transform_to_twos(reduced_value, check_negative=True)
    subtracted = transform_to_twos(-subtracted_value, check_negative=True)

    sum_of_digits = ''
    shift_magnitude = '0'

    for index1, index2 in zip(reversed(reduced), reversed(subtracted)):
        ones_count = sum([index1 == '1', index2 == '1', shift_magnitude == '1'])
        if ones_count == 0:
            sum_of_digits = '0' + sum_of_digits
            shift_magnitude = '0'
        elif ones_count == 1:
            sum_of_digits = '1' + sum_of_digits
            shift_magnitude = '0'
        elif ones_count == 2:
            sum_of_digits = '0' + sum_of_digits
            shift_magnitude = '1'
        else:
            sum_of_digits = '1' + sum_of_digits
            shift_magnitude = '1'

    if shift_magnitude == '1':
        sum_of_digits = '1' + sum_of_digits

    sum_of_digits = sum_of_digits[-8:]

    return sum_of_digits

def do_the_mult(mltplcnd_value, mltplr_value):
    multiplication_result = "0" * 16
    result_sign = '0' if mltplcnd_value * mltplr_value >= 0 else '1'

    multiplicand = transform_pos_to_bin(abs(mltplcnd_value))
    multiplier = transform_pos_to_bin(abs(mltplr_value))
    multiplier = multiplier[::-1]
    for index, value in enumerate(multiplier):
        if index == 0 and value == "1":
            multiplication_result = multiplicand
            continue
        if value == '1':
            multiplicand = multiplicand[1:] + "0"
            multiplication_result = dob_two_compl(multiplication_result, multiplicand, mode='direct_code')
        else:
            multiplicand = multiplicand[1:] + "0"
            continue

    return multiplication_result

def transform_to_ones(input_num):
    if isinstance(input_num, str):
        try:
            input_num = int(input_num)
        except ValueError:
            return "Ошибка: входное значение должно быть числом или строкой, представляющей число."
    if input_num >= 0:
        return transform_pos_to_bin(input_num)
    else:
        abs_num = abs(input_num)
        binary_representation = transform_pos_to_bin(abs_num)
        ones_complement = binary_representation.translate(str.maketrans('01', '10'))
        return ones_complement

def main():
    positive_string = 42
    positive_binary = transform_pos_to_bin(positive_string)
    print(f"Положительное число {positive_string} в прямом коде: {positive_binary}")
    positive_decimal = bin_to_dec(positive_binary)
    print(f"Бинарное число {positive_binary} обратно в десятичное: {positive_decimal}")

    negative_string = -42
    negative_binary = transform_neg_to_bin(negative_string)
    print(f"Отрицательное число {negative_string} в прямом коде: {negative_binary}")
    negative_decimal = direct_code_to_dec(negative_binary)
    print(f"Бинарное число {negative_binary} в прямом коде обратно в десятичное: {negative_decimal}")

    ones_complement_number = -49
    ones_complement_binary = transform_to_ones(ones_complement_number)
    print(f"Число {ones_complement_number} в обратном коде: {ones_complement_binary}")
    ones_complement_decimal = ones_complement_to_decimal(ones_complement_binary)
    print(f"Бинарное число {ones_complement_binary} в обратном коде обратно в десятичное: {ones_complement_decimal}")

    # Пример числа в дополнительном коде
    twos_complement_number = -42
    twos_complement_binary = transform_to_twos(twos_complement_number)
    print(f"Число {twos_complement_number} в дополнительном коде: {twos_complement_binary}")
    twos_complement_decimal = twos_complement_to_dec(twos_complement_binary)
    print(f"Бинарное число {twos_complement_binary} в дополнительном коде обратно в десятичное: {twos_complement_decimal}")

    first_term_value = -42
    second_term_value = 23
    sum_result = dob_two_compl(first_term_value, second_term_value)
    print(f"Сумма {first_term_value} и {second_term_value} в дополнительном коде: {sum_result}")
    sum_decimal = twos_complement_to_dec(sum_result)
    print(f"Сумма в дополнительном коде {sum_result} обратно в десятичное: {sum_decimal}")

    reduced_value = 42
    subtracted_value = 23
    difference_result = do_the_diff(reduced_value, subtracted_value)
    print(f"Разность {reduced_value} и {subtracted_value} в дополнительном коде: {difference_result}")
    difference_decimal = twos_complement_to_dec(difference_result)
    print(f"Разность в дополнительном коде {difference_result} обратно в десятичное: {difference_decimal}")

    multiplicand_value = 6
    multiplier_value = 7
    multiplication_result = do_the_mult(multiplicand_value, multiplier_value)
    print(f"Произведение {multiplicand_value} и {multiplier_value} в прямом коде: {multiplication_result}")
    multiplication_decimal = bin_to_dec(multiplication_result)
    print(f"Произведение в бинарном виде {multiplication_result} обратно в десятичное: {multiplication_decimal}")

if __name__ == "__main__":
    main()
