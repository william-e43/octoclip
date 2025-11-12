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
    background_color = random_choice(TRAITS["BackgroundPool"])
    outfit = random_choice(TRAITS["Outfits"])

    # Accessories are now dicts: get key and color
    head_acc_dict = TRAITS["HeadAccessories"]
    body_acc_dict = TRAITS["BodyAccessories"]
    tentacle_acc_dict = TRAITS["TentacleAccessories"]
    eye_acc_dict = TRAITS["EyeAccessories"]

    head_accessory = random_choice(list(head_acc_dict.keys()))
    body_accessory = random_choice(list(body_acc_dict.keys()))
    tentacle_accessory = random_choice(list(tentacle_acc_dict.keys()))
    eye_accessory = random_choice(list(eye_acc_dict.keys()))

    head_accessory_color = head_acc_dict[head_accessory]
    body_accessory_color = body_acc_dict[body_accessory]
    tentacle_accessory_color = tentacle_acc_dict[tentacle_accessory]
    eye_accessory_color = eye_acc_dict[eye_accessory]

    eyes = random_choice(TRAITS["EyeExpressions"])
    mouth = random_choice(TRAITS["MouthExpressions"])
    head_type = random_choice(TRAITS["HeadTypes"])
    face_tentacles = random_choice(TRAITS["FaceTentacles"])

    color_lock_phrases = [
        f"base skin {base_color}",
        f"underside {underside_color}",
        f"sucker accents {sucker_color}",
        f"background {background_color}",
    ]

    def add_accessory_color(label, accessory_name, color_value):
        if isinstance(color_value, str) and color_value.startswith("#"):
            color_lock_phrases.append(f"{label} ({accessory_name.lower()}) {color_value}")

    add_accessory_color("head accessory", head_accessory, head_accessory_color)
    add_accessory_color("body accessory", body_accessory, body_accessory_color)
    add_accessory_color("tentacle accessory", tentacle_accessory, tentacle_accessory_color)
    add_accessory_color("eye accessory", eye_accessory, eye_accessory_color)

    color_instructions = (
        "Sora color instructions: use the provided hex values exactly as written — no shifts, "
        "blends, or invented hues. Lock the palette to "
        + "; ".join(color_lock_phrases)
        + ". Use these colors exactly as flat tones — no hue shift, no desaturation, "
        + "no gradient transitions, and no color bleed between materials."
    )

    # sizing_notes = TRAITS["Sizing"]
    # sizing_instructions = (
    #     "Sora sizing instructions: framed as a portrait 2:3 canvas that shows the octopus from crown to lower tentacles with even spacing above and below — "
    #     + sizing_notes
    # )
    framing_note = (
        "Keep the full octopus body and all eight tentacles completely inside the portrait frame — no cropped crowns, limbs, or accessories."
    )

    style_lock = "Style consistency rule: identical line weight, contour thickness, and character proportions across all outputs."
    system_instructions = (
        "System: Generate a collectible 2D cartoon portrait of an anthropomorphic octopus character in a consistent visual template."
    )

    def acc_desc(acc, color):
        if acc.lower() == "none":
            return "no accessory"
        if color is None:
            return f"{acc.lower()} (no color)"
        return f"{acc.lower()} (color {color})"

    def face_tentacle_desc(length):
        if length.lower() == "none":
            return "no prominent face tentacles"
        return f"{length.lower()} face tentacles"

    prompt = textwrap.dedent(f"""
    Composition and pose: A slouched upright anthropomorphic octopus, facing right in the iconic Rektirement Club silhouette with full mantle and all eight tentacles visible.
    Tentacle count: Exactly eight tentacles — show every limb and do not add or remove any.
    Subject identity: Head type {head_type.lower()} with {face_tentacle_desc(face_tentacles)}; skin shows base tone {base_color}, undersides {underside_color}, sucker accents {sucker_color}, and solid background color {background_color}.
    Accessory map: Wearing a {outfit.lower()} with {acc_desc(body_accessory, body_accessory_color)}, plus {acc_desc(head_accessory, head_accessory_color)} and {acc_desc(tentacle_accessory, tentacle_accessory_color)} on limbs, and {acc_desc(eye_accessory, eye_accessory_color)} around the eyes.
    Expression and vibe: {eyes.lower()} eyes paired with a {mouth.lower()} mouth for a cohesive demeanor.
    Style and rendering: Rendered in vivid cartoon collectible style — bold outlines, flat saturated colors, smooth gradients, no realism, no shadows. {style_lock}
    Framing note: {framing_note}
    Color discipline: Strict hex color mapping — {color_instructions}
    Negative constraints: {TRAITS["NegativePrompt"]}
    """)

    negative_prompt = TRAITS["NegativePrompt"]
    sizing = TRAITS["Sizing"]  # Keep general sizing reference for downstream use

    return {
        "system_instructions": system_instructions,
        "base_color": base_color,
        "underside_color": underside_color,
        "sucker_color": sucker_color,
        "background": background_color,
        "outfit": outfit,
        "head_accessory": head_accessory,
        "body_accessory": body_accessory,
        "tentacle_accessory": tentacle_accessory,
        "eye_accessory": eye_accessory,
        "head_accessory_color": head_accessory_color,
        "body_accessory_color": body_accessory_color,
        "tentacle_accessory_color": tentacle_accessory_color,
        "eye_accessory_color": eye_accessory_color,
        "eyes": eyes,
        "mouth": mouth,
        "head_type": head_type,
        "face_tentacles": face_tentacles,
        "prompt": " ".join(prompt.split()),
        "negative_prompt": negative_prompt,
        "color_instructions": color_instructions,
        # "sizing_instructions": sizing_instructions,
        "sizing": sizing
    }

# --- Example run ---
if __name__ == "__main__":
    octo = generate_cephalopod_prompt()
    print(json.dumps(octo, indent=2))
