import os


def string_with_default(name, default):
    env_val = os.getenv(name)
    if not env_val:
        return default
    return env_val

def intWithDefault(name, default):
    return int(string_with_default(name, default))

# The opencv channel to use for video capture
CAM_CHANNEL = intWithDefault("CAM_CHANNEL", 0)

# The fps to render at
RENDER_FPS = intWithDefault("RENDER_FPS", 40)

# directory where saved av files go
SAVED_VIDEOS_DIR = string_with_default("SAVED_VIDEOS_DIR", "data/messages")

SOURCE_IMAGES_DIR = string_with_default("SOURCE_IMAGES_DIR", "src/images")
