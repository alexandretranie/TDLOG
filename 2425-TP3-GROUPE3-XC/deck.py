import player
import tile


def tile_no_links():
    return tile.Tile(links=[])


def tile_one_link(sides, color):
    return tile.Tile(
        links=[
            tile.Link(
                sides=frozenset(sides),
                color=color,
            )
        ]
    )


def tile_two_links(
    sides1,
    color1,
    sides2,
    color2,
):
    return tile.Tile(
        links=[
            tile.Link(
                sides=frozenset(sides1),
                color=color1,
            ),
            tile.Link(
                sides=frozenset(sides2),
                color=color2,
            ),
        ]
    )


def tile_consecutive(color):
    return tile_one_link((tile.Side.NORTH, tile.Side.EAST), color)


def tile_opposite(color):
    return tile_one_link((tile.Side.NORTH, tile.Side.SOUTH), color)


def tile_consecutives(color1, color2):
    return tile_two_links(
        (tile.Side.NORTH, tile.Side.EAST),
        color1,
        (tile.Side.SOUTH, tile.Side.WEST),
        color2,
    )


def make_tiles():
    return (
        [
            # 4 tiles with no links
            tile_no_links()
            for _ in range(4)
        ]
        + [
            # 8 tiles (2 per color) with one link between consecutive sides
            tile_consecutive(color)
            for color in player.Color
            for _ in range(2)
        ]
        + [
            # 12 tiles (3 per color) with one link between opposite sides
            tile_opposite(color)
            for color in player.Color
            for _ in range(3)
        ]
        + [
            # 12 tiles (2 per combination of two different colors)
            # with two links between consecutive sides
            tile_consecutives(color1, color2)
            for color1 in player.Color
            for color2 in player.Color
            if color1.value < color2.value
            for _ in range(2)
        ]
    )

def parse_link_spec(link_str):
    """Analyse la spécification du lien et la retourne sous forme de tuple."""
    try:
        sides, color_str = link_str.split(':')
        side1, side2 = sides.split('-')
        side1 = getattr(tile.Side, side1.upper())
        side2 = getattr(tile.Side, side2.upper())
        color = getattr(player.Color, color_str.upper())
        return (side1, side2), color
    except Exception as e:
        raise ValueError(f"Erreur dans la spécification du lien : {link_str}, {e}")

def load_tiles(path):
    tiles = []
    # Ouverture du fichier et lecture. 
    with open(path, 'r') as f:
        for line in f:
            # Méthode supprimant tous les commentaires (chaine de caractère derrière %). On met l'agument 0 pour prendre ce qu'il y a avant le %. 
            clean_line = line.split('%')[0].strip()

            # Ignore les lignes vides ou les commentaires.
            if not clean_line:
                continue

            # Traiter les directives NO_LINKS, ONE_LINK et TWO_LINKS
            if clean_line == "NO_LINKS":
                tiles.append(tile_no_links())

            elif clean_line.startswith("ONE_LINK"):
                # Extraire les spécifications du lien
                try:
                    # On prend les caractères après ONE_LINK
                    link_spec = clean_line.split("ONE_LINK")[1].strip()
                    # Utilisation de la fonction parse_link_spec(link_spec) pour extraire les spécificités de la tuile.
                    sides, color = parse_link_spec(link_spec)
                    tiles.append(tile_one_link(sides, color))
                except Exception as e:
                    raise ValueError(f"Erreur dans ONE_LINK : {clean_line}, {e}")

            elif clean_line.startswith("TWO_LINKS"):
                # Extraire les deux spécifications de liens
                try:
                    link_specs = clean_line.split("TWO_LINKS")[1].strip().split("&")
                    sides1, color1 = parse_link_spec(link_specs[0].strip())
                    sides2, color2 = parse_link_spec(link_specs[1].strip())
                    tiles.append(tile_two_links(sides1, color1, sides2, color2))
                except Exception as e:
                    raise ValueError(f"Erreur dans TWO_LINKS : {clean_line}, {e}")

            else:
                raise ValueError(f"Ligne non reconnue : {clean_line}")
    return tiles



