def decimal_to_binary(num):

    if num == 0:
        return "0"
    binary = ""
    while num > 0:
        binary = str(num % 2) + binary
        num //= 2
    return binary


def fraction_to_binary(frac, length=23):

    binary = ""
    while frac > 0 and len(binary) < length:
        frac *= 2
        if frac >= 1:
            binary += "1"
            frac -= 1
        else:
            binary += "0"
    return binary


def float_to_binary32(value):

    if value == 0:
        return "00000000000000000000000000000000"
    

    sign = 0 if value >= 0 else 1
    value = abs(value)

    int_part = int(value)
    frac_part = value - int_part

    int_bin = decimal_to_binary(int_part)
    frac_bin = fraction_to_binary(frac_part)

    if int_part != 0:
        exponent = len(int_bin) - 1
        mantissa = int_bin[1:] + frac_bin
    else:
        exponent = -frac_bin.find('1') - 1
        mantissa = frac_bin[frac_bin.find('1') + 1:]

    exponent += 127
    mantissa = mantissa[:23].ljust(23, '0')

    if len(mantissa) < 23:
        mantissa = mantissa.ljust(23, '0')
    else:
        mantissa = mantissa[:23]

    binary32 = f"{sign}{decimal_to_binary(exponent).zfill(8)}{mantissa}"
    return binary32


def binary32_to_float(binary):

    if binary == '00000000000000000000000000000000':
        return 0.0
    

    sign = int(binary[0])
    exponent = int(binary[1:9], 2) - 127
    mantissa = binary[9:]

    int_part = 1 if exponent >= 0 else 0
    frac_part = 0.0

    for i in range(min(exponent, len(mantissa))):
        int_part = int_part * 2 + int(mantissa[i])

    for i in range(len(mantissa[exponent:])):
        frac_part += int(mantissa[exponent + i]) * 2 ** -(i + 1)

    value = int_part + frac_part
    if sign == 1:
        value = -value
    return value


def add_floating_point_numbers(value1, value2):

    binary1 = float_to_binary32(value1)
    binary2 = float_to_binary32(value2)

    print(f"Original {value1}: {binary1}")
    print(f"Original {value2}: {binary2}")

    sum_binary = binary32_to_float(binary1) + binary32_to_float(binary2)
    sum_binary32 = float_to_binary32(sum_binary)

    print(f"Sum: {sum_binary32}")

    return sum_binary


result = add_floating_point_numbers(1.0, 1.5)
print(f"Результат сложения: {result}")
