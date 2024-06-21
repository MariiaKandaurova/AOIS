from table import Table
import methods

if __name__ == "__main__":
    print("Algorithmic method")
    print("SKFN")
    print(f"result: {methods.calc_SKNF_algorithmic('(!(a|b)->!c)')}")
    print("SDNF")
    print(f"result: {methods.calc_SDNF_algorithmic('(!(a|b)->!c)')}")
    print("Karno method")
    print("SKNF")
    print(f"result: {methods.calc_SKNF_Karno_method('(!(a|b)->!c)')}")
    print("SDNF")
    print(f"result: {methods.calc_SDNF_Karno_method('(!(a|b)->!c)')}")
    print("Table method")
    print("SDNF")
    print(f"result: {methods.calc_SDNF_table_method('(!(a|b)->!c)')}")
    print("SKNF")
    print(f"result: {methods.calc_SKNF_table_method('(!(a|b)->!c)')}")
