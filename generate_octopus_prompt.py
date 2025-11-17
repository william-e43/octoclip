import json, random, textwrap

# --- Load trait data (from separate JSON file) ---
with open("octopus_traits.json", "r") as f:
    TRAITS = json.load(f)["CephalopodElderGenerator"]

# --- Random helpers ---
def choose_distinct(pool, k=3):
    """Pick k distinct items from a list."""
    return random.sample(pool, k)

def random_choice(pool):
    return random.choice(pool)

# --- Generate Cephalopod Elder ---
def generate_cephalopod_prompt():
    base_color, underside_color, sucker_color = choose_distinct(TRAITS["ColorPool"])
    background_color = "#FFFFFF"
    eye_color = random_choice(TRAITS.get("EyeColors", ["#FFFFFF"]))

    skin_palette = {base_color, underside_color, sucker_color}
    tries = 0
    outfit = random_choice(TRAITS["Outfits"])

    # Accessories are now dicts: get key and color
    head_acc_dict = TRAITS["HeadAccessories"]
    body_acc_dict = TRAITS["BodyAccessories"]
    tentacle_acc_dict = TRAITS["TentacleAccessories"]
    eye_acc_dict = TRAITS["EyeAccessories"]

    head_accessory = random_choice(list(head_acc_dict.keys()))
    body_accessory = random_choice(list(body_acc_dict.keys()))
    tentacle_accessory_count = random.randint(1, min(2, len(tentacle_acc_dict)))
    tentacle_accessories = random.sample(list(tentacle_acc_dict.keys()), tentacle_accessory_count)
    eye_accessory = random_choice(list(eye_acc_dict.keys()))

    eyes = random_choice(TRAITS["EyeExpressions"])
    head_type = random_choice(TRAITS["HeadTypes"])
    face_tentacles = random_choice(TRAITS["FaceTentacles"])

    def acc_desc(acc: str):
        lowered = acc.lower()
        return "no accessory" if lowered == "none" else lowered

    def tentacle_acc_desc(selected: list[str]):
        if not selected:
            return "no accessories"
        return ", ".join(acc_desc(acc) for acc in selected)

    def face_tentacle_desc(length):
        if length.lower() == "none":
            return "no prominent face tentacles"
        return f"{length.lower()} face tentacles"

    raw_prompt = textwrap.dedent(f"""
Render a collectible anthropomorphic octopus in a consistent vector-friendly cartoon template.

- Composition: Upright, relaxed 3/4 right pose. Full mantle and all eight tentacles visible, tentacles are all distinct from one another. And clearly outlined. nothing cropped, no mouth.
    - Style: Uniform line weight, closed vector paths, flat fills only. No gradients, no textures, no realism.
    - Colors: Use hex colors exactly — base {base_color}, underside {underside_color}, suckers {sucker_color}, background {background_color}, eyes {eye_color}.
    - Background: Ensure the entire canvas is pure white (255, 255, 255) with no gradient, shadow, or texture; the white fill must cover the whole background.
- Accessories: Outfit {outfit.lower()}, head {acc_desc(head_accessory)}, body {acc_desc(body_accessory)}, tentacles {tentacle_acc_desc(tentacle_accessories)}, eyes {acc_desc(eye_accessory)}.
- Expression: Eyes {eyes.lower()}.
- Framing: Keep full character inside a 2:3 portrait with balanced whitespace.
    - Coloring: outfits and accessories must each use a color palette distinct from the skin color (and the background); avoid repeating the skin tone when coloring clothing or accessories.
- Details: Ensure tentacles wrap around accessories. Tentacles SHOULD NOT grasp accessories like a human with fingers.
- Details: Ensure eyes are not the same color as the skin or background.
- Style lock: The output should adhere to the silhouette and proportions of the

Negative constraints: {TRAITS["NegativePrompt"]}
""")

    prompt = raw_prompt.replace("'", "")
    negative_prompt = TRAITS["NegativePrompt"]

    system_instructions = (
        "System: Generate a collectible 2D cartoon portrait of an anthropomorphic octopus character in a consistent visual template."
    )

    return {
        "system_instructions": system_instructions,
        "base_color": base_color,
        "underside_color": underside_color,
        "sucker_color": sucker_color,
        "background": background_color,
        "outfit": outfit,
        "head_accessory": head_accessory,
        "body_accessory": body_accessory,
        "tentacle_accessories": tentacle_accessories,
        "eye_accessory": eye_accessory,
        # "head_accessory_color": head_accessory_color,
        #"body_accessory_color": body_accessory_color,
        # "tentacle_accessory_color": tentacle_accessory_color,
        # "eye_accessory_color": eye_accessory_color,
        "eyes": eyes,
        "eye_color": eye_color,
        "head_type": head_type,
        "face_tentacles": face_tentacles,
        "prompt": " ".join(prompt.split()),
        "negative_prompt": negative_prompt
    }

# --- Example run ---
if __name__ == "__main__":
    octo = generate_cephalopod_prompt()
    print(json.dumps(octo, indent=2))
