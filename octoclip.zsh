#Add this to your .zshrc file

# Generate an octopus prompt and copy the JSON output to the clipboard
function octoclip() {
  local tentacle_count=${1:-1}
  local output
  output=$(cd /Users/blackseatech/401jk && python3 generate_octopus_prompt.py \
    --tentacle-accessories "$tentacle_count")
  printf "%s\n" "$output"
  printf "%s" "$output" | pbcopy
  echo "Copied octopus prompt (version $prompt_version) to clipboard."
}