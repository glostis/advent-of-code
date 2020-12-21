import os
import re


def solve(ingr_list):
    all_allergens = set(allergen for line in ingr_list for allergen in line[1])
    all_ingredients = set(ingredient for line in ingr_list for ingredient in line[0])
    allergen_candidates = dict()
    ingredient_allergen = dict()
    for allergen in all_allergens:
        candidates = all_ingredients
        for ingredients, allergens in ingr_list:
            if allergen in allergens:
                candidates = candidates.intersection(ingredients)
            allergen_candidates[allergen] = candidates

    while any(len(candidates) == 1 for candidates in allergen_candidates.values()):
        for allergen, candidates in allergen_candidates.items():
            if len(candidates) == 1:
                ingredient_allergen[candidates.pop()] = allergen

        for allergen, candidates in allergen_candidates.items():
            new_candidates = set()
            for candidate in candidates:
                if candidate not in ingredient_allergen:
                    new_candidates.add(candidate)
            allergen_candidates[allergen] = new_candidates

    count = 0
    for ingredients, allergens in ingr_list:
        for ingredient in ingredients:
            if ingredient not in ingredient_allergen and not any(
                [ingredient in allergen_candidates[allergen] for allergen in allergens]
            ):
                count += 1
    return count, ingredient_allergen


def main():
    regex = re.compile(r"([\w\s]+) \(contains ([\w\s,]+)\)$")
    ingr_list = []
    with open(os.path.join("data", "day21.txt")) as f:
        for line in f:
            line = line.strip()
            m = regex.match(line)
            ingredients, allergens = m.groups()
            ingredients = set(ingredients.split())
            allergens = set(allergens.split(", "))
            ingr_list.append((ingredients, allergens))

    count, ingredient_allergen = solve(ingr_list)
    print(count)
    print(",".join(dict(sorted(ingredient_allergen.items(), key=lambda item: item[1])).keys()))


if __name__ == "__main__":
    main()
