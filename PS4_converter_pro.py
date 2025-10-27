import subprocess

print("🎮✨ PS4 Video Converter Pro ✨🎮")
print("=================================\n")
print("Convert any video into a PS4-friendly MP4 file — fast, easy, and high-quality!\n")

# Ask for input video
input_file = input("📂 Enter the *input video file name* (with extension): ").strip()
while not input_file:
    input_file = input("⚠️ Please enter a valid file name: ").strip()

# Ask for output video name
output_file = input("💾 Enter the *output file name* (e.g. MyVideo_PS4.mp4): ").strip()
if not output_file:
    output_file = "ps4_ready.mp4"
    print("➡️  No output name entered. Using default: ps4_ready.mp4")

# Show preset options
print("\n⚙️  Choose your *encoding speed preset*:")
print("   🟢 ultrafast  – Fastest (biggest file, lowest compression)")
print("   🔵 superfast  – Very quick")
print("   🟣 veryfast   – Great balance of speed & size")
print("   🟠 faster     – Slightly slower, better compression")
print("   🟡 fast       – Good balance (recommended)")
print("   ⚪ medium     – Standard FFmpeg preset")
print("   🔴 slow       – Higher quality, slower encode")
print("   🔵 slower     – Even better compression, slower")
print("   🟤 veryslow   – Maximum compression, longest encode")

preset = input("\n🎚️  Enter your chosen preset (default = fast): ").strip().lower()
if preset == "":
    preset = "fast"

valid_presets = [
    "ultrafast", "superfast", "veryfast", "faster",
    "fast", "medium", "slow", "slower", "veryslow"
]
if preset not in valid_presets:
    print(f"\n⚠️  '{preset}' is not a valid preset. Defaulting to 'fast'.")
    preset = "fast"

# Ask if user wants resize
resize_choice = input("\n🖥️  Resize video to 1080p Full HD? (y/n): ").strip().lower()
resize_filter = ""
if resize_choice == "y":
    resize_filter = "-vf scale=1920:1080"
    print("📏  Resize enabled: 1920x1080")
else:
    print("📏  Keeping original resolution.")

# Ask for quality
print("\n💎  Choose your *video quality level* (CRF value):")
print("   0  = Lossless (huge file)")
print("   18 = Visually perfect (recommended)")
print("   20 = High quality (default)")
print("   23 = Good quality, smaller file")
print("   28 = Faster, lower quality")

crf_value = input("\n🎚️  Enter CRF value (default = 20): ").strip()
if crf_value == "":
    crf_value = "20"

# Show chosen settings summary
print("\n🔧  Conversion Settings Summary:")
print(f"   📂 Input:  {input_file}")
print(f"   💾 Output: {output_file}")
print(f"   ⚙️  Preset: {preset}")
print(f"   💎 Quality (CRF): {crf_value}")
print(f"   🖥️  Resize: {'Yes (1080p)' if resize_filter else 'No'}")
print("\n🚀 Starting conversion... please wait.\n")

# Build FFmpeg command
cmd = [
    "ffmpeg",
    "-i", input_file,
    "-c:v", "libx264",
    "-preset", preset,
    "-crf", crf_value,
    "-profile:v", "high",
    "-level", "4.2",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "160k",
    "-ac", "2",
    "-movflags", "+faststart",
    "-threads", "0"  # use all CPU cores
]

if resize_filter:
    cmd += resize_filter.split()

cmd.append(output_file)

# Run FFmpeg
try:
    subprocess.run(cmd, check=True)
    print(f"\n✅ Done! File saved as: {output_file}")
    print("🎮 Your video is now fully PS4-compatible — enjoy watching on your console! 🙌")
except subprocess.CalledProcessError:
    print("\n❌ Conversion failed. Please check the input file and try again.")
except FileNotFoundError:
    print("\n⚠️ FFmpeg not found. Install it in Termux with:")
    print("   👉 pkg install ffmpeg -y")