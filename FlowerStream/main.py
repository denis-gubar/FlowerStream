FLOWER_SET_SIZE: int = 26

# Total number of all flowers in store
store_total_number_large: int = 0
store_total_number_small: int = 0

# the number of distinct flower species in bouquet with sufficient quantity
bouquet_fulfillment: list = []


def main():
    def check():
        for i in range(2 * FLOWER_SET_SIZE):
            if store_flower_collection[i] > 0:
                if i < FLOWER_SET_SIZE:
                    print(chr(ord('A') + i) + ' ' + str(store_flower_collection[i]) + ', ', end='')
                else:
                    print(chr(ord('a') + i - FLOWER_SET_SIZE) + ' ' + str(store_flower_collection[i]) + ', ', end='')
        print()

    def parse_bouquet(bouquet: str, bouquet_index: int):
        if bouquet[0] < 'A' or bouquet[0] > 'Z':
            raise ValueError("Invalid bouquet name")
        if bouquet[1] != 'L' and bouquet[1] != 'S':
            raise ValueError("Invalid bouquet size type")
        flower_collection: list = [0] * 2 * FLOWER_SET_SIZE
        bouquet_id: str = bouquet[0:2]
        index_delta: int = 0 if bouquet[1] == 'L' else FLOWER_SET_SIZE
        count: int = 0
        distinct_total_flower_count: int = 0
        total_flower_count: int = 0
        for i in range(2, len(bouquet)):
            if bouquet[i].isdigit():
                count = count * 10 + int(bouquet[i])
            else:
                if count == 0:
                    raise ValueError("Invalid flower specie quantity in bouquet")
                if bouquet[i] < 'a' or bouquet[i] > 'z':
                    raise ValueError("Invalid flower specie in bouquet")
                flower_specie_index: int = ord(bouquet[i]) - ord('a') + index_delta
                flower_collection[flower_specie_index] = count
                total_flower_count += count
                distinct_total_flower_count += 1
                flower_update_subscribers[flower_specie_index].append(bouquet_index)
                count = 0
        free_flower_count: int = count - total_flower_count
        total_flower_count = count
        if free_flower_count < 0:
            raise ValueError("Total quantity of flowers are less than sum of flowers' quantity in bouquet")
        return bouquet_id, flower_collection, total_flower_count, distinct_total_flower_count, free_flower_count

    def add_new_flower(flower_specie_index: int):
        global store_total_number_large, store_total_number_small, bouquet_fulfillment
        store_flower_collection[flower_specie_index] += 1
        store_total_number_local: int = 0
        if flower_specie_index < FLOWER_SET_SIZE:
            store_total_number_large += 1
            store_total_number_local = store_total_number_large
        else:
            store_total_number_small += 1
            store_total_number_local = store_total_number_small
        # Updating statistics for each affected bouquet design
        for bouquet_index in flower_update_subscribers[flower_specie_index]:
            # [1] means flower_collection
            if bouquet_designs[bouquet_index][1][flower_specie_index] == store_flower_collection[flower_specie_index]:
                bouquet_fulfillment[bouquet_index] += 1
        release_bouquet_index: int = -1
        # check all bouquet designs if any complete mandatory flowers list and
        # whether total quantity of flowers is sufficient to create a bouquet with <release_bouquet_index> index
        for bouquet_index in range(len(bouquet_designs)):
            # [3] means distinct_total_flower_count
            if bouquet_fulfillment[bouquet_index] == bouquet_designs[bouquet_index][3]:
                # [2] means the total number of flowers in bouquet
                if release_bouquet_index == -1 and store_total_number_local >= bouquet_designs[bouquet_index][2]:
                    release_bouquet_index = bouquet_index
        if release_bouquet_index != -1:
            return create_bouquet(release_bouquet_index)
        return None

    def create_bouquet(release_bouquet_index: int):
        global bouquet_fulfillment
        # [1] means flower_collection
        release_flower_collection: list = list(bouquet_designs[release_bouquet_index][1])

        # [4] means the number of flowers to make necessary total quantity
        free_flower_count: int = bouquet_designs[release_bouquet_index][4]
        index_delta: int = 0 if bouquet_designs[release_bouquet_index][0][1] == 'L' else FLOWER_SET_SIZE

        # [0] means bouquet unique identifier <bouquet name><bouquet size>
        release_bouquet_code: str = bouquet_designs[release_bouquet_index][0]

        for flower_specie_index in range(index_delta, index_delta + FLOWER_SET_SIZE):
            store_flower_collection[flower_specie_index] -= release_flower_collection[flower_specie_index]
            if free_flower_count > 0 and store_flower_collection[flower_specie_index] > 0:
                delta: int = min(free_flower_count, store_flower_collection[flower_specie_index])
                free_flower_count -= delta
                store_flower_collection[flower_specie_index] -= delta
                release_flower_collection[flower_specie_index] += delta
            if release_flower_collection[flower_specie_index] > 0:
                release_bouquet_code += str(release_flower_collection[flower_specie_index])
                release_bouquet_code += chr(ord('a') + (flower_specie_index - index_delta))
                store_count: int = store_flower_collection[flower_specie_index]
                release_count: int = release_flower_collection[flower_specie_index]
                global store_total_number_large, store_total_number_small
                if index_delta == 0:
                    store_total_number_large -= release_count
                else:
                    store_total_number_small -= release_count

                # Updating statistics for each affected bouquet design
                for bouquet_index in flower_update_subscribers[flower_specie_index]:
                    # [1] means flower_collection
                    design_count: int = bouquet_designs[bouquet_index][1][flower_specie_index]
                    if store_count + release_count >= design_count > store_count:
                        bouquet_fulfillment[bouquet_index] -= 1

        return release_bouquet_code

    def read_bouquet_input_lines():
        while True:
            bouquet_input_line: str = str(input())
            if bouquet_input_line == '':
                break
            bouquet_id, flower_collection, total_flower_count, distinct_total_flower_count, free_flower_count = \
                parse_bouquet(bouquet_input_line, len(bouquet_designs))
            bouquet_designs.append((bouquet_id,  # bouquet unique identifier <bouquet name><bouquet size>
                                    flower_collection,  # list corresponding to [A-Za-z] flower species
                                    # if <x> is lowercase then small flower size type otherwise large
                                    # on <x> position stores number of <x> flower specie in bouquet
                                    total_flower_count,  # the total number of flowers in bouquet
                                    distinct_total_flower_count,  # the number of distinct flower species in bouquet
                                    free_flower_count))  # the number of flowers to make necessary total quantity

    def read_flower_input_lines():
        try:
            while True:
                flower_input_line: str = str(input())
                if len(flower_input_line) != 2:
                    raise ValueError("Invalid flower input line length")
                if flower_input_line[0] < 'a' or flower_input_line[0] > 'z':
                    raise ValueError("Invalid flower specie")
                if flower_input_line[1] != 'L' and flower_input_line[1] != 'S':
                    raise ValueError("Invalid flower size type")
                flower_specie_index: int = ord(flower_input_line[0]) - ord('a')
                if flower_input_line[-1] == 'S':
                    flower_specie_index += FLOWER_SET_SIZE
                release_bouquet_code: str = add_new_flower(flower_specie_index)
                if release_bouquet_code is not None:
                    print(release_bouquet_code)
        except EOFError:
            pass  # graceful application stop on end of file signal

    # list of immutable bouquet design specification
    bouquet_designs: list = []

    # list corresponding to [A-Za-z] flower species
    # if x is lowercase then small flower size type otherwise large
    # on 'x' position stores number of x flower specie in store
    store_flower_collection: list = [0] * 2 * FLOWER_SET_SIZE

    # list of bouquet designs lists which has specific flower specie of specific size type
    flower_update_subscribers: list = [[] for i in range(2 * FLOWER_SET_SIZE)]

    read_bouquet_input_lines()

    # the number of distinct flower species in bouquet with sufficient quantity
    global bouquet_fulfillment
    bouquet_fulfillment = [0] * len(bouquet_designs)

    read_flower_input_lines()


if __name__ == '__main__':
    try:
        main()
        exit(0)
    except ValueError as err:
        print('ValueError:', err)
        print('Application is terminated')
        exit(1)
