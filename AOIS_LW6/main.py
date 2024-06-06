from table import HashTable

if __name__ == "__main__":
    ht = HashTable()

    ht.insert("key1", "value1")
    ht.insert("key2", "value2")
    ht.insert("key3", "value3")


    print("Search for 'key2':", ht.search("key2"))

    ht.update("key2", "new_value2")

    print("Search for 'key2' after update:", ht.search("key2"))

    ht.delete("key2")

    print("Search for 'key2' after deletion:", ht.search("key2"))

    print(ht)
    table = HashTable(25)

    for i in range(25):
        table.insert(str(i), i)

    print(str(table))
