import logging
from colorama import Fore
from typing import Dict

def create_pseudo_mods(j: Dict) -> Dict:
    """
    Combines life and resists into pseudo-mods

    Returns modified JSON #TODO change this to only modify the stats section of the JSON
    """
    # Combine life and resists for pseudo-stats
    total_ele_resists = 0
    total_chaos_resist = 0
    total_life = 0

    # TODO: Find a way to not hard-code
    # TODO: Support for attributes (including str->life), added phys to attacks, life regen
    solo_resist_ids = {
        "explicit.stat_3372524247",  # Explicit fire resist
        "explicit.stat_1671376347",  # Explicit lightning resist
        "explicit.stat_4220027924",  # Explicit cold resist
        "implicit.stat_3372524247",  # Implicit fire resist
        "implicit.stat_1671376347",  # Implicit lightning resist
        "implicit.stat_4220027924",  # Implicit cold resist
        "crafted.stat_3372524247",  # Crafted fire resist
        "crafted.stat_1671376347",  # Crafted lightning resist
        "crafted.stat_4220027924",  # Crafted cold resist
    }

    dual_resist_ids = {
        "explicit.stat_2915988346",  # Explicit fire and cold resists
        "explicit.stat_3441501978",  # Explicit fire and lightning resists
        "explicit.stat_4277795662",  # Explicit cold and lightning resists
        "implicit.stat_2915988346",  # Implicit fire and cold resists
        "implicit.stat_3441501978",  # Implicit fire and lightning resists
        "implicit.stat_4277795662",  # Implicit cold and lightning resists
        "crafted.stat_2915988346",  # Crafted fire and cold resists
        "crafted.stat_3441501978",  # Crafted fire and lightning resists
        "crafted.stat_4277795662",  # Crafted cold and lightning resists
    }

    triple_resist_ids = {
        "explicit.stat_2901986750",  # Explicit all-res
        "implicit.stat_2901986750",  # Implicit all-res
        "crafted.stat_2901986750",  # Crafted all-res
    }

    solo_chaos_resist_ids = {
        "explicit.stat_2923486259",  # Explicit chaos resist
        "implicit.stat_2923486259",  # Implicit chaos resist
    }

    dual_chaos_resist_ids = {
        "crafted.stat_378817135",  # Crafted fire and chaos resists
        "crafted.stat_3393628375",  # Crafted cold and chaos resists
        "crafted.stat_3465022881",  # Crafted lightning and chaos resists
    }

    life_ids = {
        "explicit.stat_3299347043",  # Explicit maximum life
        "implicit.stat_3299347043",  # Implicit maximum life
    }

    possible_ids = solo_resist_ids.copy()
    possible_ids.update(dual_resist_ids)
    possible_ids.update(triple_resist_ids)
    possible_ids.update(solo_chaos_resist_ids)
    possible_ids.update(dual_chaos_resist_ids)
    possible_ids.update(life_ids)

    combined_filters = []

    # Solo elemental resists
    for i in j["query"]["stats"][0]["filters"]:
        if i["id"] in possible_ids:
            if i["id"] in solo_resist_ids:
                total_ele_resists += int(i["value"]["min"])
                combined_filters.append(i)

            # Dual elemental resists
            elif i["id"] in dual_resist_ids:
                total_ele_resists += 2 * int(i["value"]["min"])
                combined_filters.append(i)

            # Triple elemental resists
            elif i["id"] in triple_resist_ids:
                total_ele_resists += 3 * int(i["value"]["min"])
                combined_filters.append(i)

            # Solo chaos resists
            elif i["id"] in solo_chaos_resist_ids:
                total_chaos_resist += int(i["value"]["min"])
                combined_filters.append(i)

            # Dual chaos resists
            elif i["id"] in dual_chaos_resist_ids:
                total_chaos_resist += int(i["value"]["min"])
                total_ele_resists += int(i["value"]["min"])
                combined_filters.append(i)

            # Maximum life
            elif i["id"] in life_ids:
                total_life += int(i["value"]["min"])
                combined_filters.append(i)

    # Round down to nearest 10 for combined stats (off by default)
    do_round = False
    if do_round:
        total_ele_resists = total_ele_resists - (total_ele_resists % 10)
        total_chaos_resist = total_chaos_resist - (total_chaos_resist % 10)
        total_life = total_life - (total_life % 10)

    # Remove stats that have been combined into psudo-stats
    j["query"]["stats"][0]["filters"] = [e for e in j["query"]["stats"][0]["filters"] if e not in combined_filters]

    if total_ele_resists > 0:
        j["query"]["stats"][0]["filters"].append(
            {"id": "pseudo.pseudo_total_elemental_resistance", "value": {"min": total_ele_resists, "max": 999},}
        )
        logging.info(
            "[o] Combining the "
            + Fore.CYAN
            + f"elemental resistance"
            + Fore.RESET
            + " mods from the list into a pseudo-parameter"
        )
        logging.info(
            "[+] Pseudo-mod "
            + Fore.GREEN
            + f"+{total_ele_resists}% total Elemental Resistance (pseudo)"
            + Fore.RESET
        )

    if total_chaos_resist > 0:
        j["query"]["stats"][0]["filters"].append({
            "id": "pseudo.pseudo_total_chaos_resistance",
            "value": {"min": total_chaos_resist, "max": 999},
        })
        logging.info(
            "[o] Combining the "
            + Fore.CYAN
            + f"chaos resistance"
            + Fore.RESET
            + " mods from the list into a pseudo-parameter"
        )
        logging.info("[+] Pseudo-mod " + Fore.GREEN + f"+{total_chaos_resist}% total Chaos Resistance (pseudo)")

    if total_life > 0:
        j["query"]["stats"][0]["filters"].append({
            "id": "pseudo.pseudo_total_life",
            "value": {"min": total_life, "max": 999}
        })
        logging.info(
            "[o] Combining the "
            + Fore.CYAN
            + f"maximum life"
            + Fore.RESET
            + " mods from the list into a pseudo-parameter"
        )
        logging.info(
            "[+] Pseudo-mod "
            + Fore.GREEN
            + f"+{total_life} to maximum Life (pseudo)"
            + Fore.RESET
        )

    return j

