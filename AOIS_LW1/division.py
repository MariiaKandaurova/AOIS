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

def difference(reduced, subtracted, mode1="not_conversed"):
    if mode1 == "conversed":
        # Преобразование в дополнительный код
        reduced = int(convert_to_twos_complement(reduced, check_negative=True), 2)
        subtracted = int(convert_to_twos_complement(-int(subtracted, 2), check_negative=True), 2)
    elif mode1 == "not_conversed":
        # Преобразуем строки в целые числа, если переданы в виде строк
        reduced = int(reduced, 2)
        subtracted = int(subtracted, 2)


    result = reduced - subtracted


    if result < 0:

        result = bin(result & ((1 << (max(len(bin(reduced)), len(bin(subtracted))) - 2)) - 1))[2:]
    else:
        result = bin(result)[2:]

    # Нормализация длины результата
    max_length = max(len(bin(reduced)), len(bin(subtracted))) - 2
    result = result.zfill(max_length)

    return result


def is_greater_or_equal(bin1, bin2):
    bin1 = bin1.lstrip('0') or '0'
    bin2 = bin2.lstrip('0') or '0'

    if len(bin1) > len(bin2):
        return True
    elif len(bin1) < len(bin2):
        return False
    else:
        return bin1 >= bin2


def division_in_direct_code(dividend, divisor, precision=10):
    dividend = bin(int(dividend))[2:].zfill(8)
    divisor = bin(int(divisor))[2:].zfill(8)
    dividend = dividend.lstrip('0') or '0'
    divisor = divisor.lstrip('0') or '0'

    if divisor == '0':
        raise ValueError("Division by zero is not allowed.")

    quotient = ''
    remainder = ''


    for bit in dividend:
        remainder += bit

        if is_greater_or_equal(remainder, divisor):
            remainder = difference(remainder, divisor, "not_conversed")
            quotient += '1'
        else:
            quotient += '0'
        remainder = remainder.lstrip('0') or '0'


    if precision > 0:
        quotient += '.'

        while precision > 0:
            remainder += '0'
            if is_greater_or_equal(remainder, divisor):
                remainder = difference(remainder, divisor, "not_conversed")
                quotient += '1'
            else:
                quotient += '0'
            remainder = remainder.lstrip('0') or '0'
            precision -= 1

    return quotient


dividend = "15"
divisor = "4"
result = division_in_direct_code(dividend, divisor)
print("Результат деления:", result)
