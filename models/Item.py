from attr import attrs

from .item_modifier import ItemModifier


@attrs(auto_attribs=True)
class Item:
    rarity: str = 'Rare'
    name: str = 'Pseudo'
    base: str = 'Pseudo'

    quality: int = 0
    # TODO: handle base stats
    stats: [str] = []

    raw_sockets: str = ''
    # Item level/ Map tier
    iLevel: int = 0

    # TODO: support map IIQ, IIR, pack size
    modifiers: [(ItemModifier, str)] = []
    corrupted: bool = False
    mirrored: bool = False

    # TODO: handle influence types, as an enum?
    influence: [str] = []

    def __attrs_post_init__(self):
        sockets = self.raw_sockets.lower()
        self.r_sockets = sockets.count('r')
        self.b_sockets = sockets.count('b')
        self.g_sockets = sockets.count('g')
        self.w_sockets = sockets.count('w')
        self.a_sockets = sockets.count('a')  # abyssal
        # R-R-R-R R-R is not incorrectly registered as 5 link
        self.links = sockets.count('-') - sockets.count(' ') + 1

    def get_pseudo_mods(self):
        raise NotImplementedError

    def get_json(self):
        # For items
        data = {
            "query": {

                # Required, we only wanna look at things that are online
                # and recently posted.
                "status": {
                    "option": "online"
                },

                # For all items, a type (base) is required. For unique items,
                # we must also include the name of the item.
                "name": "Kaom's Sign",
                # The actual type of the item -- an item base.
                "type": "Coral Ring",

                # When we're searching a map, there is no name, only a type
                # that has an option field, accompanied by a discriminate.
                # The discriminate in the current league's case is "warfortheatlas"
                "type": {
                    "option": "Ghetto Map",
                    "discriminate": "warfortheatlas"
                },

                # When we're searching a prophecy, "Prophecy" is required
                # as the type, and it's name is required.
                "name": "Fated Connections",
                "type": "Prophecy",

                # A flask is treated just the same as items are. See line 50.

                # Gems can be found by just searching it's type. For gems,
                # quality and gem level are quite important -- see
                # misc_filters below.
                "type": "Fireball",

                # Jewels are treated just the same as items are. See line 50.

                # A metamorph sample. The request with one of these types
                # should probably be accompanied by stats for direct matching.
                # We should probably also specify an ilvl misc_filter.
                "type": "Metamorph Brain",
                "type": "Metamorph Liver",
                "type": "Metamorph Lung",
                "type": "Metamorph Heart",
                "type": "Metamorph Eye",

                # Captured Beasts are a totally different story... they have
                # different fields than I've seen on any other items, with
                # Genus, Group, and Family. Not sure what we should do here.

                # Stats to search for; When we're including no stats in our
                # search, the minimum standard value given for stats would be:
                # [{ "type": "and", "filters": [] }]
                "stats": [
                    {
                        "type": "and",
                        "filters": [   
                            {
                                "id": "explicit.stat_3509831",
                                "value": {
                                    "min": 1,
                                    "max": 999
                                }
                            },
                            {
                                "id": "pseudo.pseudo_total_life",
                                "value": {
                                    "min": 23,
                                    "max": 999
                                }
                            },
                            # ... any more mods here.
                        ]
                    },

                    # This next one could be another section of stats
                    # to be searching for; when normally trading,
                    # we could use this to specify a set of stats for "count"
                    # etc, but when we're predicting things, we won't do this.
                    {
                        "type": "count",
                        "value": {
                            "min": 1,
                            "max": 1
                        },
                        "filters": []
                    }
                ],

                # Filters specified here are all options on the left-side
                # of pathofexile.com/trade's UI.
                "filters": {
                    "socket_filters": {
                        "filters": {
                            "links": {
                                "min": 6,
                                "max": 6
                            }
                        }
                    },

                    # For certain item attributes, we must specify misc_filters
                    # This field is quite important for gems or bases.
                    "misc_filters": {
                        "ilvl": {
                            "min": 1,
                            "max": 100
                        },
                        "quality": {
                            "min": 20,
                            "max": 20
                        },
                        "gem_level": {
                            "min": 21,
                            "max": 21
                        },
                        # Gem experience
                        "gem_level_progress": {
                            "min": 0,
                            "max": 666
                        },

                        # Influences should be given in this section.
                        "shaper_item": {
                            "option": "true"
                        },

                        # If "Any" is specified, these specifications with
                        # { "option": "true" } should be omitted.
                        "corrupted": {
                            "option": "true"
                        },

                        # Veiled items
                        "veiled": {
                            "option": "true"
                        }
                    }
                }
            },
            # We always want to sort in ascending order; this should be
            # included with every search payload.
            "sort": {
                "price": "asc"
            }
        }

        # For exchange, which includes: currency, fragments, catalysts, oils,
        # incubators, scarabs, delve resonators, delve fossils, vials,
        # essences, cards and maps.
        data = {
            "exchange": {
                "status": {
                    "option": "online"
                },
                # Whatever currency we want to count
                "have": ["chaos"],

                # Map format
                "want": ["beach-map-tier-1"],

                # Divination Cards
                "want": ["a-dab-of-ink"],

                # Essences
                "want": ["muttering-essence-of-hatred"],

                # Vials
                "want": ["vial-of-dominance"],

                # Fossils
                "want": ["scorched-fossil"],

                # Resonators
                "want": ["primitive-alchemical-resonator"],

                # Scarabs
                "want": ["rusted-breach-scarab"],

                # Incubators
                "want": ["fine-incubator"],

                # Oils
                "want": ["silver-oil"],

                # Catalysts
                "want": ["turbulent-catalyst"],

                # We should look up fragments as items in the Item
                # alternative request above. Seems that fragments
                # are named quite oddly in the exchange trade site,
                # and searching them up as items should be fine.
                # In the fragment case, we should just supply the fragment
                # name as the "type" field of a query.
            },
        }
        raise NotImplementedError
