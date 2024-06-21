def transform_dec_to_bin(numeric_val):

    if numeric_val == 0:
        return "0"
    bit_code = ""
    while numeric_val > 0:
        bit_code = str(numeric_val % 2) + bit_code
        numeric_val //= 2
    return bit_code


def drob_to_bin(frac, length=23):
    bit_code = ""
    while frac > 0 and len(bit_code) < length:
        frac *= 2
        if frac >= 1:
            bit_code += "1"
            frac -= 1
        else:
            bit_code += "0"
    return bit_code


def transform_float_to_bin32(data_val):

    if data_val == 0:
        return "00000000000000000000000000000000"

    """Перевод числа с плавающей запятой в 32-битное двоичное представление."""
    polarity_sign = 0 if data_val >= 0 else 1
    data_val = abs(data_val)

    int_part = int(data_val)
    frac_part = data_val - int_part

    int_bin = transform_dec_to_bin(int_part)
    frac_bin = drob_to_bin(frac_part)

    if int_part != 0:
        exponent_magnitude = len(int_bin) - 1
        mantissa_magnitude = int_bin[1:] + frac_bin
    else:
        exponent_magnitude = -frac_bin.find('1') - 1
        mantissa_magnitude = frac_bin[frac_bin.find('1') + 1:]

    exponent_magnitude += 127
    mantissa_magnitude = mantissa_magnitude[:23].ljust(23, '0')


    if len(mantissa_magnitude) < 23:
        mantissa_magnitude = mantissa_magnitude.ljust(23, '0')
    else:
        mantissa_magnitude = mantissa_magnitude[:23]

    binary32 = f"{polarity_sign}{transform_dec_to_bin(exponent_magnitude).zfill(8)}{mantissa_magnitude}"
    return binary32


def transform_bin32_to_float(bit_code):
    if bit_code == '00000000000000000000000000000000':
        return 0.0

    """Перевод 32-битного двоичного представления в число с плавающей запятой."""
    polarity_sign = int(bit_code[0])
    exponent_magnitude = int(bit_code[1:9], 2) - 127
    mantissa_magnitude = bit_code[9:]

    mantissa = 1.0
    for i in range(len(mantissa_magnitude)):
        mantissa += int(mantissa_magnitude[i]) * 2 ** -(i + 1)

    data_val = mantissa * (2 ** exponent_magnitude)
    if polarity_sign == 1:
        data_val = -data_val
    return data_val


def sum_of_float_numbers(data_val1, data_val2):
    binary1 = transform_float_to_bin32(data_val1)
    binary2 = transform_float_to_bin32(data_val2)

    print(f"Original {data_val1}: {binary1}")
    print(f"Original {data_val2}: {binary2}")

    decimal1 = transform_bin32_to_float(binary1)
    decimal2 = transform_bin32_to_float(binary2)

    binary_aggregate = decimal1 + decimal2

    binary_aggregate_rounded = round(binary_aggregate, 2)
    sum_binary32 = transform_float_to_bin32(binary_aggregate_rounded)
    print(f"Sum: {sum_binary32}")
    return binary_aggregate_rounded


result_of_calculation = sum_of_float_numbers(0.5, 0.5)
print(f"Результат сложения: {result_of_calculation}")
