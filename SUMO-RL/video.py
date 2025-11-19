import os
import cv2

output_dir = "/home/jay/RL-examples/SUMO-RL/outputs/visualization_outs"
frames_dir = os.path.join(output_dir, "frames")
video_path = os.path.join(output_dir, "simulation_video.mp4")
fps = 30  # frames per second for video

# Create video from frames
images = sorted([img for img in os.listdir(frames_dir) if img.endswith(".png")])
if not images:
    raise RuntimeError("No frames captured. Check your SUMO simulation or frames directory.")

# Read the first frame to get dimensions
first_frame = cv2.imread(os.path.join(frames_dir, images[0]))
height, width, layers = first_frame.shape

# Initialize video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

# Write all frames to video
for img_name in images:
    frame = cv2.imread(os.path.join(frames_dir, img_name))
    video.write(frame)

video.release()
print(f"Video saved at: {video_path}")