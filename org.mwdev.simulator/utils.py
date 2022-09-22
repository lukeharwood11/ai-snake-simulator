def calculate_fps(self, time_elapsed):
    # convert to seconds (from milliseconds)
    t = time_elapsed
    # save to attribute
    self._calc_fps = round(1 / t)