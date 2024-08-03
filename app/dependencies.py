async def read_video_url(cap, identifer):
    if cap[identifer] is None:
        raise ValueError("Video stream not initialized")
